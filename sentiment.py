# # Mateo Estrada
# # The following is from a tutorial from: https://realpython.com/python-nltk-sentiment-analysis/
# import string
# from collections import defaultdict
# import csv
# import pandas as pd
# import nltk
# from typing import List
# from pprint import pprint
# from nltk.sentiment import SentimentIntensityAnalyzer
#
# # I will use the following resources:
# ####################################
# # names: A list of common English names compiled by Mark Kantrowitz
# # stopwords: A list of really common words, like articles, pronouns, prepositions, and conjunctions
# # state_union: A sample of transcribed State of the Union addresses by different US presidents, compiled by Kathleen Ahrens
# # twitter_samples: A list of social media phrases posted to Twitter
# # movie_reviews: Two thousand movie reviews categorized by Bo Pang and Lillian Lee
# # averaged_perceptron_tagger: A data model that NLTK uses to categorize words into their part of speech
# # vader_lexicon: A scored list of words and jargon that NLTK references when performing sentiment analysis, created by C.J. Hutto and Eric Gilbert
# # punkt: A data model created by Jan Strunk that NLTK uses to split full texts into word lists
# ######################################
#
# #
# # nltk.download(
# #     [
# #         "names",
# #         "stopwords",
# #         "state_union",
# #         "twitter_samples",
# #         "movie_reviews",
# #         "averaged_perceptron_tagger",
# #         "vader_lexicon",
# #         "punkt",
# #         "shakespeare"
# #     ]
# # )
#
# # w = nltk.corpus.shakespeare.words()
#
# # Compiling data for the state of the union downloaded files:
# # str.isalpha makes sure that its only words and not punctuation marks
# words = [w for w in nltk.corpus.state_union.words() if w.isalpha()]
#
#
#
#
# # Stop words have a negative effect on analysis (a, the, that, etc)
# # make sure to specify the lanugage that the stop words are in.
# stopwords = nltk.corpus.stopwords.words("english")
#
# # Removing the stop words from the words
# # all stop words in stopwords are lowercase so the words in words have to be lowercase
# words = [w for w in words if w.lower() not in stopwords]
#
#
# # Another way to split raw text into individual words: tokenization
#
# #########################
# #
# # For the movie terminator 2
# #
# #########################
#
#
# # terminator = pd.read_csv('terminator2.csv', error_bad_lines=0)
# # print(terminator)
# # for now this is how accurate this will be:
# # reading text from a text file: help from this: https://stackoverflow.com/questions/8369219/how-to-read-a-text-file-into-a-string-variable-and-strip-newlines
#
# # if the file is empty run the one with the header
# # one else run the one that only appends movie data
# with open('csv/saw.csv', 'r') as f:
#     columns = defaultdict(list)
#     # reading the csv content
#     lines = f.read().replace('\n', '')
#
#     # getting the title of the film
#     title = ["Terminator 2: Judgement Day", "Iron Man", "Up", "Interstellar", "Por mis pistolas", "Saw"]
#     # Doing a rudimentary sentiment analysis
#     sia = SentimentIntensityAnalyzer()
#     dictionary_output = sia.polarity_scores(lines)
#     dictionary_output['title'] = title[5]
#
#     # print(dictionary_output)
#     with open('movie_data.csv', 'a') as output_csv:
#         fieldnames =['neg', 'neu', 'pos', 'compound', 'title']
#         writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerow(dictionary_output)
#
#     output_csv.close()
#
#
#
#     # using VADER
#     # tokentize words
#     # pprint(nltk.word_tokenize(lines), width=200, compact=True)
#
#
#     # Removing punctuation from the lines
#     lines = lines.translate(str.maketrans('', '', string.punctuation))  # removing the punctuation from the text
#
#     # making a list of words
#     movie_1_words: List[str] = nltk.word_tokenize(lines)
#
#     #  filtering stopwords from the lines
#     words = [w for w in movie_1_words if w.lower() not in stopwords]
#     fd = nltk.FreqDist(words)
#     # print(movie_1_words)
#     # fd.most_common(5)
#     # fd.tabulate(5)
