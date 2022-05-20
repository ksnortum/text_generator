from nltk import WhitespaceTokenizer
from nltk.util import bigrams
from collections import Counter, defaultdict


class TextGenerator:

    def __init__(self):
        self.bi_grams = []
        self.markov_chain = {}

    def run(self):
        self.load_corpus()
        self.create_markov_chain()
        self.head_loop()

    def load_corpus(self):
        file_name = input()
        with open(file_name, "r", encoding="utf-8") as f:
            tokens = WhitespaceTokenizer().tokenize(f.read())
            self.bi_grams = list(bigrams(tokens))

    def create_markov_chain(self):
        tails_by_head = defaultdict(list)

        # make a list of all tails for this head
        for head, tail in self.bi_grams:
            tails_by_head[head].append(tail)

        # use the list of tails to create a Counter, then set the
        # Markov chain using the frequency dict
        for head, list_of_tails in tails_by_head.items():
            tails = Counter(list_of_tails)
            self.markov_chain[head] = tails.most_common()

    def head_loop(self):
        head = input()

        while head != 'exit':
            if head in self.markov_chain.keys():
                self.print_head_and_tails(head)
            else:
                print(f'Head: {head}')
                print('Key Error. The requested word is not in the model. Please input another word.\n')

            head = input()

    def print_head_and_tails(self, head: str) -> None:
        print(f'Head: {head}')
        for element in self.markov_chain[head]:
            print(f'Tail: {element[0]}\tCount: {element[1]}')
        print()


if __name__ == "__main__":
    TextGenerator().run()
