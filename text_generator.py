from nltk import WhitespaceTokenizer
from nltk.util import trigrams
from collections import Counter, defaultdict
import random


class TextGenerator:

    ENDING_PUNCTUATION = ('.', '!', '?')

    def __init__(self):
        self.tri_grams = []
        self.tokens = []
        self.markov_chain = {}
        self.start_words = []

    def run(self):
        self.load_corpus()
        self.create_start_word_list()
        self.create_markov_chain()

        for _ in range(10):
            print(self.make_realistic_sentence())

    def load_corpus(self):
        file_name = input()
        with open(file_name, "r", encoding="utf-8") as f:
            self.tokens = WhitespaceTokenizer().tokenize(f.read())
            self.tri_grams = list(trigrams(self.tokens))

    def create_markov_chain(self):
        tails_by_head = defaultdict(list)

        # make a list of all tails for this two-word head
        for head1, head2, tail in self.tri_grams:
            tails_by_head[f'{head1} {head2}'].append(tail)

        # use the list of tails to create a Counter, then set the
        # Markov chain using the frequency dict
        for two_word_head, list_of_tails in tails_by_head.items():
            self.markov_chain[two_word_head] = Counter(list_of_tails).most_common()

    def create_start_word_list(self):
        self.start_words = [(words[0], words[1]) for words in self.tri_grams
                            if words[0][0].isupper()
                            and not words[0].endswith(self.ENDING_PUNCTUATION)]

    def make_realistic_sentence(self) -> str:
        head1, head2 = random.choice(self.start_words)
        sentence = [head1, head2]

        while len(sentence) < 5 or not sentence[-1].endswith(self.ENDING_PUNCTUATION):
            next_word = self.get_next_word(head1, head2)
            sentence.append(next_word)
            head1 = head2
            head2 = next_word

        return ' '.join(sentence)

    def get_next_word(self, head1: str, head2: str) -> str:
        two_word_head = f'{head1} {head2}'
        tails = [element[0] for element in self.markov_chain[two_word_head]]
        weights = [element[1] for element in self.markov_chain[two_word_head]]

        return random.choices(tails, weights=weights)[0]


if __name__ == "__main__":
    TextGenerator().run()
