"""Loads/saves data from 'data' and 'generated' folders.

    Usage:
    full_votes = data_loading.full_votes()
"""

import pandas as pd
import datetime as dt
import gzip
import numpy as np


DATA_FOLDER = "../data/"
GENERATED_FOLDER = "../generated/"


SOURCE_VOTE_DATA_DTYPES = {
    "AffairShortId": np.int,
    "AffairTitle": np.str,
    "VoteRegistrationNumber": np.int,
    "VoteDate": np.str,
    "VoteMeaningYes": np.str,
    "VoteMeaningNo": np.str,
    "DivisionText": np.str,
    "VoteSubmissionText": np.str,
    "VoteFilteredYes": np.uint8,
    "VoteFilteredNo": np.uint8,
    "VoteFilteredAbstain": np.uint8,
    "VoteFilteredNotParticipated": np.uint8,
    "VoteFilteredExcused": np.uint8,
    "VoteFilteredPresident": np.uint8,
    "CouncillorId": np.int,
    "CouncillorName": np.str,
    "CouncillorYes": np.uint0,
    "CouncillorNo": np.uint0,
    "CouncillorAbstain": np.uint0,
    "CouncillorNotParticipated": np.uint0,
    "CouncillorExcused": np.uint0,
    "CouncillorPresident": np.uint0,
}

SOURCE_VOTE_DATA_DATE_FORMAT = "%a %b %d %Y %H:%M:%S %Z"


def source_vote_data():
    """Get the votes data between 2007 and 2019 from gzip files as a dataframe"""
    dfs = []
    for year in range(2007, 2020):
        dfs.append(_load(str(year)))
    df = pd.concat(dfs, ignore_index=True, copy=False).astype(SOURCE_VOTE_DATA_DTYPES)
    return df


def _read_file(file_name):
    """Iterator over rows in gzipped file"""
    path = DATA_FOLDER + file_name + ".csv.gz"
    with gzip.open(path, "rt") as file:
        for line in file:
            columns = line.split('","')
            yield [column.strip(u'"\n\ufeff') for column in columns]


def _load(file_name):
    """Loads gzipped file as dataframe"""
    rows = np.array(list(_read_file(file_name)))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


VOTE_DATA_DTYPES = {
    "AffairShortId": np.int,
    "AffairTitle": np.str,
    "VoteRegistrationNumber": np.int,
    "VoteMeaningYes": np.str,
    "VoteMeaningNo": np.str,
    "DivisionText": np.str,
    "VoteSubmissionText": np.str,
    "VoteFilteredYes": np.uint8,
    "VoteFilteredNo": np.uint8,
    "VoteFilteredAbstain": np.uint8,
    "VoteFilteredNotParticipated": np.uint8,
    "VoteFilteredExcused": np.uint8,
    "VoteFilteredPresident": np.uint8,
    "CouncillorId": np.int,
    "CouncillorName": np.str,
    "CouncillorYes": np.uint0,
    "CouncillorNo": np.uint0,
    "CouncillorAbstain": np.uint0,
    "CouncillorNotParticipated": np.uint0,
    "CouncillorExcused": np.uint0,
    "CouncillorPresident": np.uint0,
}

VOTE_DATA_DATE_COLUMNS = ["VoteDate"]
VOTE_DATA_FILE_NAME = "vote_data.csv.gz"


def vote_data(file_name=None):
    if not file_name:
        file_name = VOTE_DATA_FILE_NAME

    path = GENERATED_FOLDER + file_name
    df = pd.read_csv(
        path,
        dtype=VOTE_DATA_DTYPES,
        parse_dates=VOTE_DATA_DATE_COLUMNS,
        date_parser=dt.datetime.fromisoformat,
    )
    return df


def save_vote_data(df, file_name=None):
    if not file_name:
        file_name = VOTE_DATA_FILE_NAME

    path = GENERATED_FOLDER + file_name
    df.to_csv(path, index=False)


SOURCE_MEMBERS_DTYPES = {
    "Active": np.bool,
    "FirstName": np.str,
    "LastName": np.str,
    "GenderAsString": np.str,
    "CantonName": np.str,
    "CantonAbbreviation": np.str,
    "CouncilName": np.str,
    "ParlGroupName": np.str,
    "ParlGroupAbbreviation": np.str,
    "PartyName": np.str,
    "PartyAbbreviation": np.str,
    "MaritalStatusText": np.str,
    "BirthPlace_City": np.str,
    "BirthPlace_Canton": np.str,
    "Mandates": np.str,
    "Citizenship": np.str,
    "CouncillorName": np.str,
}

SOURCE_MEMBERS_DATE_COLUMNS = [
    "DateJoining",
    "DateLeaving",
    "DateOfBirth",
    "DateOfDeath",
]
SOURCE_MEMBERS_DATE_FORMAT = "%M/%d/%Y"
SOURCE_MEMBERS_FILE_NAME = "Ratsmitglieder_1848_EN.xlsx"


