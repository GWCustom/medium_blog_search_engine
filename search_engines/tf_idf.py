
import math 
from collections import Counter 
import pandas as pd

def compute_tf(text): 
    """Compute log-normalized TF for a given text (single document).""" 
    words = text.lower().split() 
    word_counts = Counter(words) 
    return {
        word: math.log(1 + count) for word, count in word_counts.items()
    }


def compute_idf(corpus):
    """Computes the IDF weights for all terms found in a corpus"""
    docs = corpus.split("\n")
    df = Counter(word for doc in docs for word in set(doc.lower().split()))
    return {word: math.log(len(docs) / df[word]) for word in df}


def compute_tfidf(word, document, idf_map):
    """Computes the TF-IDF score for a given word in a document."""
    tf = compute_tf(document)  # Compute TF for the document
    return tf.get(word, 0) * idf_map.get(word, 0)  # Multiply TF by IDF


def make_tfidf_table(articles, corpus):
    """Creates a TF-IDF table for all terms in a corpus."""

    idf_map = compute_idf(corpus)
    article_maps = []

    for article in articles:
        # Compute the term-frequency map for each article
        article_specific_tf_map = compute_tf(article)
        
        # Compute the TF-IDF score for each term in the corpus
        tfidf_scores = {
            word: compute_tfidf(word, article, idf_map) for word in corpus.split()
        }

        article_maps.append(tfidf_scores)

    return pd.DataFrame(article_maps)


def search(query, table):

    """Searches for a query in the TF-IDF table and returns the top match."""
    
    if not query.strip():
        return None  # Return None if the query is empty
    
    # Compute the corpus-wide importance for all terms
    scores = table.sum()

    # Compute the TF-IDF score for the query
    query_tf = compute_tf(query)
    query_tfidf = {
        word: query_tf.get(word, 0) * scores.get(word, 0)
        for word in query.split() if word in scores
    }

    if not query_tfidf:  # If no matching words found
        return None

    # Find the article with the highest TF-IDF score for the query and return the index
    return table[query_tfidf.keys()].sum(axis=1).nlargest(1).index[0]