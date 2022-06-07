from csv import reader
from re import sub
from typing import List, Any

from config import LSD
from unsc_sentiment.corpus_utils import preprocess


def calc_sentiment_score(sentence: str, pol_words: List[Any]):
    """Calculate the sentiment score of a sentence.
    The score is in [-1,1] and score = (n_positive_words - n_negative_words) / n_words.

    Args
    ----
    sentence (str): The sentence.
    pol_words (list(tuple(str, str)) or list(str)): The words and their polarities or just polarites.

    Return
    ------
    float: The sentiment score.
    """
    neg = sum([1 for t in pol_words if "negative" in t]) 
    neg_neg = sum([1 for t in pol_words if "neg_negative" in t])
    pos = sum([1 for t in pol_words if "positive" in t])
    neg_pos = sum([1 for t in pol_words if "neg_positive" in t])
    pos = pos - neg_pos + neg_neg
    neg = neg - neg_neg + neg_pos
    score = pos - neg
    if score != 0:
        score = score / len(sentence.split())
    return score

def create_lex_entry(pattern: str):
    """Create an entry with meta info for the new LSD.

    Args
    ----
    pattern (str): The unprocessed entry.

    Return
    ------
    list: Containing the lexicon entry, the number of tokens, 0 or 1 (prefix or no prefix).
    """
    pattern = pattern.strip()
    tokens = pattern.split()
    is_prefix = False
    if pattern.endswith("*"):
        is_prefix = True
        pattern = sub('\*', '', pattern)
    return [pattern, len(tokens), int(is_prefix)]

def pretty_polarity(polarity: str):
    """Extract the polarity label.

    Args
    ----
    polarity (str): The label of the the unprocessed lsd file.

    Return
    ------
    str: The polarity without unnecessary characters.
    """
    polarity = polarity[1:].strip()
    if "#" in polarity:
        polarity = polarity.split("#")[0]
    return polarity

def find_sentiment_entries(sentence: str):
    """Get the sentiment words in a sentence.
    Check the words in the sentence that are contained in the sentiment dictionary.
    Return the sentence and the words and their polarity.
    The polarities are negative|positive|neg_negative|neg_positive.

    Args
    ----
    sentence (str): The sentence.

    Return
    ------
    str, list(tuple(str, str)): the sentence, the sentiment words and their polarity.
    """
    sentence = preprocess(sentence)
    sentence_seperated = sentence.split()
    out_entries = []
    with open(LSD, "r", encoding="utf-8") as lex:
        lex_reader = reader(lex, delimiter="\t")
        # skip header
        next(lex_reader, None)
        for entry in lex_reader:
            # lex entry is single token
            if entry[1] == "1":
                # lex entry is not a prefix
                if entry[2] == "0":
                    out_entries.extend([(entry[0], entry[3]) for t in sentence_seperated if entry[0] == t])
                else:
                    out_entries.extend([(entry[0], entry[3]) for t in sentence_seperated if t.startswith(entry[0])])
            else:
                out_entries.extend([(entry[0], entry[3]) for i in range((len(sentence.split(entry[0]))-1))])
    lex.close()    
    return sentence, out_entries