from pymongo import MongoClient

import re

topics_collection = MongoClient().manhattan_project.topics

def term_distance(term1, term2):
    #look at percentage of match using string distances?
    #look at how large overlap of wordsets are?
    wordset1 = set(term1.split(' '))
    wordset2 = set(term2.split(' '))

    intersection = wordset1 & wordset2
    overlap_score = float(len(intersection)/max(len(wordset1),len(wordset2)))

    return overlap_score

def annotate(text, stoplistfile="SmartStoplist.txt"):

    with open(stoplistfile,'r') as stoplist:
        stop_words = stoplist.read().splitlines()

    words =  re.findall(r"[\w']+", text)
    nonstop_words = [word.lower() for word in words if word.lower() not in stop_words]

    annotations = {}
    word_index = 0
    while word_index < len(nonstop_words):

        term = nonstop_words[word_index]

        term_matches = topics_collection.find({"topic": {"$regex": term.replace(' ','*')}})
        term_matches = list(term_matches)

        #include following context until a single result remains?
        while len(term_matches) > 1:

            term += ' %s' % nonstop_words[word_index + 1]
            if "newton" in term and "gravitation":
                print term
            term_matches = topics_collection.find({"topic": {"$regex": term}})
            term_matches = list(term_matches)


            word_index += 1

        if not term_matches and len(term.split(' ')) > 1:

            term = ' '.join(term.split(' ')[:-1])
            term_matches = topics_collection.find({"topic": {"$regex": term}})
            term_matches = list(term_matches)
            if "newton" in term:
                print term

            word_index -= 1

        match_scores = []

        for match in term_matches:
            score = term_distance(match['topic'], term)
            if score > 0.7:
                match['score'] = score
                match_scores.append(match)

        match_scores.sort(key=lambda match: match['score'], reverse=True)

        if match_scores:
        #    print match_scores
            annotations[term] = match_scores[0]['url']




        #
        # # if a result remains, check to see if it is close enough
        # if len(term_matches) == 1:
        #     if (term==term_matches[0]['topic']):
        #         term_match = term_matches[0]
        #     else:
        #         term_match = None
        #
        # # if not return to the previous round (if there was one) to look for exact match
        # elif not term_matches and len(term.split(' ')) > 1:
        #
        #     term = ' '.join(term.split(' ')[:-1])
        #     term_match = topics_collection.find_one({"topic": term})
        #
        #     word_index -= 1
        #
        # # otherwise no match
        # else:
        #     term_match = None
        #
        #
        # if term_match and term not in annotations.keys():
        #
        #     annotations[term] = term_match['url']

        word_index += 1

    return annotations


if __name__ == "__main__":

    with open('newtons_laws.txt','r') as ifile:
        text = ifile.read()

    print annotate(text)
