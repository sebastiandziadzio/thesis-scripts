import distance
import operator
import argparse
from collections import defaultdict
from srilm import LM

def read_hypotheses(filename):
    hypo = defaultdict(list)
    with open(filename, 'r') as f:
        for line in f:
            index, text = line.split("\t")
            hypo[int(index)].append(text)
    return hypo

def get_prob(lm):
    def calculate_prob(hypothesis)
        return lm.total_logprob_strings(hypothesis.split())
    return calculate_prob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to the language model file', type=str)
    parser.add_argument('test', help='path to the test file', type=str)
    args = parser.parse_args()
    lm = LM(args.path)
    score = get_prob_fun(lm)
    hypo = read_hypotheses(args.test)
    werr_total = 0
    for index in hypo:
        reference = hypo[index][0]
        scores = [(hypothesis, score(hypothesis)) for hypothesis in hypo[index][1:]] 
        best = max(scores, key=operator.itemgetter(1))
        werr_total +=  distance.levenshtein(reference.split(), best.split())
