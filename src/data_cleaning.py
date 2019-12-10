"""Collection of data cleaning functions.
Converts files in 'data' folder into cleaned datasets in 'generated' folder.

    Usage:
    # from terminal in 'src' folder
    $ python data_cleaning.py
"""

import pandas as pd
import numpy as np
import data_loading
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

    # Rename 'FullName' column to 'FullName' to unify naming conventions
    vote_data = vote_data.rename(columns={"CouncillorName": "FullName"})

    # Some votes have identical entries, we don't need duplicates
    vote_data = vote_data.drop_duplicates()

    # Bernasconi Maria has two different family names in the dataset but we need them to be identical
    _rename_bernasconi_maria(vote_data)

    # Add the 'Legislative' to the data
    vote_data["Legislative"] = _legislative(vote_data["VoteDate"])

    # Add unique VoteId to the data
    vote_data["VoteId"] = _vote_id(vote_data)

    vote_data = vote_data.reset_index(drop=True)

    # Reorder Columns
    columns = ["VoteId", "Legislative", "FullName", "CouncillorId"]
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
        vote_data["FullName"] == "Bernasconi Maria", "FullName"
    ] = "Roth-Bernasconi Maria"


def _vote_id(df):
    return (
        df["AffairShortId"].astype(str) + "-" + df["VoteRegistrationNumber"].astype(str)
    )


def _legislative(series):
    return series.map(metadata.legislative)


def _party_abbreviation(series):
    return series.map(metadata.ALL_PARTY_ABBREVIATION)


def _simple_party_abbreviation(series):
    return series.map(metadata.SIMPLE_PARTY_ABBREVIATION)


def _simple_party_id(series):
    return series.map(metadata.SIMPLE_PARTY_TO_INDEX)


def _full_name(df):
    return metadata.full_names(df)


def _image(df, councillor_info):
    df = df.join(
        councillor_info[["FullName", "Image"]].set_index("FullName"),
        on="FullName",
        how="left",
    )
    return df["Image"]


def _members_add_columns(df, councillor_info):
    df = df.copy()

    # Unify Party Abbreviations
    df["PartyAbbreviation"] = _party_abbreviation(df["PartyAbbreviation"])

    df["Legislative"] = _legislative(df["DateLeaving"])
    df["SimplePartyAbbreviation"] = _simple_party_abbreviation(df["PartyAbbreviation"])
    df["SimplePartyId"] = _simple_party_id(df["SimplePartyAbbreviation"])
    df["FullName"] = _full_name(df)
    df["Image"] = _image(df, councillor_info)

    # Reorder columns
    df = _reorder_columns(df)
    return df


def _reorder_columns(df, columns=None):
    if columns is None:
        columns = [
            "Legislative",
            "FullName",
            "PartyAbbreviation",
            "SimplePartyAbbreviation",
            "SimplePartyId",
        ]
    cols = [*columns, *df.columns.drop(columns).values]
    return df.loc[:, cols]


def get_all_members(source_members, councillor_info):
    all_members = source_members.copy()

    all_members["FullName"] = _full_name(all_members)

    # Rename Imfeld Adrian to Imfeld Adriano to use same name as in votes dataframe
    _members_rename_imfeld_adriano(all_members)

    # Fix differing names between Council of States and National Council entries
    _members_update_last_name(all_members, "Pascale", "Bruderer", "Bruderer Wyss")
    _members_update_last_name(all_members, "Verena", "Diener", "Diener Lenz")

    all_members = _members_add_columns(all_members, councillor_info)
    all_members = all_members.reset_index(drop=True)
    return all_members


def get_members(all_members, vote_data):
    """Returns members who were active from 2007-2019 from all_members like Dataframe.

    Does NOT filter for National Council!
    """

    # Some councillors participated in votes but are missing from the members data
    # We have to add some entries for them
    all_members = _members_add_missing(all_members, vote_data)

    # Select only members who were active between 2007-2019
    members = all_members.loc[all_members["Legislative"].notna()]

    columns = [
        "Legislative",
        "FullName",
        "CouncillorId",
        "PartyAbbreviation",
        "SimplePartyAbbreviation",
        "SimplePartyId",
    ]
    members = _reorder_columns(members, columns)
    # members = _sort_councillor_id(members, na_position="first")
    members = members.reset_index(drop=True)
    return members


