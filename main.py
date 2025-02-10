from search_engines import tf_idf
from medium_scraper import get_articles
from PARAMS import BASE_URL, QUERY

import pandas as pd


def get_most_relevant_article_using_TFIDF(BASE_URL, search_query):

    # Now create a corpus from all the articles
    corpus = "\n".join(articles)

    # Create a TF-IDF table for all terms in the corpus
    table = tf_idf.make_tfidf_table(articles, corpus)

    # Search for the most relevant article, returned as an index.
    most_relevant_article = tf_idf.search(search_query, table)

    # Print the url link to the most relevant article
    return links[most_relevant_article]


if __name__ == "__main__":

    print("Retrieving articles from the blog found at: ", BASE_URL)
    articles, links = get_articles(BASE_URL)

    # Get the most relevant article based on the search query
    print(f"Searching for query term (TF-IDF): \n'{QUERY}':\n\n {get_most_relevant_article_using_TFIDF(BASE_URL, QUERY)}")

