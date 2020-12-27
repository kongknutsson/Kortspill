from random import shuffle
import time

class Entities:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.points = [0, 0]

    def draw_cards(self, deck, number):
        for x in range(0, number):
            new_card = deck.pop()
            self.cards.append(new_card)
            self.points[0] += new_card.points
            self.points[1] += new_card.points
            if new_card.points == 1:
                self.points[1] += 11 - new_card.points

    def print_newest_card(self):
        newest_card = self.cards[len(self.cards)-1].name
        print(self.name, "- new card is", newest_card)

    def print_cards(self):
        i = 1
        for card in self.cards:
            print(self.name, "- card", i, "is", card.name)
            i += 1

    def print_points(self):
        f_points = self.points[0]
        s_points = self.points[1]
        if f_points != s_points:
            print("fpoints:", f_points,"spoints:", s_points)
            if not s_points > 21:
                print(self.name, "- has", f_points, "/", s_points, "points.")
            else:
                print(self.name, "- has", f_points, "points.")
        else:
            print(self.name, "- has", f_points, "points.")


class Dealer(Entities):

    def print_starting_cards(self):
        print(self.name, "- 1st card is", self.cards[0].name)
        print(self.name, "- 2nd card is hidden.")

    def print_starting_points(self):
        f_points = self.points[0]
        s_points = self.points[1]
        if self.cards[0].points == 1:
            print(self.name, "- has 1 / 11 points. (Second card is hidden.)")
        else:
            print(self.name, "- has", f_points - self.cards[1].points, "points. (Second card is hidden.)")

    def loop(self, deck):
        self.print_cards()
        self.print_points()
        x = [17, 18, 19, 20, 21]
        while ((self.points[0] not in x) or (self.points[1] not in x)) and (self.points[0] < 21 and self.points[1] < 21):
        #while self.points[0] < 17 or (self.points[1] < 17 and not self.points[1] > 21):
            self.draw_cards(deck, 1)
            self.print_newest_card()
            self.print_points()
        highest = self.points[0]
        if self.points[1] > highest:
            highest = self.points[1]
        return highest

class Player(Entities):

    def loop(self, deck):
        playerturn = True
        while playerturn:
            if self.points[1] == 21:
                return "blackjack"
            inp = input("Write D to draw a card. Write S to stand: ")
            inp = inp.upper()
            if inp == "D":
                self.draw_cards(deck, 1)
                self.print_newest_card()
                self.print_points()
                if self.points[0] > 21:
                    playerturn = False
                    return self.points[0]
            elif inp == "S":
                playerturn = False
                highest = self.points[0]
                if self.points[1] > highest and not self.points[1] > 21:
                    highest = self.points[1]
                return highest
            else:
                print("Invalid character. Write either D or S.")

class Card:
    def __init__(self, points, suit):
        self.suit = suit
        if points == 11:
            self.name = " ".join(["Jack of", str(suit)])
        elif points == 12:
            self.name = " ".join(["Queen of", str(suit)])
        elif points == 13:
            self.name = " ".join(["King of", str(suit)])
        elif points == 1:
            self.name = " ".join(["Ace of", str(suit)])
        else:
            self.name = " ".join([str(points), "of", str(suit)])
        if points >= 11:
            self.points = 10
        else:
            self.points = points

def new_deck():
    card_list = []
    suit_list = ("spades", "clubs", "diamonds", "hearts")
    for suit in suit_list:
        for x in range(1, 14):
            c = Card(x, suit)
            card_list.append(c)
    return card_list

def main():
    deck = new_deck()
    shuffle(deck)
    player = Player("Adrian")
    dealer = Dealer("Dealer")
    print()

    dealer.draw_cards(deck, 2)
    print(dealer.name, "- draws 2 cards.")
    dealer.print_starting_cards()
    dealer.print_starting_points()
    print()

    player.draw_cards(deck, 2)
    print(player.name, "- draws 2 cards")
    player.print_cards()
    player.print_points()
    print()
    player_points = player.loop(deck)

    if player_points == "blackjack":
        print("-- YOU WON DUE TO BLACKJACK --")
    elif player_points <= 21:
        print(player.name, "- standing at", player_points, "points.\n")
        time.sleep(1)
        dealer_points = dealer.loop(deck)
        if player_points > dealer_points or dealer_points > 21:
            print("\n-- YOU WON --")
        elif dealer_points >= player_points:
            print("\n-- YOU LOST --")

    elif player_points > 21:
        print("You lost due to going over 21. Sorry.")

if __name__ == "__main__":
    main()