def _members_rename_imfeld_adriano(members):
    """Renames 'Imfeld Adrian' to 'Imfeld Adriano'."""
    members.loc[members["FullName"] == "Imfeld Adrian", "FirstName"] = "Adriano"


def _members_update_last_name(members, first_name, last_name, new_last_name):
    """Change the last name of a member to new_last_name."""
    members.loc[
        (members["FirstName"] == first_name) & (members["LastName"] == last_name),
        "LastName",
    ] = new_last_name


def _members_add_missing(members, vote_data):
    """Add councillors who are in vote_data to members dataframe."""

    unique_cols = ["FullName", "Legislative", "CouncilName"]

    # Only keep the most recent info per legislative
    members = members.drop_duplicates(unique_cols, keep="last")

    # Get all members in the vote dataframe
    vote_members = vote_data.loc[
        vote_data["Legislative"].notna(), ["FullName", "Legislative"]
    ].drop_duplicates(["FullName", "Legislative"])

    # Put dummy data in columns depending on legislative. Will be overwritten.
    vote_members["DateJoining"] = metadata.LEGISLATIVE_DATES[0]
    vote_members["DateLeaving"] = metadata.LEGISLATIVE_DATES[0]
    vote_members["Active"] = False
    vote_members["CouncilName"] = "Conseil national"

    # Fill missing legislative data
    for i, (start, end) in enumerate(
        zip(metadata.LEGISLATIVE_DATES[:-1], metadata.LEGISLATIVE_DATES[1:])
    ):
        mask = vote_members["Legislative"] == i
        values = [start, end, i == 2]
        vote_members.loc[mask, ["DateJoining", "DateLeaving", "Active"]] = values

    # Add all vote_members and remove duplicates
    # Keeps old entries from members dataframe and adds only new entries.
    members = (
        members.append(vote_members, sort=True)
        .drop_duplicates(unique_cols, keep="first")
        .reset_index(drop=True)
    )

    # Fill missing values with values from the past, if those do not exist then values from the future.
    # We only want to consider columns which contain data that does not depend on the legislative
    fill_columns = list(
        members.columns.drop(
            ["Legislative", "DateJoining", "DateLeaving", "Active", "CouncilName"]
        )
    )

    members[fill_columns] = (
        members[fill_columns]
        .groupby("FullName", as_index=False)
        .fillna(method="ffill")
        .groupby("FullName", as_index=False)
        .fillna(method="bfill")
        .loc[:, fill_columns]
    )

    members = _add_councillor_id(members, vote_data)
    members = members.reset_index(drop=True)
    return members


def _sort_councillor_id(df, **kwargs):
    df["CouncillorId"] = df["CouncillorId"].astype(int)
    df = df.sort_values("CouncillorId", **kwargs)
    df["CouncillorId"] = df["CouncillorId"].astype(str)
    return df


def _add_councillor_id(members, vote_data):
    vote_data_members = vote_data[["FullName", "CouncillorId"]].drop_duplicates()
    members = members.join(vote_data_members.set_index("FullName"), on="FullName")
    return members


def get_national_council_members(members):
    """Returns all members in the national council from a members like Dataframe."""
    ncm = (
        members[members["CouncilName"] == "Conseil national"]
        .reset_index(drop=True)
        .drop_duplicates()
    )
    ncm = ncm.loc[ncm["CouncillorId"].notna()]
    ncm["Group"] = ncm["ParlGroupAbbreviation"].map(metadata.GROUP)
    # ncm["GroupId"] = ncm["Group"].map(metadata.GROUP_ID)
    ncm["GroupNameEN"] = ncm["Group"].map(metadata.GROUP_NAME_EN)
    ncm = _sort_councillor_id(ncm)
    ncm = ncm.reset_index(drop=True)
    return ncm


def get_full_votes(vote_data, national_council_members):
    """Returns joined Dataframes with joining and leaving dates of the members in
    the National Council matching the vote dates in vote_data.
    """
    # Remove data that was not in one of the legislatures
    vote_data = vote_data.loc[vote_data["Legislative"].notna()]

    full_votes = vote_data.join(
        national_council_members.drop(columns="CouncillorId").set_index(
            ["FullName", "Legislative"]
        ),
        on=["FullName", "Legislative"],
        how="inner",
    )

    assert len(full_votes) == len(vote_data)

    full_votes = full_votes.reset_index(drop=True)

    # Reorder Columns
    columns = [
        "VoteId",
        "Legislative",
        "FullName",
        "PartyAbbreviation",
        "SimplePartyAbbreviation",
        "SimplePartyId",
    ]
    columns.extend(full_votes.columns.drop(columns))
    return full_votes.loc[:, columns]


