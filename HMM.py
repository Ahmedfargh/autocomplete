

import nltk
import pandas as pd
from collections import Counter
from nltk.tokenize import TreebankWordTokenizer
from nltk import ngrams
dataset_train=pd.read_csv("total_train.csv")
dataset_train
class Preprocessor:
    def __init__(self):
        self.tokenizer=TreebankWordTokenizer()
    def tokenize(self,text):
        return self.tokenizer.tokenize(text.lower())
    def get_ngram(self,text):
        return list(ngrams(self.tokenizer.tokenize(text),2))
processor=Preprocessor()
dataset_train["bigram"]=dataset_train["total_string"].map(processor.get_ngram)
dataset_train["bigram"]
class HMM:
    def __init__(self,datatrain):
        self.train_data=datatrain
        self._counter={}
        self.processor=Preprocessor()
    def is_trained(self):
        return len(self.counter)==0
    def train(self):
        for data in self.train_data:
            for bigram in data:
                if bigram[0] in self._counter.keys():
                    if bigram[1] in self._counter[bigram[0]].keys():
                        self._counter[bigram[0]][bigram[1]]+=1
                    else:
                        self._counter[bigram[0]][bigram[1]]=1 
                    continue
                else:
                    self._counter[bigram[0]]={bigram[1]:1}
                    continue
        print("training is done")
        return True
    def get_counter(self):
        return self._counter
    def predict_next_word(self,sent):
        bigram=self.processor.get_ngram(sent)
        last_one=bigram[len(bigram)-1]
        sencond_words_list=self._counter[last_one[1]]
        indicator={}
        first_word_counter=0
        best_choise=self._counter[last_one[1]][list(self._counter[last_one[1]].keys())[0]]
        best_word=list(self._counter[last_one[1]].keys())[0]
        for word in list(self._counter[last_one[1]].keys()):
            first_word_counter+=self._counter[last_one[1]][word]
        for word in list(sencond_words_list.keys()):
            if sencond_words_list[word]> sencond_words_list[best_word]:
                best_word=word
                best_choise=sencond_words_list[best_word]
        return {"next_word":best_word}
    def predict_next_word_given_first_letters(self,sent):
        sent=sent.lower().split(" ")
        last_word_list=self._counter[sent[len(sent)-2]]
        first_char=sent[len(sent)-1]
        candidate={}
        for word in list(last_word_list.keys()):
            if word.startswith(first_char):
                candidate[word]=last_word_list[word]
        best_choise=candidate[list(candidate.keys())[0]]
        best_word=list(candidate.keys())[0]
        for word in list(candidate.keys()):
            if best_choise<candidate[word]:
                best_word=word
                best_choise=candidate[word]
        prob=1
        if best_choise>1:
            prob=1
        else:
            prob=best_choise/len(self._counter[sent[len(sent)-2]])
        return {"next_word":best_word}
hmm=HMM(dataset_train["bigram"].values)
hmm.train()
print(hmm.predict_next_word("Add Live from Aragon Ballroom to my"))
print(hmm.predict_next_word_given_first_letters("Add Live from Aragon Ballroom to my pl"))
