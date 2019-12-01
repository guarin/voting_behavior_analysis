"""Collection of data cleaning functions.
Converts files in 'data' folder into cleaned datasets in 'generated' folder.

    Usage:
    # from terminal in 'src' folder
    $ python data_cleaning.py
"""

import pandas as pd
import data_loading
import create_votes
import sys
import metadata
import util
import webscraping


def get_vote_data(source_vote_data):
    """Returns vote_data Dataframe from a source_vote_data like Dataframe."""
    vote_data = source_vote_data.copy()

    # Remove weird AffairShortIds
    vote_data = vote_data.loc[vote_data["AffairShortId"] > 2]

    vote_data["VoteDate"] = _format_vote_date(vote_data)

    # some votes have identical entries, we don't need duplicates
    vote_data = vote_data.drop_duplicates()

    # Bernasconi Maria has two different family names in the dataset but we need them to be identical
    _rename_bernasconi_maria(vote_data)

    # Add the 'Legislative' to the data
    vote_data["Legislative"] = vote_data["VoteDate"].map(metadata.legislative)

    # Add unique VoteId to the data
    vote_data["VoteId"] = (
        vote_data["AffairShortId"].astype(str)
        + "-"
        + vote_data["VoteRegistrationNumber"].astype(str)
    )

    # Reorder Columns
    columns = ["VoteId", "Legislative", "CouncillorName", "CouncillorId"]
    columns.extend(vote_data.columns.drop(columns))
    return vote_data.loc[:, columns]


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


def get_all_members(source_members):
    all_members = source_members.copy()

    # Add Legislative Column
    all_members["Legislative"] = all_members["DateLeaving"].map(metadata.legislative)

    # Unify Party Abbreviations
    all_members["PartyAbbreviation"] = all_members["PartyAbbreviation"].map(
        metadata.ALL_PARTY_ABBREVIATION
    )
    # Add Simple Party Abbrevation Column
    all_members["SimplePartyAbbreviation"] = all_members["PartyAbbreviation"].map(
        metadata.SIMPLE_PARTY_ABBREVIATION
    )

    # Add Simple Party Id Column
    all_members["SimplePartyId"] = all_members["SimplePartyAbbreviation"].map(
        metadata.SIMPLE_PARTY_TO_INDEX
    )

    # Add FullName Column
    all_members["FullName"] = metadata.full_names(all_members)

    # Reorder columns
    columns = [
        "FullName",
        "Legislative",
        "PartyAbbreviation",
        "SimplePartyAbbreviation",
        "SimplePartyId",
    ]
    columns.extend(all_members.columns.drop(columns))
    return all_members.loc[:, columns]


def get_members(source_members, vote_data, councillor_info):
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

    # Add Legislative Column
    members["Legislative"] = members["DateLeaving"].map(metadata.legislative)

    # Remove entries outside legislatures
    members = members.loc[members["Legislative"].notna()]

    # Unify Party Abbreviations
    members["PartyAbbreviation"] = members["PartyAbbreviation"].map(
        metadata.ALL_PARTY_ABBREVIATION
    )

    # Add Simple Party Abbrevation Column
    members["SimplePartyAbbreviation"] = members["PartyAbbreviation"].map(
        metadata.SIMPLE_PARTY_ABBREVIATION
    )

    # Add Simple Party Id Column
    members["SimplePartyId"] = members["SimplePartyAbbreviation"].map(
        metadata.SIMPLE_PARTY_TO_INDEX
    )

    # Add FullName Column
    members["FullName"] = metadata.full_names(members)

    # Add Image Column
    members = members.join(
        councillor_info[["FullName", "Image"]].set_index("FullName"),
        on="FullName",
        how="left",
    )

    # Reorder columns
    columns = [
        "FullName",
        "Legislative",
        "PartyAbbreviation",
        "SimplePartyAbbreviation",
        "SimplePartyId",
    ]
    columns.extend(members.columns.drop(columns))

    return members.loc[:, columns]


def _members_rename_imfeld_adriano(members):
    """Renames 'Imfeld Adrian' to 'Imfeld Adriano'."""
    members.loc[
        metadata.full_names(members) == "Imfeld Adrian", "FirstName"
    ] = "Adriano"


def _add_bignasca_giuliano(members, source_members, vote_data):
    """Adds an additional entry to the members Dataframe for Bignasca Giuliano."""
    bignasca_vote_data = vote_data[
        vote_data["CouncillorName"] == "Bignasca Giuliano"
    ].drop_duplicates("VoteId")

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


