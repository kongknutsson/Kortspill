from random import shuffle
import time
d = 1

# En klasse som Dealer og Player arver egenskaper fra.
class Contestants:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.points = 0

    #drar n kort fra deck
    def draw_cards(self, deck, n):
        for x in range(0, n):
            new_card = deck.pop()
            self.cards.append(new_card)
            self.points += new_card.points

    def print_newest_card(self):
        newest_card = self.cards[len(self.cards)-1].name
        print(self.name, "- new card is", newest_card)
        time.sleep(d)

    def print_cards(self):
        i = 1
        for card in self.cards:
            print(self.name, "- card", i, "is", card.name)
            time.sleep(d)
            i += 1

    def print_points(self):
        print(self.name, "- has", self.points, "points.")

class Dealer(Contestants):
    # Man skal kun se dealeren sitt første kort.
    def print_starting_cards(self):
        print(self.name, "- 1st card is", self.cards[0].name)
        time.sleep(d)
        print(self.name, "- 2nd card is hidden.")
        time.sleep(d)

    # Man skal kun se dealeren sin poengsum UTEN det skjulte kortet.
    def print_starting_points(self):
        print(self.name, "- has", self.points - self.cards[1].points, "points. (Second card is hidden.)")

    def loop(self, deck):
        self.print_cards()
        self.print_points()
        # Dealeren trekkert kort frem til han har 17 poeng.
        while self.points < 17:
            self.draw_cards(deck, 1)
            self.print_newest_card()
            self.print_points()
        return self.points

class Player(Contestants):
    def loop(self, deck):
        while True:
            inp = input("Write D to draw a card. Write S to stand: ").upper()
            if inp == "D":
                self.draw_cards(deck, 1)
                time.sleep(d)
                self.print_newest_card()
                time.sleep(d)
                self.print_points()
                time.sleep(d)
                # Om du er over 21 poeng har du tapt.
                # Om du er på 21 poeng har du beste scoren, og det er derfor
                # ingen vits å fortsette, fordi du allerede vant.
                if self.points >= 21:
                    return self.points
            elif inp == "S":
                return self.points
            else:
                print("Invalid character. Write either D or S.")

class Card:
    def __init__(self, points, suit):
        # Spar, kløver, hjerte, ruter
        self.suit = suit
        # Endrer poengene over 10 til bildekort.
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

        # Verdien til et kort er maks 10.
        if points > 10:
            self.points = 10
        else:
            self.points = points

def new_deck():
    card_list = []
    suit_list = ("spades", "clubs", "diamonds", "hearts")
    for suit in suit_list:
        # Kort tall går fra 1 til 13
        for x in range(1, 14):
            card_list.append(Card(x, suit))
    return card_list

def main():
    # Lager kortstokk og shuffler den.
    deck = new_deck()
    shuffle(deck)

    # Lager spillere.
    player = Player(input("Player Name: "))
    dealer = Dealer("Dealer")
    print()

    # Begynner dealeren sin del av spillet.
    dealer.draw_cards(deck, 2)
    time.sleep(d)
    print(dealer.name, "- draws 2 cards.")
    time.sleep(d)
    dealer.print_starting_cards()
    time.sleep(d)
    dealer.print_starting_points()
    time.sleep(d)
    print()

    # Begynner spilleren sin del av spillet.
    player.draw_cards(deck, 2)
    time.sleep(d)
    print(player.name, "- draws 2 cards")
    time.sleep(d)
    player.print_cards()
    time.sleep(d)
    player.print_points()
    time.sleep(d)
    print()
    player_points = player.loop(deck)

    # Spiller og deal er er ferdig, så sjekker scoren. 
    if player_points <= 21:
        print(player.name, "- standing at", player.points, "points.\n")
        time.sleep(d)
        dealer_points = dealer.loop(deck)

        if player_points > dealer_points or dealer_points > 21:
            print("\n-- YOU WON --")
        elif dealer_points >= player_points:
            print("\n-- YOU LOST --")

    elif player_points > 21:
        print("You lost due to going over 21. Sorry.")

if __name__ == "__main__":
    main()