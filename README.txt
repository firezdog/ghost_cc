LONGEST WORD GUESSING GAME

Two players take turns entering a single character into the terminal (hot-seat style).

The first player to complete a word longer than three characters loses!

Features / Functional Requirements:
* game builds Trie data structure from dictionary entries (words.txt) to track valid words
* random player selected on start
* input validation prompts users who enter non-letters or more than one letter
* game tracks and displays current word continuation
* letters that do not produce a word continuation result in a strike
* players that get three strikes lose
* players that are forced to complete a word longer than three characters lose

Non-Functional Areas Addressed
* error handling for IO / FileNotFound errors
* (inchoate) modular architecture with (inchoate) service layer
* simple Docker deployment

To Use With Docker:
1. in console enter `make play` to play
2. run `make clean` to cleanup