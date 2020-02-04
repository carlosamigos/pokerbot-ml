from deuces.card import Card


class Player:

    def __init__(self, name, numberOfChips):
        self.name = name
        self.stack = numberOfChips
        self.card1 = ""
        self.card2 = ""

    def giveCards(self, card1, card2):
        self.card1 = card1
        self.card2 = card2

    def getHand(self):
        return [self.card1, self.card2]

    def doAction(self, game, playerBettedCurrentRound):
        print("\nPlayer " + self.name + "'s (" + str(self.stack) + ") turn:")
        if (game.roundValue - playerBettedCurrentRound > 0):
            toCall = str(game.roundValue - playerBettedCurrentRound)
            minRaise = float(toCall) + max(game.roundValue - playerBettedCurrentRound, game.bigBlind)
            print(game.roundValue - playerBettedCurrentRound, "to call")
            inpString = "Choices; fold = -1, call (" + toCall + ") or raise > " + str(minRaise) + " "
            inp = float(input(inpString))
            while not (inp == float(toCall) or inp >= minRaise or inp == -1):
                inp = float(input(inpString))
            return inp
        inpString = "Choices; fold = -1, check = 0, raise > " + str(game.bigBlind) + " "
        inp = float(input(inpString))
        while inp < game.bigBlind and inp > 0 and inp != -1:
            inp = float(input(inpString))
        return inp

    def bet(self, value):
        bet = min(value, self.stack)
        self.stack -= bet
        return min(value, bet)

    def fold(self):
        self.card1 = ""
        self.card2 = ""

    def print(self):
        print(self.name + "(chips=" + str(self.stack) + "):")
        Card.print_pretty_card(self.card1)
        Card.print_pretty_card(self.card2)
