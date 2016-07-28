from gensim.models import doc2vec

import json
import numpy as np
import Levenshtein


def preprocess_text(contentfiles = ["physics_textbook_0.json", "physics_textbook_1.json", "physics_textbook_2.json","physics_textbook_3.json"]):

    training_data = []
    for filename in contentfiles:
        with open(filename,'rb') as infile:
            training_data += json.load(infile)

    # with open('physics_content.json') as infile:
    #     content = json.load(infile)

    #assemble txt file with each sent on a separate line
    # all_content = ''.join([topic['content'].lower()+' '+topic['topic'].lower() for topic in content])
    # sentences = all_content.split('.')

    sentences = []
    # for topic in content:
    #     topic_sentences = topic['content'].split(' ')
    #     topic_sentences = [sentence.lower()+' '+topic['topic'.lower()] for sentence in topic_sentences]
    #     sentences += topic_sentences

    for line in training_data:
        sentences.append(line.lower())
    print len(sentences)
    labeled_sentences = []
    for i in range(len(sentences)):
        labeled_sentences.append(doc2vec.TaggedDocument(sentences[i].split(' '),'sent%d'%i))

    return labeled_sentences


def train_model(labeled_sentences, epochs=15, savefile = 'textbook_model.doc2vec'):

    model = doc2vec.Doc2Vec(documents=labeled_sentences, size=100, window=20, min_count=10, workers=4, iter=epochs, dm=1)
    #model.build_vocab(labeled_sentences)

    # for epoch in range(epochs):
    #     model.train(labeled_sentences)
    #     model.alpha -= 0.002  # decrease the learning rate
    #     model.min_alpha = model.alpha

    model.save(savefile)

    return model

if __name__ == "__main__":
    labeled_sentences = preprocess_text()
    model = train_model(labeled_sentences)
