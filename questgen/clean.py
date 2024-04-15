import nltk
import re
import string
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

nltk.download('stopwords')
punctuation = string.punctuation
stop_words = nltk.corpus.stopwords.words('english')


def remove_specialwords(text):
    text = re.sub('\S+@\S+', '', text) # mail ids
    text = re.sub('@\S+' , '', text)   # mentions
    # text = re.sub('#\S+' , '', text)   # hashtags (should I do this?)
    text = re.sub('http\S+', '', text) # links
    text = re.sub('www\S+', '', text)  # links
    text = re.sub('pic.twitter.com\S+', '', text) # image links (not properly working yet)
    return text


def remove_punct(text):
    text = "".join([char for char in text if char not in punctuation])
    #text = re.sub('[0-9]+', '', text)
    return text


tokenizer = RegexpTokenizer(r'\w+')


def remove_stopwords(text):
    words = [w for w in text if w not in stop_words]
    return words


lemmatizer = WordNetLemmatizer()


def word_lemmatizer(text):
    lem_text = [lemmatizer.lemmatize(i) for i in text]
    return lem_text


stemmer = PorterStemmer()


def word_stemmer(text):
    stem_text = [stemmer.stem(i) for i in text]
    return stem_text


def make_sentence(text):
    sentence = " ".join([word for word in text])
    return sentence


def clean_text(text, lemmatize=True, sentence=False):
    text = remove_specialwords(text)
    text = remove_punct(text)
    text = tokenizer.tokenize(text.lower())
    text = remove_stopwords(text)
    if lemmatize is True:
        text = word_lemmatizer(text)
    else:
        text = word_stemmer(text)

    if sentence is True:
        text = make_sentence(text)
    return text


def give_all_words(doc):
    words = []
    for word in doc:
        words.append(word)
    return words