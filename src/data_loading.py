"""Loads/saves data from 'data' and 'generated' folders.

    Usage:
    full_votes = data_loading.full_votes()
"""

import pandas as pd
import gzip
import numpy as np

DATA_FOLDER = "../data/"
GENERATED_FOLDER = "../generated/"


def _read_pickle(file_name, default_file_name, folder):
    if not file_name:
        file_name = default_file_name

    path = folder + file_name
    return pd.read_pickle(path)


def _save_pickle(df, file_name, default_file_name, folder):
    if not file_name:
        file_name = default_file_name

    path = folder + file_name
    df.to_pickle(path)


COUNCILLOR_INFO_FILE_NAME = "councillor_info.pickle"


def councillor_info(file_name=None):
    return _read_pickle(file_name, COUNCILLOR_INFO_FILE_NAME, GENERATED_FOLDER)


def save_councillor_info(df, file_name=None):
    _save_pickle(df, file_name, COUNCILLOR_INFO_FILE_NAME, GENERATED_FOLDER)


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
    "CouncillorId": np.str,
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
            yield [column.strip('"\n\ufeff') for column in columns]


def _load(file_name):
    """Loads gzipped file as dataframe"""
    rows = np.array(list(_read_file(file_name)))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


VOTE_DATA_FILE_NAME = "vote_data.pickle.gz"


def vote_data(file_name=None):
    return _read_pickle(file_name, VOTE_DATA_FILE_NAME, GENERATED_FOLDER)


def save_vote_data(df, file_name=None):
    _save_pickle(df, file_name, VOTE_DATA_FILE_NAME, GENERATED_FOLDER)


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


MEMBERS_FILE_NAME = "members.pickle"


def members(file_name=None):
    return _read_pickle(file_name, MEMBERS_FILE_NAME, GENERATED_FOLDER)


def save_members(members, file_name=None):
    _save_pickle(members, file_name, MEMBERS_FILE_NAME, GENERATED_FOLDER)


ALL_MEMBERS_FILE_NAME = "all_members.pickle"


def all_members(file_name=None):
    return _read_pickle(file_name, ALL_MEMBERS_FILE_NAME, GENERATED_FOLDER)


def save_all_members(df, file_name=None):
    _save_pickle(df, file_name, ALL_MEMBERS_FILE_NAME, GENERATED_FOLDER)


NATIONAL_COUNCIL_MEMBERS_FILE = "national_council_members.pickle"


def national_council_members(file_name=None):
    return _read_pickle(file_name, NATIONAL_COUNCIL_MEMBERS_FILE, GENERATED_FOLDER)


def save_national_council_members(national_council_members, file_name=None):
    _save_pickle(
        national_council_members,
        file_name,
        NATIONAL_COUNCIL_MEMBERS_FILE,
        GENERATED_FOLDER,
    )


FULL_VOTES_FILE_NAME = "full_votes.pickle.gz"


def full_votes(file_name=None):
    return _read_pickle(file_name, FULL_VOTES_FILE_NAME, GENERATED_FOLDER)


def save_full_votes(full_votes, file_name=None):
    _save_pickle(full_votes, file_name, FULL_VOTES_FILE_NAME, GENERATED_FOLDER)


VOTES_FILE_NAME = "votes.pickle.gz"


def votes(file_name=None):
    return _read_pickle(file_name, VOTES_FILE_NAME, GENERATED_FOLDER)


def save_votes(votes, file_name=None):
    _save_pickle(votes, file_name, VOTES_FILE_NAME, GENERATED_FOLDER)


VOTES_LEGISLATIVE_FILE_NAME = "votes_legislative"
VOTES_LEGISLATIVE_FILE_EXT = ".pickle.gz"


def votes_legislative(file_name=None):
    if not file_name:
        file_name = VOTES_LEGISLATIVE_FILE_NAME

    dfs = []
    for legislative in range(3):
        path = file_name + "_" + str(legislative) + VOTES_LEGISLATIVE_FILE_EXT
        dfs.append(votes(path))
    return dfs


def save_votes_legislative(votes, legislative, file_name=None):
    if not file_name:
        file_name = VOTES_LEGISLATIVE_FILE_NAME

    path = file_name + "_" + str(legislative) + VOTES_LEGISLATIVE_FILE_EXT
    save_votes(votes, path)
