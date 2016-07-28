from gensim.models import doc2vec

import json
import numpy as np
import Levenshtein
import sys


def vectorize_terms(term_list, model):

    for term in term_list:
    #     words = term['topic'].lower().split(' ')
    #     word_vecs = [model.infer_vector([word], steps=40) for word in words]
    #
    #     norm_vecs = [vec/np.linalg.norm(vec) for vec in word_vecs]
    #     avg_vec = sum(norm_vecs)/len(norm_vecs)
    # #    print avg_vec
    #     term['vector'] = avg_vec
        term['vector'] = model.infer_vector(term['topic'].lower().split(' '), steps=40)

    return term_list


def similarity(vec1, vec2):
    return np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))

def normed_levensthein(term1, term2):

    term1 = term1.encode('ascii', 'ignore')
    term2 = term2.encode('ascii', 'ignore')

    distance = Levenshtein.distance(str(term1.lower()), str(term2.lower()))
    normed_d = float(distance)/max(len(term1), len(term2))

    return normed_d

def rough_word_intersection(term1, term2, threshold = 0.7):
    words1 = term1.split(' ')
    words2 = term2.split(' ')

    word_intersect = 0
    for word1 in words1:
        for word2 in words2:
            distance = normed_levensthein(word1, word2)
            if (1-distance) > threshold:
                word_intersect += (1-distance)
    return word_intersect


def find_match(match_term, term_list, model):

    match_vec = model.infer_vector(match_term.lower().split(' '), steps=40)

    sim_scores = [{'sim':similarity(topic['vector'], match_vec), 'topic': topic['topic']} for topic in term_list]
    ranked_sims = sorted(sim_scores, key = lambda x: x['sim'], reverse=True)
    top_sims = ranked_sims[: int(len(sim_scores)/3.)]

    # for term in top_sims:
    #     word_overlap = rough_word_intersection(term['topic'], match_term)
    #
    #     term['sim'] += word_overlap
    #
    # ranked_sims = sorted(top_sims, key=lambda x: x['sim'], reverse=True)

    return ranked_sims


if __name__ == "__main__":

    model = doc2vec.Doc2Vec.load('textbook_model.doc2vec')

    term_list = json.load(open('keyphrase_list.json','rb'))
    term_list = vectorize_terms(term_list, model)

    if len(sys.argv) > 1:
        match_term = sys.argv[1]
    else:
        match_term = 'momentum'

    matches = find_match(match_term, term_list, model)

    print matches[:5]
