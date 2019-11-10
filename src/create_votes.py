import data_loading
import pandas as pd


def create_votes(full_votes=None):
    if full_votes is None:
        full_votes = data_loading.full_votes()

    temp = pd.DataFrame(
        {
            "VoteMeaning": full_votes["CouncillorYes"],
            "CouncillorId": full_votes["CouncillorId"],
        }
    )
    temp.loc[full_votes["CouncillorNo"] == 1, "VoteMeaning"] = 0
    temp.loc[full_votes["CouncillorAbstain"] == 1, "VoteMeaning"] = 2
    temp.loc[full_votes["CouncillorNotParticipated"] == 1, "VoteMeaning"] = 3
    temp.loc[full_votes["CouncillorExcused"] == 1, "VoteMeaning"] = 4
    temp.loc[full_votes["CouncillorPresident"] == 1, "VoteMeaning"] = 5
    temp["Id"] = (
        full_votes["AffairShortId"].astype(str)
        + "-"
        + full_votes["VoteRegistrationNumber"].astype(str)
    )
    votes = temp.groupby(["Id", "CouncillorId"]).aggregate("first").unstack()
    votes.columns = votes.columns.get_level_values(0)
    votes = votes.fillna(-1).astype(int)
    return votes
