# Bachelorarbeit
# Sara Derakhshani
# Matrikelnummer: 792483
# Abgabe: 01.07.2022 

from csv import writer
import multiprocessing as mp
from os import path
import tqdm

from unsc_sentiment.corpus_utils import read_speech_file, preprocess
from unsc_sentiment.lsd_utils import calc_sentiment_score
from config import ANNOTATIONS_META, SPEECH_ANNOTATIONS

def annotate_speech(speech_meta: list):
    """Calculate the total sentiment score for a speech using the sentence sentiment scores.

    Args
    ----
    speech_path (list): speech id, path to speech, path to speech annotation

    Return
    ------
    None
    """
    # get file id
    filename = speech_meta[0]
    if filename.endswith(".txt"):
        filename = filename[0:-4]
    # get path to speech
    speech_filepath = speech_meta[1]
    # get out file path
    sentiment_filepath = speech_meta[2]
    # If speech has already been annotated get sentiment entries and calculate sentiment score
    if path.isfile(sentiment_filepath):
        speech = read_speech_file(speech_filepath)
        with open(sentiment_filepath, "r", encoding="utf-8") as speech_annotations_file:
            annotation_lines = speech_annotations_file.readlines()
            speech_annotations_file.close()
        polarities_in_speech = [line.strip().split("\t")[4] for line in annotation_lines[1:]]
        sentiment_score = calc_sentiment_score(preprocess(speech), polarities_in_speech)
        # Add new line to document level annotation file
        with open(SPEECH_ANNOTATIONS, "a", encoding="utf-8") as sentiment_per_speech_file:
            sps_writer = writer(sentiment_per_speech_file, delimiter='\t')
            sps_writer.writerow([filename, speech_filepath, sentiment_score, sentiment_filepath])
        sentiment_per_speech_file.close()

def main():
    if not path.isfile(SPEECH_ANNOTATIONS):
        print(f"\n Start document level annotation... \n")
        with open(SPEECH_ANNOTATIONS, "w", encoding="utf-8") as f:
            fwriter = writer(f, delimiter='\t')
            fwriter.writerow((
                "speech_id",
                "speech_path", 
                "sentimentScore", 
                "speech_annotation_path"))
            f.close()
        with open(ANNOTATIONS_META, "r", encoding="utf-8") as meta_file:
            meta_lines = meta_file.readlines()
            meta_file.close()
        speeches_meta = [line.strip().split("\t") for line in meta_lines[1:]]
        pool = mp.Pool(mp.cpu_count())
        for _ in tqdm.tqdm(pool.imap_unordered(annotate_speech, speeches_meta),total=len(speeches_meta)):
            pass
        print(f"\nFinished document level annotation. \n")
    else:
        print(f"\nSpeeches already annotated. Check {SPEECH_ANNOTATIONS}\n")

if __name__ == "__main__":
    main()