def get_full_votes(vote_data, national_council_members, source_members):
    """Returns joined Dataframes with joining and leaving dates of the members in
    the National Council matching the vote dates in vote_data.
    """
    # Remove data that was not in one of the legislatures
    vote_data = vote_data.loc[vote_data["Legislative"].notna()]

    # Drop column because it exists also in national_council_members
    vote_data = vote_data.drop("Legislative", axis=1)

    full_votes = vote_data.join(
        national_council_members.set_index("FullName"), on="CouncillorName", how="inner"
    )

    full_votes = full_votes[
        (full_votes["VoteDate"] >= full_votes["DateJoining"])
        & (full_votes["VoteDate"] <= full_votes["DateLeaving"])
    ]

    # Some member's joining and leave dates do not match their vote dates.
    # We create new entries for the missing dates.
    missing_names = _full_votes_missing_names(full_votes, vote_data)
    all_members = get_all_members(source_members)
    full_votes = full_votes.append(
        _full_votes_new_entries(full_votes, missing_names, all_members, vote_data),
        sort=True,
        verify_integrity=True,
    )

    full_votes = full_votes.reset_index(drop=True)

    # Reorder Columns
    columns = [
        "VoteId",
        "CouncillorName",
        "Legislative",
        "PartyAbbreviation",
        "SimplePartyAbbreviation",
    ]
    columns.extend(full_votes.columns.drop(columns))

    return full_votes.loc[:, columns]


def _full_votes_missing_names(full_votes, vote_data):
    """Returns CouncillorNames present in vote_data but not in full_votes."""
    return vote_data.loc[vote_data.index ^ full_votes.index]["CouncillorName"].values


def _full_votes_new_entries(full_votes, missing_names, all_members, vote_data):
    """Creates new entries for members whose joining and leaving dates do not match all their vote dates."""
    new_entries = (
        all_members[all_members["FullName"].isin(missing_names)]
        .groupby("FullName")
        .first()
        .reset_index()
    )

    # join with the vote_data dataframe
    new_entries = vote_data.loc[vote_data.index ^ full_votes.index].join(
        new_entries.set_index(metadata.full_names(new_entries)),
        on="CouncillorName",
        how="inner",
    )

    # create fake 'DateJoining' and 'DateLeaving' values
    new_entries["DateJoining"] = new_entries["VoteDate"].dt.date
    new_entries["DateLeaving"] = new_entries["VoteDate"].dt.date
    new_entries["Legislative"] = new_entries["DateLeaving"].map(metadata.legislative)

    return new_entries


if __name__ == "__main__":
    # clean all data if no arguments are passed
    if len(sys.argv) == 1:
        to_clean = [
            "vote_data",
            "members",
            "national_council_members",
            "full_votes",
            "votes",
            "votes_legislative",
        ]
    else:
        to_clean = sys.argv[1:]

    if "vote_data" in to_clean:
        source_vote_data = data_loading.source_vote_data()
        vote_data = get_vote_data(source_vote_data)
        data_loading.save_vote_data(vote_data)
        print("vote_data done.")

    vote_data = data_loading.vote_data()
    source_members = data_loading.source_members()
    councillor_info = webscraping.councillor_info_df()

    if "members" in to_clean:
        members = get_members(source_members, vote_data, councillor_info)
        data_loading.save_members(members)
        print("members done.")

    members = data_loading.members()

    if "national_council_members" in to_clean:
        national_council_members = get_national_council_members(members)
        data_loading.save_national_council_members(national_council_members)
        print("national_council_members done.")

    national_council_members = data_loading.national_council_members()

    if "full_votes" in to_clean:
        full_votes = get_full_votes(vote_data, national_council_members, source_members)
        data_loading.save_full_votes(full_votes)
        print("full_votes done.")

    full_votes = data_loading.full_votes()

    if "votes" in to_clean:
        votes = create_votes.create_votes(full_votes)
        data_loading.save_votes(votes)
        print("votes done.")

    votes = data_loading.votes()

    if "votes_legislative" in to_clean:
        votes_legislative = [
            create_votes.create_votes(df) for df in util.split_legislative(full_votes)
        ]
        for legislative, df in enumerate(votes_legislative):
            data_loading.save_votes_legislative(df, legislative=legislative)
        print("votes_legislative done.")
