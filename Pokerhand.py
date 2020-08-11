"""This module contains a code example related to
Think Python, 2nd Edition
by Allen Downey
http://thinkpython2.com
Copyright 2015 Allen Downey
License: http://creativecommons.org/licenses/by/4.0/
"""

from __future__ import print_function, division

from Card import Hand, Deck


class PokerHand(Hand):
    """Represents a poker hand."""

    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.
        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """
        Builds a histogram of the ranks that appear in the hand.
        Stores the result in atribute ranks.
        """
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1

    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
      
        Note that this works correctly for hands with more than 5 cards.
        """
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_pair(self):
        """
        Returns True if the hand has a pair, False otherwise.
        This works if the hand has more than 2 cards.
        """
        for val in self.ranks.values():
            if val >= 2:
                return True
        return False

    def has_twopair(self):
        """
        Returns True if the hand has two pairs, False otherwise.
        """
        num_pairs = 0
        for val in self.ranks.values():
            if val >= 2:
                num_pairs += 1
            if num_pairs == 2:
                return True
        return False

    def has_threerank(self):
        """
        Returns True if the hand has three cards with the same rank,
        False otherwise. This works if the hand has more than 3 cards.
        """
        for val in self.ranks.values():
            if val >= 3:
                return True
        return False

    def has_straight(self):
        """
        Returns True if the hand contains five cards with ranks in sequence,
        False otherwise. This works if the hand has more than 5 cards with ranks
        in sequence.
        """
        sequential_ranks = 1
        curr_key = 0
        previous_key = -1
        ace = {'Ace':(1,14)}
        
        for card in self.cards:
            # print(card)
            if sequential_ranks == 1 and card.rank_names[card.rank] == 'Ace':
                curr_key = ace['Ace'][0]
            elif card.rank_names[card.rank] == 'Ace':
                curr_key = ace['Ace'][1]
            else:
                curr_key = card.rank

            if curr_key == previous_key + 1:
                if (sequential_ranks != 1 or sequential_ranks != 4) and curr_key == 'Ace':
                    previous_key = None
                    continue
                sequential_ranks += 1

            if sequential_ranks == 5:
                return True
            
            previous_key = curr_key

        return False

    def full_house(self):
        """
        Returns True if there are three cards in one rank, and two cards in another rank,
        otherwise returns False.
        """
        three_rank = False
        two_rank = False

        for val in self.ranks.values():
            if val == 2:
                two_rank = True
            elif val == 3:
                three_rank = True
            if two_rank and three_rank:
                return True
        return False

    def has_fourrank(self):
        """
        Returns True if there exists four cards with the same rank,
        otherwise returns False.
        """
        for val in self.ranks.values():
            if val >= 4:
                return True
        return False

    def straight_flush(self):
        """
        Returns True if five cards in a sequence contain a straight
        and a flush, otherwise return False.
        """
        return self.has_straight() and self.has_flush()

    def classify(self):

        self.rank_hist()
        self.suit_hist()

        poker_hands = {
            "straight flush": self.straight_flush(),
            "four of a kind": self.has_fourrank(),
            "full house": self.full_house(),
            "flush": self.has_flush(),
            "straight": self.has_straight(),
            "three of a kind": self.has_threerank(),
            "two pair": self.has_twopair(),
            "pair": self.has_pair()
        }

        for key in poker_hands:
            if poker_hands[key]:
                return key

def num_classifications(elem):
    
    deck = Deck()
    deck.shuffle()
    classifications = {}
    curr_classification = ''
    num_hands = elem
    
    for i in range(num_hands):
        hand = PokerHand()
        deck.move_cards(hand, num_hands)
        curr_classification = hand.classify()
        classifications[curr_classification] = classifications.get(curr_classification, 0) + 1

    return classifications

def print_table():
    print("{0:<9}{1:<19}{2:<5}".format("hands", "classifications", "%"))
    print(34*"-")

    for i in range(1, 7):
        print("{0:>5}".format(i), end="")
        list_classes = list(num_classifications(i).items()) 
        for curr_class in list_classes:
            # print(curr_class)
            if curr_class[0] == None:
                curr_class = ("None",curr_class[1])
            print("    {0:<19}{1:.4f}".format(*curr_class, curr_class[1] / i))
            print(5*' ', end='')
        print('\n' + 34*'-')

# print(num_classifications())
print_table()