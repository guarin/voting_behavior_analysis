from sklearn.impute import SimpleImputer
import numpy as np


def yesno_imputed(leg):
    """
    Outputs df with 0 for votes 'no', 1 for votes 'yes' and 
    mean imputation for all other votes.
    """
    yesno = leg.copy()
    yesno[yesno > 1] = np.NaN
    yesno[yesno < 0] = np.NaN
    imp = SimpleImputer(missing_values=np.nan, strategy="mean")
    return imp.fit_transform(yesno.T).T


def get_politician_attendance(leg):
    """
    For every politician in legislature gets the number of times they weren't in 
    parliament during the vote.
    """
    n_votes = leg.shape[0]
    return ((leg <= 3).sum(axis=0) - (leg < 0).sum(axis=0)) / n_votes


def filter_lazy(leg, ncm, thresh):
    """
    Removes all politicians in legislature that were present in less than thresh 
    percent of the votes.
    """
    att = get_politician_attendance(leg).to_numpy()
    #    print(att)
    #    print(ncm)
    #    print(att>thresh)
    return leg.loc[:, att > thresh], ncm.loc[att > thresh, :]


def filter_impute(leg, ncm, thresh=0.5):
    """
    Filters politicians that aren't there often, and imputes then with the mean.
    """
    no_lazy, ncm = filter_lazy(leg, ncm, thresh)
    return yesno_imputed(no_lazy), ncm.reset_index(drop=True)
