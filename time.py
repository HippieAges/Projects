class Time:
    def __init__(self, hours=0,minutes=0,seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __lt__(self, other):
        t1 = self.hours, self.minutes, self.seconds
        t2 = other.hours, other.minutes, other.seconds
        return t1 < t2

time1 = Time(1,5,9)
time2 = Time(1,5,10)

print(time1.__lt__(time2))

class Card:

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7', 
              '8', '9', '10', 'Jack', 'Queen', 'King']

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __lt__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2

class Deck:

    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        res = []
        for card in self.cards:
            res.append('%s of %s' % (card.suit_names[card.suit], card.rank_names[card.rank]))
        return '\n'.join(res)

    def sort_cards(self):
        self.cards.sort(key=lambda x: x.__lt__(x))


class Hand(Deck):

    def __init__(self, label=''):
        self.cards = []
        self.label = label

# deck = Deck()
# deck.sort_cards()
# print(deck)