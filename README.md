# Solitaire
Python implementation with GUI for Solitaire

## What is Solitaire? ##
Solitaire is a classic card game that can be played solo, hence the name from France. The most common version is Klondike Solitaire, the version implemented here, where the goal is to move all cards to four foundation piles, starting with the Ace and ending with the King, all in the same suit.

## How to play? ##
You just have to run the main.py script in order for the game to start. Cards will be dealt randomly, and you can start to place them by the rules.

## What rules are there? ##
There are four different types of piles in Solitaire:

__The Tableau__: Seven piles that make up the main table.

__The Foundations__: Four piles on which a whole suit or sequence must be built up. In most Solitaire games, the four aces are the bottom card or base of the foundations. The foundation piles are hearts, diamonds, spades, and clubs.

__The Stock (or “Hand”) Pile__: If the entire pack is not laid out in a tableau at the beginning of a game, the remaining cards form the stock pile from which additional cards are brought into play according to the rules.

__The Talon (or “Waste”) Pile__: Cards from the stock pile that have no place in the tableau or on foundations are laid face up in the waste pile.

The initial array may be changed by "building" - transferring cards among the face-up cards in the tableau. Certain cards of the tableau can be played at once, while others may not be played until certain blocking cards are removed. For example, of the seven cards facing up in the tableau, if one is a nine and another is a ten, you may transfer the nine to on top of the ten to begin building that pile in sequence. Since you have moved the nine from one of the seven piles, you have now unblocked a face down card; this card can be turned over and now is in play.

As you transfer cards in the tableau and begin building sequences, if you uncover an ace, the ace should be placed in one of the foundation piles. The foundations get built by suit and in sequence from ace to king.

Continue to transfer cards on top of each other in the tableau in sequence. If you can’t move any more face up cards, you can utilize the stock pile by flipping over the first card. This card can be played in the foundations or tableau. If you cannot play the card in the tableau or the foundations piles, move the card to the waste pile and turn over another card in the stock pile.

If a vacancy in the tableau is created by the removal of cards elsewhere it is called a “space”, and it is of major importance in manipulating the tableau. If a space is created, it can only be filled in with a king. Filling a space with a king could potentially unblock one of the face down cards in another pile in the tableau.

Continue to transfer cards in the tableau and bring cards into play from the stock pile until all the cards are built in suit sequences in the foundation piles to win!

## Project definition ##

<img width="630" alt="Screenshot 2024-12-07 at 00 27 02" src="https://github.com/user-attachments/assets/82a0e01a-8a27-409b-a331-e295e02ca59e">

## References ##

https://bicyclecards.com/how-to-play/solitaire

https://www.britannica.com/topic/solitaire-card-game
