from nltk import WhitespaceTokenizer
from nltk.util import bigrams
from collections import Counter, defaultdict
import random
import re


class TextGenerator:

    def __init__(self):
        self.bi_grams = []
        self.tokens = []
        self.markov_chain = {}
        self.uppercase_letters = re.compile(r'[A-Z]')
        self.sentence_ending_punctuation = re.compile(r'[.!?]$')

    def run(self):
        self.load_corpus()
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
        head = self.find_first_word()
        sentence = [head]

        for _ in range(4):
            next_word = self.get_next_word(head)
            sentence.append(next_word)
            head = next_word

        count = 0
        # TODO, use endswith and list of punct
        # TODO, choose from list of tokens ending with punct
        while not self.sentence_ending_punctuation.search(sentence[-1]):

            # Give up after 100 tries
            if count > 100:
                print("*** sentence too long")  # TODO testing
                last_word = random.choice(self.tokens)
                # TODO, use endswith and punct
                # TODO, select for ending words list
                if not self.sentence_ending_punctuation.search(last_word):
                    last_word += "."
                sentence.append(last_word)
                break

            sentence.append(self.get_next_word(head))
            count += 1

        return ' '.join(sentence)

    # TODO make list of valid starting words once, then pick from that list
    def find_first_word(self):
        word = ''

        # TODO, or just use word[0].isUpper()
        # TODO, use word.endswith(<list of punct>)
        while not self.uppercase_letters.match(word) \
                or self.sentence_ending_punctuation.search(word):
            word = random.choice(self.tokens)

        return word

    def get_next_word(self, head: str) -> str:
        tails = [element[0] for element in self.markov_chain[head]]
        weights = [element[1] for element in self.markov_chain[head]]

        return random.choices(tails, weights=weights)[0]


if __name__ == "__main__":
    TextGenerator().run()
