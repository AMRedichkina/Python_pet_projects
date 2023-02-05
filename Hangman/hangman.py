'''
The hangman game is a word guessing game
where the player is given a word and
has to guess the letters that make up the word.
The player is given a certain number of tries
(no more than 6 wrong guesses are allowed)
to guess the correct letters before the game is over.
'''
# Output
'''
You have 6 tries left.
Used letters:
Word: _ _ _ _
Guess a letter: a

You have 6 tries left.
Used letters: a
Word: _ a _ a
Guess a letter: j

You have 6 tries left.
Used letters: j a
Word: j a _ a
Guess a letter: v
You guessed the word java !
'''

tries = 6
word = 'j a v a'
empty_word = '_ _ _ _'
list_1 = []


def get_new_letter(list_1):
    """
    Function to get a new letter from the player
    """
    while True:
        try:
            new_letter = input('Guess a letter: ')
            if not new_letter.isalpha():
                raise ValueError("Invalid input, enter an alphabet.")
            if new_letter in list_1:
                print("Letter has already been used, enter a different letter:")
            else:
                break
        except ValueError as e:
            print(e)
    list_1.append(new_letter)
    return new_letter


def update_empty_word(word, empty_word, new_letter):
    """
    Function to update the empty word.
    """
    indexes = [i for i, x in enumerate(word) if x == new_letter]
    empty_word = list(empty_word)
    for i in indexes:
        empty_word[i] = new_letter
    empty_word = "".join(empty_word)
    return empty_word


if __name__ == "__main__":
    """
    Main function.
    """
    while tries > 0:
        print(f'You have {tries} tries left.')
        print("Used letters: " + " ".join(list_1))

        new_letter = get_new_letter(list_1)
        empty_word = update_empty_word(word, empty_word, new_letter)

        print(f'Word:{empty_word}')

        if empty_word == word:
            print('You guessed the word java !')
            break

        tries -= 1

    print('The word is not guessed !')
