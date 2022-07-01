# Bachelorarbeit
# Sara Derakhshani
# Matrikelnummer: 792483
# Abgabe: 01.07.2022 

from csv import writer
import multiprocessing as mp
from os import listdir, makedirs, path
import spacy
import tarfile
import tqdm

from unsc_sentiment.corpus_utils import read_speech_file, structure_paragraphs_and_sentences
from unsc_sentiment.lsd_utils import calc_sentiment_score, find_sentiment_entries
from config import ANNOTATIONS_DIR, SENTENCE_ANNOTATIONS, ANNOTATIONS_META, SPEECHES_DIR, SPEECHES_TAR

nlp = spacy.load("en_core_web_sm")

def annotate(speech_path: str):
    """Sentiment annotate a speech and save an annotation tsv file.
    Save each token that has sentiment with the paragraph index, paragraph sentence index, total sentence index
    token form of the sentiment lexicon token, sentiment polarity.

    Args
    ----
    speech_path (str): Path to the speech txt file.

    Return
    ------
    None
    """
    # get file id
    filename = path.split(speech_path)[1]
    # create sentiment filename
    sentiment_filename = "".join((path.splitext(filename)[0], "_sentiment.tsv"))
    # get out file path
    sentiment_filepath = path.join(ANNOTATIONS_DIR, sentiment_filename)
    # stop if speech has already been annotated
    if path.isfile(sentiment_filepath):
        return None
    with open(ANNOTATIONS_META, "a", encoding="utf-8") as meta_file:
        meta_writer = writer(meta_file, delimiter='\t')
        meta_writer.writerow([filename, speech_path, sentiment_filepath])
        meta_file.close()
    speech = structure_paragraphs_and_sentences(read_speech_file(speech_path), nlp)
    # Iterate each sentence in each paragraph
    with open(sentiment_filepath, "w", encoding="utf-8") as speech_annotations_file:
        sa_writer = writer(speech_annotations_file, delimiter='\t')
        # write header
        sa_writer.writerow(["paragraphIndex", "paragraphSentenceIndex", "totalSentenceIndex", "tokenLexForm", "tokenSentiment"])
        paragraph_index = -1
        total_sentence_index = -1
        for paragraph in speech:
            paragraph_index  += 1
            sentence_index = -1
            for sentence in paragraph:
                sentence_index  += 1
                total_sentence_index += 1
                # preprocess sentence, match LSD entries, calc sentiment score and 
                # make entry to sentence level annotation file
                preprocessed_sentence, sentiment_entries = find_sentiment_entries(sentence)
                with open(SENTENCE_ANNOTATIONS, "a", encoding="utf-8") as corpus_annotations_file:
                    ca_writer = writer(corpus_annotations_file, delimiter='\t')
                    ca_writer.writerow([speech_path,
                        paragraph_index,
                        sentence_index,
                        total_sentence_index,
                        sentence,
                        calc_sentiment_score(preprocessed_sentence, sentiment_entries)])
                    corpus_annotations_file.close()
                # make entry to annotation file of the speech for each matched LSD entry
                for entry in sentiment_entries:
                    out_entry = [paragraph_index, sentence_index, total_sentence_index]
                    out_entry.extend(entry)
                    sa_writer.writerow(out_entry)
    speech_annotations_file.close()


def main():
    if not path.isdir(SPEECHES_DIR):
        makedirs(SPEECHES_DIR)
    if len(listdir(SPEECHES_DIR)) < 1:
        print(f"\nStart extracting {SPEECHES_TAR}... \n")
        with tarfile.open(SPEECHES_TAR) as tar:
            for member in tqdm.tqdm(iterable=tar.getmembers(), total=len(tar.getmembers())):
                tar.extract(member=member, path=SPEECHES_DIR)
        print(f"\nFinished extracting speeches to {SPEECHES_DIR}. \n")
    if not path.isdir(ANNOTATIONS_DIR):
        makedirs(ANNOTATIONS_DIR)
    if not path.isfile(SENTENCE_ANNOTATIONS):
        print(f"Start sentence level annotation... \n")
        with open(SENTENCE_ANNOTATIONS, "w", encoding="utf-8") as f:
            fwriter = writer(f, delimiter='\t')
            fwriter.writerow((
                "speech_path", 
                "paragraphIndex", 
                "paragraphSentenceIndex", 
                "totalSentenceIndex", 
                "sentenceText", 
                "sentimentScore"))
            f.close()
        with open(ANNOTATIONS_META, "w", encoding="utf-8") as f:
            fwriter = writer(f, delimiter='\t')
            fwriter.writerow(("speech_id", "path_to_speech", "path_to_speech_annotation"))
            f.close()
        corpus_files = [f"{SPEECHES_DIR}{filename}" for filename in listdir(SPEECHES_DIR)]
        pool = mp.Pool(mp.cpu_count())
        for _ in tqdm.tqdm(pool.imap_unordered(annotate, corpus_files), total=len(listdir(SPEECHES_DIR))):
            pass
        print(f"\nFinished sentence level annotation. \n")
    else:
        print(f"\nSentences already annotated. Check {SENTENCE_ANNOTATIONS} \n")

if __name__ == "__main__":
    main()