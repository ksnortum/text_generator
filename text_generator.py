from nltk import WhitespaceTokenizer
from nltk.util import bigrams
from collections import Counter, defaultdict
import random


class TextGenerator:

    ENDING_PUNCTUATION = ('.', '!', '?')

    def __init__(self):
        self.bi_grams = []
        self.tokens = []
        self.markov_chain = {}
        self.start_words = []

    def run(self):
        self.load_corpus()
        self.create_start_word_list()
        self.create_markov_chain()

        for _ in range(10):
            print(self.make_more_realistic_sentence())

    def load_corpus(self):
        file_name = input()
        with open(file_name, "r", encoding="utf-8") as f:
            self.tokens = WhitespaceTokenizer().tokenize(f.read())
            self.bi_grams = list(bigrams(self.tokens))

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

    def create_start_word_list(self):
        self.start_words = [word for word in self.tokens
                            if word[0].isupper()
                            and not word.endswith(self.ENDING_PUNCTUATION)]

    # Not currently used
    def head_loop(self):
        head = input()

        while head != 'exit':
            if head in self.markov_chain.keys():
                self.print_head_and_tails(head)
            else:
                print(f'Head: {head}')
                print('Key Error. The requested word is not in the model. Please input another word.\n')

            head = input()

    # Not currently used
    def print_head_and_tails(self, head: str) -> None:
        print(f'Head: {head}')
        for element in self.markov_chain[head]:
            print(f'Tail: {element[0]}\tCount: {element[1]}')
        print()

    # Not currently used
    def make_pseudo_sentence(self) -> str:
        # Get first word randomly
        head = random.choice(self.tokens)
        sentence = [head]

        # For the next 9 words...
        # Choose from a weighted list of tails for this head
        for _ in range(9):
            tails = [element[0] for element in self.markov_chain[head]]
            weights = [element[1] for element in self.markov_chain[head]]
            next_word = random.choices(tails, weights=weights)[0]
            sentence.append(next_word)
            head = next_word

        return ' '.join(sentence)

    def make_more_realistic_sentence(self) -> str:
        head = random.choice(self.start_words)
        sentence = [head]

        while len(sentence) < 5 or not sentence[-1].endswith(self.ENDING_PUNCTUATION):
            next_word = self.get_next_word(head)
            sentence.append(next_word)
            head = next_word

        return ' '.join(sentence)

    def get_next_word(self, head: str) -> str:
        tails = [element[0] for element in self.markov_chain[head]]
        weights = [element[1] for element in self.markov_chain[head]]

        return random.choices(tails, weights=weights)[0]


if __name__ == "__main__":
    TextGenerator().run()
