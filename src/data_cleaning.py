import pandas as pd
import data_loading
import sys


def get_vote_data(source_vote_data):
    """Returns vote_data Dataframe from a source_vote_data like Dataframe."""
    vote_data = source_vote_data.copy()
    vote_data["VoteDate"] = _format_vote_date(vote_data)

    # some votes have identical entries, we don't need duplicates
    vote_data = vote_data.drop_duplicates()

    # Bernasconi Maria has two different family names in the dataset but we need them to be identical
    _rename_bernasconi_maria(vote_data)
    return vote_data


def _format_vote_date(vote_data):
    """Returns the 'VoteDate' column formatted as a datetime object."""
    return pd.to_datetime(
        vote_data["VoteDate"].str[:28],
        format=data_loading.SOURCE_VOTE_DATA_DATE_FORMAT,
    )


def _rename_bernasconi_maria(vote_data):
    """Renames 'Bernasconi Maria' to 'Roth-Bernasconi Maria'."""
    vote_data.loc[
        vote_data["CouncillorName"] == "Bernasconi Maria", "CouncillorName"
    ] = "Roth-Bernasconi Maria"


def get_members(source_members, vote_data):
    """Returns members Dataframe from a source_members like Dataframe. Does NOT filter for National Council!"""

    # Councillors who did not leave the council yet
    did_not_leave = source_members["DateLeaving"].isna()

    # Councillors who left the council after the first vote date in the vote_data Dataframe
    left_after_first_vote = (
        source_members["DateLeaving"] > vote_data["VoteDate"].dt.date.min()
    )
    members = source_members[did_not_leave | left_after_first_vote].copy()

    # Imfeld Adriano is called Imfeld Adrian in the source_members Dataframe
    _members_rename_imfeld_adriano(members)

    # Bignasca Giuliano participated in votes but was not in the national council during
    # that period according to the source_members Dataframe. We have to add him manually.
    members = _add_bignasca_giuliano(members, source_members, vote_data)

    # Fix differing names between Council of States and National Council entries
    _members_update_last_name(members, "Pascale", "Bruderer", "Bruderer Wyss")
    _members_update_last_name(members, "Verena", "Diener", "Diener Lenz")
    return members


def full_names(members):
    """Returns 'LastName FirstName' of members Dataframe."""
    return members["LastName"] + " " + members["FirstName"]


def _members_rename_imfeld_adriano(members):
    """Renames 'Imfeld Adrian' to 'Imfeld Adriano'."""
    members.loc[full_names(members) == "Imfeld Adrian", "FirstName"] = "Adriano"


def _add_bignasca_giuliano(members, source_members, vote_data):
    """Adds an additional entry to the members Dataframe for Bignasca Giuliano."""
    bignasca_vote_data = vote_data[
        vote_data["CouncillorName"] == "Bignasca Giuliano"
    ].drop_duplicates("AffairShortId")

    # Copy last entry for Bignasca Giuliano in source_members
    bignasca = (
        source_members[
            (source_members["FirstName"] == "Giuliano")
            & (source_members["LastName"] == "Bignasca")
        ]
        .sort_values("DateLeaving", ascending=False)
        .iloc[0]
        .copy()
    )

    # Modify DateJoining and DateLeaving to match his minimum/maximum vote dates
    bignasca["DateJoining"] = bignasca_vote_data["VoteDate"].dt.date.min()
    bignasca["DateLeaving"] = bignasca_vote_data["VoteDate"].dt.date.max()
    members = members.append(bignasca).reset_index(drop=True)
    return members


def _members_update_last_name(members, first_name, last_name, new_last_name):
    """Change the last name of a member to new_last_name."""
    members.loc[
        (members["FirstName"] == first_name) & (members["LastName"] == last_name),
        "LastName",
    ] = new_last_name


def get_national_council_members(members):
    """Returns all members in the national council from a members like Dataframe."""
    return (
        members[members["CouncilName"] == "Conseil national"]
        .reset_index(drop=True)
        .drop_duplicates()
    )


def get_full_votes(vote_data, national_council_members):
    """Returns joined Dataframes with joining and leaving dates of the members in
    the National Council matching the vote dates in vote_data.
    """
    full_votes = vote_data.join(
        national_council_members.set_index(full_names(national_council_members)),
        on="CouncillorName",
    )
    full_votes = full_votes[
        (full_votes["VoteDate"] >= full_votes["DateJoining"])
        & (full_votes["VoteDate"] <= full_votes["DateLeaving"])
    ]

    # Some member's joining and leave dates do not match their vote dates.
    # We create new entries for the missing dates.
    missing_names = _full_votes_missing_names(full_votes, vote_data)
    full_votes = full_votes.append(
        _full_votes_new_entries(
            full_votes, missing_names, national_council_members, vote_data
        ),
        sort=True,
    )
    return full_votes


def _full_votes_missing_names(full_votes, vote_data):
    """Returns CouncillorNames present in vote_data but not in full_votes."""
    return vote_data.loc[vote_data.index ^ full_votes.index]["CouncillorName"].values


def _full_votes_new_entries(
    full_votes, missing_names, national_council_members, vote_data
):
    """Creates new entries for members whose joining and leaving dates do not match all their vote dates."""
    new_entries = (
        national_council_members[
            full_names(national_council_members).isin(missing_names)
        ]
        .groupby(["FirstName", "LastName"])
        .first()
        .reset_index()
    )

    # join with the vote_data dataframe
    new_entries = vote_data.loc[vote_data.index ^ full_votes.index].join(
        new_entries.set_index(full_names(new_entries)), on="CouncillorName"
    )

    # create fake 'DateJoining' and 'DateLeaving' values
    new_entries["DateJoining"] = new_entries["VoteDate"].dt.date
    new_entries["DateLeaving"] = new_entries["VoteDate"].dt.date

    return new_entries


if __name__ == "__main__":
    # clean all data if no arguments are passed
    if len(sys.argv) == 1:
        to_clean = ["vote_data", "members", "national_council_members", "full_votes"]
    else:
        to_clean = sys.argv[1:]

    if "vote_data" in to_clean:
        source_vote_data = data_loading.source_vote_data()
        vote_data = get_vote_data(source_vote_data)
        data_loading.save_vote_data(vote_data)
    else:
        vote_data = data_loading.vote_data()

    if "members" in to_clean:
        source_members = data_loading.source_members()
        members = get_members(source_members, vote_data)
        data_loading.save_members(members)
    else:
        members = data_loading.members()

    if "national_council_members" in to_clean:
        national_council_members = get_national_council_members(members)
        data_loading.save_national_council_members(national_council_members)
    else:
        national_council_members = data_loading.national_council_members()

    if "full_votes" in to_clean:
        full_votes = get_full_votes(vote_data, national_council_members)
        data_loading.save_full_votes(full_votes)
