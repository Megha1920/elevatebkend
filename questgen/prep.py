import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from .clean import clean_text

class Que:
    def __init__(self, question, ans, options):
        self.question = question
        self.ans = ans
        self.options = options

class Text:
    def __init__(self, text):
        self.text = text
        self.sents = sent_tokenize(text)

    def generate_questions(self):
        questions = []
        for sent in self.sents:
            tokenized_sent = word_tokenize(sent)
            selected_words = [word for word, pos in nltk.pos_tag(tokenized_sent) if pos.startswith('NN')]

            if len(selected_words) == 0:
                continue

            ans = random.choice(selected_words)
            blank = '__' * len(ans)
            blanked_sentence = re.sub(r'\b' + re.escape(ans) + r'\b', blank, sent)

            options = self.get_options(ans)

            if options is None:
                continue

            new_question = Que(blanked_sentence, ans, options)
            questions.append(new_question)

        return questions

    def get_options(self, word, n=4):
        synonyms = []
        try:
            synsets = wn.synsets(word, pos=wn.NOUN)
            for synset in synsets:
                synonyms.extend([lemma.replace('_', ' ') for lemma in synset.lemma_names() if lemma != word])
        except:
            return None

        if len(synonyms) >= n:
            options = random.sample(synonyms, n)
            options.append(word)
            return options
        else:
            return None