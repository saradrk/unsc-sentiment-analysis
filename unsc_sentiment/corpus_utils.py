# Bachelorarbeit
# Sara Derakhshani
# Matrikelnummer: 792483
# Abgabe: 01.07.2022 

import csv
from re import sub, split
from typing import Any, List, Union

def get_debates_by_theme(theme: Union[str, List[str]], unsc_meta_path: str):
    """Get UNSC debate ids concerning the specified debate theme and return ids.

    Args
    ----
    theme (list): List of the debate themes.
    unsc_meta_path (str): Path to tsv file containing UNSC meta data.

    Return
    ------
    list of strings: List containing the debate ids.
    """
    debates = []
    themes = None
    if type(theme) == list:
        themes = [t.lower() for t in theme]
    else:
        theme = theme.lower()
    with open(unsc_meta_path, 'r', encoding='utf-8') as meta_file:
        meta_reader = csv.reader(meta_file, delimiter='\t')
        for row in meta_reader:
            speech_id = row[0]
            if themes:
                if row[3].lower() in themes:
                    debates.append(speech_id)
            else:
                if row[3].lower() == theme:
                    debates.append(speech_id)
    meta_file.close()
    return debates

def preprocess(text: str):
    """Remove punctuation, transform to lower case and remove newlines.
    
    Args
    ----
    text (str): The text to preprocess.
    """
    text = sub(r'[^\w\s]', '', text)
    text = sub('\n', ' ', text)
    return text.lower()

def read_speech_file(path: str):
    """Return speech as string.

    Args
    ----
    path (str): Path to speech.
    """
    speech_file = open(path, "r", encoding="utf-8")
    speech = speech_file.read()
    speech_file.close()
    return speech

def __remove_speaker(text: str):
    """Remove speaker and country from speech."""
    end_of_speaker = text.find(':')
    speech_start = end_of_speaker + 1
    speech = text[speech_start:]
    speech = speech.strip()
    return speech

# Stolen from https://github.com/glaserL/unsc-ne to have matching paragraph & sentence IDs
def __split_paragraphs(text: str):
    """Return a list of paragraph strings."""
    return [f"{p}." for p in split(r"\.\n{2,}", text)]

def structure_paragraphs_and_sentences(speech: str, model: Any):
    """Structure a speech into paragraphs and sentences.

    Args
    ----
    speech (str): The speech.
    model (spacy nlp): The loaded language model

    Return
    ------
    list of lists of strings: A list containing the sentences of each paragraph in a seperate list.
    """
    # remove speaker, merge new lines, and seperate paragraphs and sentences
    speech = __remove_speaker(speech)
    speech_paragraphs = __split_paragraphs(speech)
    speech_paragraphs_docs = [model(p) for p in speech_paragraphs]
    speech_paragraphs_sents = [d.sents for d in speech_paragraphs_docs]
    return [[sent.text for sent in sents] for sents in speech_paragraphs_sents]