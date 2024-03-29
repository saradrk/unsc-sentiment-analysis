<!--- Bachelorarbeit, Sara Derakhshani, Matrikelnummer: 792483, Abgabe: 01.07.2022 --->
# Sentiment Analysis of UNSC Speeches

A lexicon-based sentiment analysis tool for the UN Security Council Debates.  

## Requirements
This project was developed with Python 3.8.

* Install **`requirements.txt`**
* Download [UNSC Debates](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/KGVSYH)
* * Choose "Original Format ZIP" download option
* * Recommendation: Move to **`data/`** directory
* * Unpack ZIP
* * Adjust path to **`speeches.tar`** in **`config.py`**
* Download [Lexicoder Sentiment Dictionary](http://www.snsoroka.com/data-lexicoder/)
* * Recommendation: Move to **`data/`** directory
* * Unpack ZIP
* * Adjust paths to **`LSD2015.lc3`** and **`LSD2015_NEG.lc3`** in **`config.py`**

## Usage
Run each script once in the following order: 
1. Preprocess LSD
```bash
python3 make_lsd.py
```  
2. Make sentence level annotations (takes a while)
```bash
python3 make_sentence_annotations.py
```  
3. Make document level annotations
```bash
python3 make_speech_annotations.py
```  

## Data Sources
Schoenfeld, Mirco; Eckhard, Steffen; Patz, Ronny; Meegdenburg, Hilde van; Pires, Antonio, 2019, "The UN Security Council Debates", https://doi.org/10.7910/DVN/KGVSYH, Harvard Dataverse, V5, UNF:6:zwZdSPbcmfAbjIiKdqzgig== [fileUNF]

Young, L. and Soroka, S. 2012. Lexicoder Sentiment Dictionary.
