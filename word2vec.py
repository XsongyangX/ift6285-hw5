import logging
import os
from sys import argv, stderr
from text_from_csv import open_csv, Timer
from typing import Generator, Iterator, List
import gensim.models
import nltk
import argparse
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MyCorpus(object):
    """An interator that yields sentences (lists of str)."""

    def __init__(self, corpus_directory: str, blog_count: int=None):
        self.corpus_directory = corpus_directory
        self.blog_count = blog_count

    def __iter__(self) -> Iterator[List[str]]:
        # get file names of the corpus
        corpus = (os.path.join(self.corpus_directory, file) for file in os.listdir(self.corpus_directory))
        only_csv = [only_csv for only_csv in corpus if only_csv.endswith(".csv")]
        pruned = only_csv[:self.blog_count] if self.blog_count is not None else only_csv
        for file in pruned:
            for line in open_csv(file):
                # preprocessing?
                yield nltk.word_tokenize(line)

    def __read_lines(self, path: str) -> Iterator[str]:
        for line in open(path):
            yield line

def parse():
    parser = argparse.ArgumentParser(description="Learns a word2vec model")

    parser.add_argument('corpus_directory',\
        help="Path to the corpus directory")

    parser.add_argument('--size', type=int, default=100,\
        help="Dimensionality of the word vectors. (Default is 100)")
    
    parser.add_argument('--window', type=int, default=5,\
        help="Maximum distance between the current and predicted word within a sentence. (Default is 5)")
    
    parser.add_argument('--negative', type=int, default=5,\
        help="If > 0, negative sampling will be used, the int for negative specifies how many “noise words” should be drawn (usually between 5-20). If set to 0, no negative sampling is used. (Default is 5)")

    parser.add_argument('--blogcount', metavar='n',type=int, default=None,\
        help="How many blogs to digest. Default is all blogs.")

    parser.add_argument('--time', action='store_const', const=True, default=False,\
        help="Whether to time file by file. It might use too much memory. Default is no timing.")

    return parser.parse_args()

def main():
    
    args = parse()

    corpus = MyCorpus(args.corpus_directory, args.blogcount)
    
    if args.time:
        Timer('time_size{size}_window{window}_negative{negative}.csv'\
            .format(size=args.size, window=args.window, negative=args.negative))
        corpus = list(corpus)

    model = gensim.models.Word2Vec(sentences=corpus,\
        size=args.size,
        window=args.window,
        negative=args.negative)

    for i, word in enumerate(model.wv.vocab):
        if i == 10:
            break
        print(word)
    
    model.save('model_size{size}_window{window}_negative{negative}.model'\
        .format(size=args.size, window=args.window, negative=args.negative))

    if Timer.is_timing:
        Timer.get_current_timer().block_until_logged()

if __name__ == "__main__":
    main()