def get_votes(full_votes=None):
    """Returns votes Dataframe with the votation identifier as index,
    the council members as columns and the votes of the members as values.
    """

    if full_votes is None:
        full_votes = data_loading.full_votes()

    temp = pd.DataFrame(
        {
            "VoteId": full_votes["VoteId"],
            "VoteMeaning": full_votes["CouncillorYes"],
            "CouncillorId": full_votes["CouncillorId"],
        }
    )
    temp.loc[full_votes["CouncillorNo"] == 1, "VoteMeaning"] = 0
    temp.loc[full_votes["CouncillorAbstain"] == 1, "VoteMeaning"] = 2
    temp.loc[full_votes["CouncillorNotParticipated"] == 1, "VoteMeaning"] = 3
    temp.loc[full_votes["CouncillorExcused"] == 1, "VoteMeaning"] = 4
    temp.loc[full_votes["CouncillorPresident"] == 1, "VoteMeaning"] = 5

    votes = temp.groupby(["VoteId", "CouncillorId"]).aggregate("first").unstack()
    votes.columns = votes.columns.get_level_values(1)
    votes = votes.fillna(-1).astype(int)

    # Sort Columns
    votes = votes.loc[:, np.sort(votes.columns.values.astype("int")).astype(str)]
    return votes


if __name__ == "__main__":
    # clean all data if no arguments are passed
    if len(sys.argv) == 1:
        to_clean = [
            "councillor_info",
            "vote_data",
            "all_members",
            "members",
            "national_council_members",
            "full_votes",
            "votes",
            "votes_legislative",
        ]
    else:
        to_clean = sys.argv[1:]

    source_vote_data = None
    vote_data = None
    source_members = None
    councillor_info = None
    all_members = None
    members = None
    national_council_members = None
    full_votes = None
    votes = None

    print("starting data cleaning.")

    if "councillor_info" in to_clean:
        councillor_info = webscraping.councillor_info_df()
        data_loading.save_councillor_info(councillor_info)
        print("councillor_info done.")

    if "vote_data" in to_clean:
        source_vote_data = data_loading.source_vote_data()
        vote_data = get_vote_data(source_vote_data)
        data_loading.save_vote_data(vote_data)
        print("vote_data done.")

    if "all_members" in to_clean:
        source_members = data_loading.source_members()
        if councillor_info is None:
            councillor_info = data_loading.councillor_info()
        all_members = get_all_members(source_members, councillor_info)
        data_loading.save_all_members(all_members)
        print("all_members done.")

    if "members" in to_clean:
        if vote_data is None:
            vote_data = data_loading.vote_data()
        if all_members is None:
            all_members = data_loading.all_members()

        members = get_members(all_members, vote_data)
        data_loading.save_members(members)
        print("members done.")

    if "national_council_members" in to_clean:
        if members is None:
            members = data_loading.members()

        national_council_members = get_national_council_members(members)
        data_loading.save_national_council_members(national_council_members)
        print("national_council_members done.")

    if "full_votes" in to_clean:
        if vote_data is None:
            vote_data = data_loading.vote_data()
        if national_council_members is None:
            national_council_members = data_loading.national_council_members()

        full_votes = get_full_votes(vote_data, national_council_members)
        data_loading.save_full_votes(full_votes)
        print("full_votes done.")

    if "votes" in to_clean:
        if full_votes is None:
            full_votes = data_loading.full_votes()

        votes = get_votes(full_votes)
        data_loading.save_votes(votes)
        print("votes done.")

    if "votes_legislative" in to_clean:
        if full_votes is None:
            full_votes = data_loading.full_votes()

        votes_legislative = [get_votes(df) for df in util.split_legislative(full_votes)]
        for legislative, df in enumerate(votes_legislative):
            data_loading.save_votes_legislative(df, legislative=legislative)
        print("votes_legislative done.")
