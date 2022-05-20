# TODO use collections.Counter and default dict
class MarkovChain:

    def __init__(self):
        self.chain = dict()

    def add(self, bi_gram):
        """{head: {tail: freq}}"""
        head = bi_gram[0]
        tail = bi_gram[1]

        if head not in self.chain:
            tails = (self.Tails())
        else:
            tails = self.chain[head]

        tails.add(tail)
        self.chain[head] = tails

    def print_head_and_tails(self, head: str) -> None:
        print(f'Head: {head}')
        tails = self.chain[head].get_tails()
        for tail in tails.keys():
            print(f'Tail: {tail}\tCount: {tails[tail]}')
        print()

    def get_chain(self):
        return self.chain

    class Tails:

        def __init__(self):
            self.tails = dict()

        def add(self, tail: str) -> None:
            if tail in self.tails:
                self.tails[tail] += 1
            else:
                self.tails[tail] = 1

        def get_tails(self) -> dict:
            return self.tails