def source_members(file_name=None):
    if not file_name:
        file_name = SOURCE_MEMBERS_FILE_NAME

    path = DATA_FOLDER + file_name
    df = pd.read_excel(
        path,
        dtype=SOURCE_MEMBERS_DTYPES,
        parse_dates=SOURCE_MEMBERS_DATE_COLUMNS,
        date_format=SOURCE_MEMBERS_DATE_FORMAT,
    )
    for column in SOURCE_MEMBERS_DATE_COLUMNS:
        df[column] = df[column].dt.date
    return df


MEMBERS_DTYPES = SOURCE_MEMBERS_DTYPES
MEMBERS_DATE_COLUMNS = ["DateJoining", "DateLeaving", "DateOfBirth", "DateOfDeath"]
MEMBERS_FILE_NAME = "members.csv"
NATIONAL_COUNCIL_MEMBERS_FILE = "national_council_members.csv"


def _read_members_like(file_name):
    df = pd.read_csv(GENERATED_FOLDER + file_name, parse_dates=MEMBERS_DATE_COLUMNS)
    for column in MEMBERS_DATE_COLUMNS:
        df[column] = df[column].dt.date
    return df


def members(file_name=None):
    if not file_name:
        file_name = MEMBERS_FILE_NAME

    return _read_members_like(file_name)


def save_members(members, file_name=None):
    if not file_name:
        file_name = MEMBERS_FILE_NAME

    path = GENERATED_FOLDER + file_name
    members.to_csv(path, index=False)


def national_council_members(file_name=None):
    if not file_name:
        file_name = NATIONAL_COUNCIL_MEMBERS_FILE

    return _read_members_like(file_name)


def save_national_council_members(national_council_members, file_name=None):
    if not file_name:
        file_name = NATIONAL_COUNCIL_MEMBERS_FILE

    path = GENERATED_FOLDER + file_name
    national_council_members.to_csv(path, index=False)


FULL_VOTES_DTYPES = {
    "Active": np.bool,
    "AffairShortId": np.int64,
    "AffairTitle": np.str,
    "BirthPlace_Canton": np.str,
    "BirthPlace_City": np.str,
    "CantonAbbreviation": np.str,
    "CantonName": np.str,
    "Citizenship": np.str,
    "CouncilName": np.str,
    "CouncillorAbstain": np.uint0,
    "CouncillorExcused": np.uint0,
    "CouncillorId": np.int64,
    "CouncillorName": np.str,
    "CouncillorNo": np.uint0,
    "CouncillorNotParticipated": np.uint0,
    "CouncillorPresident": np.uint0,
    "CouncillorYes": np.uint0,
    "DivisionText": np.str,
    "FirstName": np.str,
    "GenderAsString": np.str,
    "LastName": np.str,
    "Mandates": np.str,
    "MaritalStatusText": np.str,
    "ParlGroupAbbreviation": np.str,
    "ParlGroupName": np.str,
    "PartyAbbreviation": np.str,
    "PartyName": np.str,
    "VoteFilteredAbstain": np.uint8,
    "VoteFilteredExcused": np.uint8,
    "VoteFilteredNo": np.uint8,
    "VoteFilteredNotParticipated": np.uint8,
    "VoteFilteredPresident": np.uint8,
    "VoteFilteredYes": np.uint8,
    "VoteMeaningNo": np.str,
    "VoteMeaningYes": np.str,
    "VoteRegistrationNumber": np.int64,
    "VoteSubmissionText": np.str,
}

FULL_VOTES_DATE_COLUMNS = [
    "VoteDate",
    "DateJoining",
    "DateLeaving",
    "DateOfBirth",
    "DateOfDeath",
]

FULL_VOTES_FILE_NAME = "full_votes.csv.gz"


def full_votes(file_name=None):
    if not file_name:
        file_name = FULL_VOTES_FILE_NAME

    path = GENERATED_FOLDER + file_name
    df = pd.read_csv(path, dtype=FULL_VOTES_DTYPES, parse_dates=FULL_VOTES_DATE_COLUMNS)
    date_columns = [
        column for column in FULL_VOTES_DATE_COLUMNS if column != "VoteDate"
    ]
    for column in date_columns:
        df[column] = df[column].dt.date
    return df


def save_full_votes(full_votes, file_name=None):
    if not file_name:
        file_name = FULL_VOTES_FILE_NAME

    path = GENERATED_FOLDER + file_name
    full_votes.to_csv(path, index=False)


VOTES_FILE_NAME = "votes.csv.gz"


def votes(file_name=None):
    if not file_name:
        file_name = VOTES_FILE_NAME

    path = GENERATED_FOLDER + file_name
    return pd.read_csv(path, index_col="Id")


def save_votes(votes, file_name=None):
    if not file_name:
        file_name = VOTES_FILE_NAME

    path = GENERATED_FOLDER + file_name
    votes.to_csv(path)
