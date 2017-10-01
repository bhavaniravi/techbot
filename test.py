import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

# word stemmer
stemmer = LancasterStemmer()
# 3 classes of training data
training_data = []
training_data.append({"class": "intro", "sentence": "Who are you?"})
training_data.append({"class": "intro", "sentence": "Hi"})
training_data.append({"class": "intro", "sentence": "what do you do?"})
training_data.append({"class": "intro", "sentence": "what can you do for me?"})
training_data.append({"class": "greet", "sentence": "Hey"})
training_data.append({"class": "greet", "sentence": "howdy"})
training_data.append({"class": "greet", "sentence": "hey there"})
training_data.append({"class": "greet", "sentence": "hello"})
training_data.append({"class": "affirm", "sentence": "yes"})
training_data.append({"class": "affirm", "sentence": "Yeah"})
training_data.append({"class": "affirm", "sentence": "that\'s right"})
training_data.append({"class": "goodbye", "sentence": "Bye"})
training_data.append({"class": "goodbye", "sentence": "goodbye"})
print("%s sentences in training data" % len(training_data))
# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    class_words[c] = []

for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a few things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            class_words[data['class']].extend([stemmed_word])

# we now have each word and the number of occurances of the word in our training corpus (the word's commonality)
print("Corpus words and counts: %s" % corpus_words)
# also we have all words in each class
print("Class words: %s" % class_words)
# we can now calculate the Naive Bayes score for a new sentence
sentence = "Hi"


# calculate a score for a given class
def calculate_class_score(sentence, class_name):
    score = 0
    for word in nltk.word_tokenize(sentence):
        if word in class_words[class_name]:
            score += 1
    return score


# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s" % (c, calculate_class_score(sentence, c)))
# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name):
    score = 0
    for word in nltk.word_tokenize(sentence):
        if word in class_words[class_name]:
            score += (1 / corpus_words[word])
    return score


# now we can find the class with the highest score
for c in class_words.keys():
    print ("Class: %s  Score: %s" % (c, calculate_class_score_commonality(sentence, c)))
# return the class with highest score for sentence
def find_class(sentence):
    high_class = None
    high_score = 0
    for c in class_words.keys():
        score = calculate_class_score_commonality(sentence, c)
        if score > high_score:
            high_class = c
            high_score = score
    return high_class, high_score


print(find_class("Hi"))
