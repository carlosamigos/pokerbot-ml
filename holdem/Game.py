#!/usr/bin/python -tt
# -*- coding: utf-8 -*
from random import randint

from deuces.card import Card
from deuces.deck import Deck
from deuces.evaluator import Evaluator
from holdem.Player import Player


class Game:

    def __init__(self, smallBlind=1):
        self.deck = Deck()
        self.players = []
        self.smallBlind = smallBlind
        self.bigBlind = self.smallBlind * 2
        self.evaluator = Evaluator()

    def runGame(self):
        self.dealerPosition = randint(0, len(self.players))
        round = 0
        while len(self.players) > 1:
            self.runRound(round)
            self.removePlayerIfBankrupt()
            round += 1


    def runRound(self, round):
        self.resetGame(round)
        self.makePlayersPayBlinds()
        self.doRound(self.bigBlind, True)

        if (self.moreThanOnePlayerInRound()):
            self.drawCardsAndDoRound(3)
            if (self.moreThanOnePlayerInRound()):
                self.drawCardsAndDoRound(1)
                if (self.moreThanOnePlayerInRound()):
                    self.drawCardsAndDoRound(1)
        self.makeWinner()

    def removePlayerIfBankrupt(self):
        newPlayers = []
        for player in self.players:
            if player.stack >= self.bigBlind:
                newPlayers.append(player)
        self.players = newPlayers


    def getPlayersInRoundNotInAllIn(self):
        return [player for player in self.playersInRound if player not in self.playerIsAllIn]

    def moreThanOnePlayerInRound(self):
        return len(self.playersInRound) > 1

    def resetGame(self, round):
        print("\n\n\n ROUND", str(round + 1), "\n\n\n")
        self.startNewRound()
        self.board = []
        for player in self.players:
            player.print()
        print("dealer is " + str(self.players[self.dealerPosition].name))
        self.pot = 0
        self.playersInRound = []
        self.playersBettedCurrentRound = {}
        self.playerIsAllIn = set()

    def increaseDealerPosition(self):
        self.dealerPosition = (self.dealerPosition + 1) % len(self.players)

    def drawCardsAndDoRound(self, cardsToDraw):
        for player in self.playersInRound:
            self.playersBettedCurrentRound[player] = 0
        print("\n\nPot total is", self.pot)
        print("\n Flop:")
        self.board += self.deck.draw(cardsToDraw)
        Card.print_pretty_cards(self.board)
        if (len(self.getPlayersInRoundNotInAllIn()) > 1):
            self.doRound()

    def makeWinner(self):
        # Todo: side pot if someone is all-in
        winner = None
        lowestScore = 999999
        for player in self.playersInRound:
            score = self.evaluator.evaluate(player.getHand(), self.board)
            if (score < lowestScore):
                winner = player
                lowestScore = score + 0
        winner.stack += self.pot
        print("\n\nWinner is:", winner.name, " with +", self.pot, "in pot.\n\n")
        self.pot = 0

    def addPlayerToGame(self, player):
        self.players.append(player)

    def startNewRound(self):
        self.increaseDealerPosition()
        self.deck.shuffle()
        self.dealCardsToPlayers()

    def doRound(self, roundValue=0, preflop=False):
        self.roundValue = roundValue
        roundNr = 0
        while True:
            for i in range(len(self.players)):
                i += self.dealerPosition + preflop * 3
                i = i % len(self.players)
                player = self.players[i]
                if (player in self.playersInRound):
                    if (roundNr != 0 and self.allBettedTheSame() or not self.moreThanOnePlayerInRound()):
                        return
                    betAmount = player.doAction(self, self.playersBettedCurrentRound[player])
                    self.doPlayerAction(player, betAmount)
            roundNr += 1

    def makePlayersPayBlinds(self):
        for player in self.players:
            if(player.stack > self.smallBlind):
                self.playersBettedCurrentRound[player] = 0
                self.playersInRound.append(player)
        smallBlindPLayer = self.players[(self.dealerPosition + 1) % len(self.players)]
        bigBlindPLayer = self.players[(self.dealerPosition + 2) % len(self.players)]
        self.makePlayerBet(smallBlindPLayer, self.smallBlind)
        self.makePlayerBet(bigBlindPLayer, self.bigBlind)

    def makePlayerBet(self, player, amount):
        actualBet = player.bet(amount)
        self.playersBettedCurrentRound[player] += actualBet
        self.pot += actualBet
        return actualBet

    def allBettedTheSame(self):
        playersToCheck = [player for player in self.playersBettedCurrentRound.keys() if
                          player not in self.playerIsAllIn]
        if(len(playersToCheck) > 0):
            firstVal = float(self.playersBettedCurrentRound[playersToCheck[0]])
            for player in playersToCheck:
                if (float(self.playersBettedCurrentRound[player]) != firstVal):
                    return False
        return True

    def doPlayerAction(self, player, betAmount):
        if (betAmount == -1):
            self.playersBettedCurrentRound.pop(player, None)
            self.playersInRound.remove(player)
            print(player.name, "folded.")
        elif (betAmount > 0):
            self.makePlayerBet(player, betAmount)
            self.roundValue = max(self.roundValue, self.playersBettedCurrentRound[player])
            self.updateAllInPlayerList(player)
            print(player.name, "in with", self.playersBettedCurrentRound[player], "in this round")

    def updateAllInPlayerList(self, player):
        if (player.stack == 0):
            self.playerIsAllIn.add(player)

    def dealCardsToPlayers(self):
        for i in range(self.dealerPosition, len(self.players) + self.dealerPosition):
            index = i % len(self.players)
            player = self.players[index]
            card1 = self.deck.draw()[0]
            card2 = self.deck.draw()[0]
            player.giveCards(card1, card2)


def main():
    game = Game()
    players = [Player("carlos", 100), Player("martin", 100), Player("sjur", 100)]
    for player in players:
        game.addPlayerToGame(player)
    game.runGame()


main()
