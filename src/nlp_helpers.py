import numpy as np
import itertools
import pandas as pd
import spacy
from spacy.lang.fr.examples import sentences 
nlp = spacy.load('fr_core_news_sm')


def get_affair_title(full_votes, l):
    unique = full_votes.drop_duplicates("VoteId")
    joined = unique.join(l, 'VoteId', how='right')[["AffairTitle", "VoteId"]]
    sort = joined.sort_values('VoteId')
    return sort.set_index('VoteId')

def get_title_nouns(titles):
    """Obtains all nouns within the titles."""
    def inner(t):
        l = []
        doc = nlp(t)
        for token in doc:
            if token.pos_=='NOUN':
                l.append(token.text.lower())
        return l
    
    return titles['AffairTitle'].map(inner)

def word_dict(series):
    """Flattens Series of lists of words into a np array of the unique words.
    Then creates dictionary of word to a unique, increasing integer with values
    in increasing alphabetical order."""
    keys = np.unique(np.array(list(itertools.chain(*list(series)))))
    out = dict()
    for val, key in enumerate(keys):
        out[key] = val
    return out

def get_count_matrix(title_nouns, word_dict):
    """For every noun counts occurrences in every individual title"""
    out = np.zeros((len(title_nouns), len(word_dict)), dtype=int)
    for i, title in enumerate(title_nouns):
        for noun in title:
            out[i, word_dict[noun]] += 1
    return pd.DataFrame(out, index=title_nouns.index, columns=list(word_dict.keys()))

def handle_plural(count_matrix):
    """For all columns who end with s or x, if the word without s or x is also in the
    data, sum the two counts"""
    names = np.array(count_matrix.columns)
    
    # Identify those that end with s or x
    last = np.array([x[-1] for x in names])
    dangerous_ending = np.logical_or(last=='s', last=='x')
    
    # Identify those that when removing the last character are equal to the previous
    stripped = np.array([x[:-1] for x in names])
    similar = np.equal(stripped[1:], names[:-1])
    similar = np.array([False, *similar], dtype=bool) # Handle first word which is always False

    # Remove those that satisfy both
    remove = np.logical_and(similar, dangerous_ending)
    
    # Add the removed column to the one before
    where_to_add = np.array([*remove[1:], False], dtype=bool)
    
    mat = count_matrix.to_numpy()
    mat[:,where_to_add] += mat[:,remove]
    #count_matrix.loc[:,where_to_add] = count_matrix.loc[:,remove].add(count_matrix.loc[:,where_to_add])
    
    keep = np.logical_not(remove)
    out_df = pd.DataFrame(mat[:,keep], index=count_matrix.index, columns=names[keep])
    
    return out_df

def get_reduced_count(count_matrix, min_count=5):
    """Removes all words present less than min_count"""
    keep = count_matrix.sum(axis=0) >= min_count    
    return count_matrix.loc[:,keep]

def get_idf(count):
    return np.log(count.shape[1] / count.sum(axis=0))
