# Spam-Filtering-using-IR-techniques
Spam Filtering is a project in which URLs can be filtered using Information Retrieval techniques.


## Project Overview:

An IR system that detects if the url is 'benign' or 'defacement' or 'phishing' or 'malware' when the user enters the terms present in his url. The top 5 predictions are ranked according to their score.

## Prerequisites

1. Make sure you have Python installed on your system.
2. nltk libraries installed
3. And all the basic python libraries installed

## Running the code:
1. Open the respective directory in the terminal
2. Run the source file using the command: "python source_code.py"
3. Enter the suspicious terms present in your url in the UI search bar to detect if the    url is 'benign' or 'defacement' or 'phishing' or 'malware'.
4. The top 5 predictions are then listed below.
5. Enter the Relevant ids in the relevance feedback section for better retrieval.

## File Structure:
-> source_code.py: The main script containing the Tkinter GUI and the Information Retrieval System logic.
-> inverted_index_with_urls.json: JSON file containing the inverted index with URLs.
-> document_contents.json: JSON file containing the content of each document.
-> Indexing.py: Script used for indexing the urls and producing the inverted_index_with_urls.json file.
->csvToJ.py: Script to convert the dataset from csv format to json format which is stored in document_contents.json file.
-> dataset.csv: Contains the dataset for the project.
