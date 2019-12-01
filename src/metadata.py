"""Collection of metadata for votes/member/party information"""
import datetime
from collections import defaultdict
import numpy as np


# Dictionary of party abbreviation in any language to abbreviation in French
ALL_PARTY_ABBREVIATION = {
    "PRD": "PLR",
    "PLR": "PLR",
    "UDC": "UDC",
    "PSS": "PSS",
    "PEV": "PEV",
    "PDC": "PDC",
    "BastA": "BastA",
    "PES": "PES",
    "pvl": "PVL",
    "PLS": "PLR",
    "Lega": "Lega",
    "CVPO": "CSPO",
    "UDF": "UDF",
    "PBD": "PBD",
    "PdT": "PdT",
    "CSPO": "CSPO",
    "PLD": "PLR",
    "PCS": "PCS",
    "GB": "AVeS",
    "MCR": "MCR",
    "MCG": "MCG",
    "DS": "DS",
    "Al": "AVZ",
    "-": "-",
    "AdG": "AdG",
    "csp-ow": "CSP OW",
    "nan": "-",
}

POPULAR_PARTIES = [
    "UDC",
    "PSS",
    "PLR",
    "PDC",
    "PBD",
    "PES",
    "PVL",
    "PEV",
    "Lega",
    "PCS",
    "UDF",
]

# Dictionary that maps party abbrevations to a reduced set of parties (popular parties)
# Any other party is labelled as 'other'.
SIMPLE_PARTY_ABBREVIATION = defaultdict(lambda: "other")
SIMPLE_PARTY_ABBREVIATION.update({p: p for p in POPULAR_PARTIES})
# Merge some parties together
# TODO: Maybe there are some others to merge?
SIMPLE_PARTY_ABBREVIATION.update({"CSP OW": "PCS", "CSPO": "PCS"})

# Maps party abbreviation to party color
PARTY_COLOR = {
    "other": "#DDDDDD",
    "UDC": "#009F4F",
    "PSS": "#E53136",
    "PLR": "#0E52A0",
    "PDC": "#EF7D00",
    "PBD": "#FBD918",
    "PES": "#84B414",
    "PVL": "#A6CF42",
    "PEV": "#EFDA18",
    "Lega": "#6495ED",
    "PCS": "#0F95A7",
    "MCG": "#FEE801",
    "UDF": "#C71585",
    # "PST": "#E93C1A",
    # "PCS OW": "#BF3235",
    # "AL": "#960018",
}

# Maps simple party abbreviations to an index
SIMPLE_PARTY_TO_INDEX = {
    "other": 0,
    "UDC": 1,
    "PSS": 2,
    "PLR": 3,
    "PDC": 4,
    "PBD": 5,
    "PES": 6,
    "PVL": 7,
    "PEV": 8,
    "Lega": 9,
    "PCS": 10,
    "UDF": 11,
}

# Maps simple party index to a party name
SIMPLE_PARTY_FROM_INDEX = {i: p for p, i in SIMPLE_PARTY_TO_INDEX.items()}


# Stores ending dates of legislatures
# Note that the start date is always the day following the ending date
LEGISLATIVE_DATES = [
    datetime.date(2007, 12, 2),
    datetime.date(2011, 12, 4),
    datetime.date(2015, 11, 29),
    datetime.date(2019, 12, 1),
]


def legislative(date):
    """Returns the legislative from a date.

    Legislatures are mapped as follows:
        - 2007-2011: 0
        - 2011-2015: 1
        - 2015-2019: 2
        - other: nan
    """
    for i, (start, end) in enumerate(
        zip(LEGISLATIVE_DATES[:-1], LEGISLATIVE_DATES[1:])
    ):
        if (date > start) and (date <= end):
            return i


def full_names(members):
    """Returns 'LastName FirstName' of members Dataframe."""
    return members["LastName"] + " " + members["FirstName"]
