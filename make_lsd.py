from csv import writer
from progress.bar import IncrementalBar

from unsc_sentiment.lsd_utils import pretty_polarity, create_lex_entry
from config import UNPROCESSED_LSD, UNPROCESSED_LSD_NEG, LSD


def main():
    polarity = None
    n_lsd_entries = sum([1 for n in open(UNPROCESSED_LSD, "r")])
    n_lsd_neg_entries = sum([1 for m in open(UNPROCESSED_LSD_NEG, "r")])
    total_n_entries = n_lsd_entries + n_lsd_neg_entries
    bar = IncrementalBar('Create lexicon', max = total_n_entries)
    with open(LSD, "w", encoding="utf-8") as out_f:
        out_writer = writer(out_f, delimiter='\t')
        out_writer.writerow(["lexEntry", "nrOfTokens", "isPrefix", "polarity"])
        with open(UNPROCESSED_LSD, "r", encoding="utf-8") as lex_f:
            for line in lex_f:
                bar.next()
                if line.startswith("+"):
                    polarity = pretty_polarity(line)
                    continue
                elif "unite" in line:
                    continue
                new_entry = create_lex_entry(line)
                new_entry.append(polarity)
                out_writer.writerow(new_entry)
        lex_f.close()
        with open(UNPROCESSED_LSD_NEG, "r", encoding="utf-8") as lex_neg_f:
            for line in lex_neg_f:
                bar.next()
                if line.startswith("+"):
                    polarity = pretty_polarity(line)
                    continue
                elif "unite" in line:
                    continue
                new_entry = create_lex_entry(line)
                new_entry.append(polarity)
                out_writer.writerow(new_entry)
        lex_neg_f.close()
    out_f.close()
    bar.finish()

if __name__ == "__main__":
    main()