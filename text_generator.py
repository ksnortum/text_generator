from nltk import WhitespaceTokenizer
from nltk.util import bigrams
from markov_chain import MarkovChain


class TextGenerator:

    def __init__(self):
        self.bi_grams = []
        self.markov_chain = MarkovChain()

    def run(self):
        self.load_corpus()
        self.create_markov_chain()
        # self.index_loop()
        self.head_loop()

    def load_corpus(self):
        file_name = input()
        with open(file_name, "r", encoding="utf-8") as f:
            tokens = WhitespaceTokenizer().tokenize(f.read())
            self.bi_grams = list(bigrams(tokens))

    def create_markov_chain(self):
        for bi_gram in self.bi_grams:
            self.markov_chain.add(bi_gram)

    def index_loop(self):  # Not currently used
        ans = input()

        while ans != 'exit':
            try:
                bi_gram = self.bi_grams[int(ans)]
                print(f'Head: {bi_gram[0]}\tTail: {bi_gram[1]}')
            except IndexError:
                print("Index Error. Please input an integer that is in the range of the corpus.")
            except ValueError:
                print("Value Error. Please input an integer.")
            except TypeError:
                print("Type Error. Please input an integer.")

            ans = input()

    def head_loop(self):
        # input()  # TODO why is this necessary when I run in the IDE?
        head = input()

        while head != 'exit':
            if head in self.markov_chain.get_chain():
                self.markov_chain.print_head_and_tails(head)
            else:
                print(f'Head: {head}')
                print('Key Error. The requested word is not in the model. Please input another word.\n')

            head = input()


if __name__ == "__main__":
    TextGenerator().run()
