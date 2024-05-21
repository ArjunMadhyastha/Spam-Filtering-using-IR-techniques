import re
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import Label, Entry, Button, Text, Scrollbar, END, Listbox

# Download NLTK resources (uncomment the following two lines if not downloaded)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class InformationRetrievalUI:
    def __init__(self, master):
        self.master = master
        master.title("Information Retrieval System")
        self.preprocessed_query = ""
        self.selected_doc_id = None

        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self.master, text="Enter the terms present in url to detect:")
        self.label.pack()

        self.entry = Entry(self.master, width=50)
        self.entry.pack()

        self.search_button = Button(self.master, text="Search", command=self.search)
        self.search_button.pack()

        self.result_text = Text(self.master, wrap="word", height=20, width=80)
        self.result_text.pack()

        self.scrollbar = Scrollbar(self.master, command=self.result_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        self.listbox_label = Label(self.master, text="Retrieved Documents:")
        self.listbox_label.pack()

        self.listbox = Listbox(self.master, selectmode=tk.SINGLE, width=80, height=5)
        self.listbox.pack()

        self.listbox_scrollbar = Scrollbar(self.master, command=self.listbox.yview)
        self.listbox_scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.listbox_scrollbar.set)

        self.feedback_label = Label(self.master, text="Relevance Feedback (comma-separated list of relevant document IDs):")
        self.feedback_label.pack()

        self.feedback_entry = Entry(self.master, width=50)
        self.feedback_entry.pack()

        self.feedback_button = Button(self.master, text="Submit Feedback", command=self.submit_feedback)
        self.feedback_button.pack()

        self.view_button = Button(self.master, text="View Document", command=self.view_document)
        self.view_button.pack()

    def preprocess_query(self, query):
        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()
        lemmatizer = WordNetLemmatizer()

        tokens = word_tokenize(query)
        tokens = [token.lower() for token in tokens]
        tokens = [re.sub(r'[^a-zA-Z0-9]', '', token) for token in tokens]
        tokens = [token for token in tokens if token not in stop_words]
        tokens = [ps.stem(token) for token in tokens]
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        self.preprocessed_query = ' '.join(tokens)

    def search(self):
        user_query = self.entry.get()
        self.preprocess_query(user_query)

        vectorizer = TfidfVectorizer()
        query_vector = vectorizer.fit_transform([self.preprocessed_query])

        similarity_scores = {}
        for term in self.preprocessed_query.split():
            if term in inverted_index:
                for doc_info in inverted_index[term]:
                    doc_id = doc_info.get('Document_ID')
                    tfidf_score = doc_info.get('TF-IDF_Score')

                    if doc_id is not None and tfidf_score is not None:
                        if doc_id not in similarity_scores:
                            similarity_scores[doc_id] = 0
                        similarity_scores[doc_id] += tfidf_score * cosine_similarity(query_vector, vectorizer.transform([term]))[0, 0]

        sorted_documents = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        result_str = ""
        doc_ids = []
        for rank, (doc_id, score) in enumerate(sorted_documents[:5], start=1):
            content = document_contents.get(str(doc_id), "Content not available")
            result_str += f"Rank {rank}: Document {doc_id}, Similarity Score: {score}\n"
            result_str += f"Content: {content}\n{'='*50}\n"
            doc_ids.append(doc_id)

        self.result_text.delete(1.0, END)
        self.result_text.insert(END, result_str)

        self.listbox.delete(0, END)
        for doc_id in doc_ids:
            self.listbox.insert(END, doc_id)

    def submit_feedback(self):
        feedback = self.feedback_entry.get()
        relevant_docs = set(feedback.split(','))

        vectorizer = TfidfVectorizer()
        query_vector_original = vectorizer.fit_transform([self.preprocessed_query])

        query_vector = query_vector_original.copy()

        for doc_id_score_list in inverted_index.values():
            for doc_info in doc_id_score_list:
                doc_id = doc_info.get('Document_ID')
                if doc_id is not None:
                    numeric_doc_id = int(''.join(filter(str.isdigit, doc_id)))
                    if numeric_doc_id in relevant_docs:
                        feedback_vector = vectorizer.transform([document_contents[str(numeric_doc_id)]])
                        query_vector += feedback_vector

                        updated_content = retrieve_content_by_id(numeric_doc_id)
                        document_contents[str(numeric_doc_id)] = updated_content

        updated_similarity_scores = {}
        for term in self.preprocessed_query.split():
            if term in inverted_index:
                for doc_info in inverted_index[term]:
                    doc_id = doc_info.get('Document_ID')
                    tfidf_score = doc_info.get('TF-IDF_Score')

                    if doc_id is not None and tfidf_score is not None:
                        numeric_doc_id = int(''.join(filter(str.isdigit, doc_id)))
                        if numeric_doc_id not in updated_similarity_scores:
                            updated_similarity_scores[numeric_doc_id] = 0
                        updated_similarity_scores[numeric_doc_id] += tfidf_score * cosine_similarity(query_vector, vectorizer.transform([term]))[0, 0]

        updated_sorted_documents = sorted(updated_similarity_scores.items(), key=lambda x: x[1], reverse=True)

        result_str = "\nTop-ranked documents with relevance feedback:\n"
        for rank, (doc_id, score) in enumerate(updated_sorted_documents[:5], start=1):
            content = document_contents.get(str(doc_id), "Content not available")
            result_str += f"Rank {rank}: Document {doc_id}, Similarity Score: {score}\n"
            result_str += f"Content: {content}\n{'='*50}\n"

        self.result_text.insert(END, result_str)

    def view_document(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.selected_doc_id = self.listbox.get(selected_index[0])
            content = document_contents.get(str(self.selected_doc_id), "Content not available")
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, f"Content of Document {self.selected_doc_id}:\n{content}")

# Load the inverted index and document contents from the saved JSON files
with open('inverted_index_with_urls.json', 'r') as json_file:
    inverted_index = json.load(json_file)

with open('document_contents.json', 'r') as json_file:
    document_contents = json.load(json_file)

# Create and run the Tkinter GUI
root = tk.Tk()
app = InformationRetrievalUI(root)
root.mainloop()
