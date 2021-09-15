from __future__ import annotations
from random import randint
import re
import os
import sys
from typing import List

VALID_GUESS_RE = re.compile(r'^[a-z]$')

class Trie:
    def __init__(self, value):
        self.children = {}
        self.value = value

    def put_child(self, value):
        child = self.children.get(value)
        if not child:
            child = Trie(value)
            self.children[value] = child
        return child
    
    def get_child(self, value) -> Trie:
        return self.children.get(value)
    
    def is_leaf(self):
        return len(self.children) == 0

    @classmethod
    def from_list(cls, list: List[str]):
        result = Trie('')
        for item in list:
            pointer = result
            for char in item:
                pointer = pointer.put_child(char)
        return result


class Player:
    def __init__(self, name):
        self.name = name
        self.hit_points = 3
    
    def hit(self):
        self.hit_points -= 1

    @property
    def dead(self):
        return self.hit_points <= 0


class WordService:
    @classmethod
    def get_words(cls, filename):
        # assumes that the word source is in the same directory as the application
        try:
            with open(os.path.join(sys.path[0], filename)) as file:
                return list(map(lambda line: line.rstrip(), file.readlines()))
        except FileNotFoundError:
            print('Fatal error while reading file: file not found')
            sys.exit(1)
        except IOError:
            print('Fatal error while reading file')
            sys.exit(1)


class Game:
    def __init__(self, dictionary_source_file):
        self.dictionary = self.get_dictionary(dictionary_source_file)
        self.dictionary_pointer: Trie = self.dictionary

        self.players = [Player('A'), Player('B')]
        self.turn = randint(0, len(self.players) - 1)   # index into the players
        
        self.current_word = ''
        self.word_length = 0
        
        self.play()

    def get_dictionary(self, dictionary_source_file):
        return Trie.from_list(self.get_words(dictionary_source_file))

    def get_words(self, dictionary_source_file):
        return WordService.get_words(dictionary_source_file)
    
    def validate_guess_syntax(self, validandum):
        if not VALID_GUESS_RE.match(validandum): return False
        return True

    def validate_guess_semantics(self, validandum):
        return self.dictionary_pointer.get_child(validandum) is not None

    def advance_word(self, guess):
        next_entry = self.dictionary_pointer.get_child(guess)
        self.dictionary_pointer = next_entry if next_entry else self.dictionary_pointer
        self.current_word += guess if next_entry else ''
        self.word_length += 1 if next_entry else 0
    
    def has_loss_condition(self):
        return self.dictionary_pointer.is_leaf() and self.word_length > 3
    
    def next_turn(self):
        self.turn = (self.turn + 1) % 2
    
    @property
    def current_player(self):
        return self.players[self.turn]
    
    def play(self):
        while True:
            guess = input(f'Turn for {self.current_player.name} (building word \'{self.current_word}\'):\n')

            if not self.validate_guess_syntax(guess):
                print('input must be a single letter from a-z')
                continue
            
            if not self.validate_guess_semantics(guess):
                print('character entered is not associated with a continuation of the current word')
                self.current_player.hit()
                if self.current_player.dead:
                    print(f'Player {self.current_player.name} lost -- 3 incorrect guesses')
                    break
                print(f'try again ({self.current_player.hit_points} guesses remaining)')

            self.advance_word(guess)
            if self.has_loss_condition():
                print(f'Player {self.current_player.name} lost by completing a word: {self.current_word}')
                break

            self.next_turn()


if __name__ == '__main__':
    Game('words.txt')