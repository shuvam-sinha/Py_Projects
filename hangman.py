from copy import copy
from random import randint

def readFile(filename):
    contents = []
    with open(filename, 'r') as reader:
        contents = reader.readlines()
    return contents


def random_word(contents):
    final_word_selection = contents[randint(0, len(contents)-1)]
    hint_and_word = final_word_selection.split(":")
    if len(hint_and_word) != 2:
        random_word(contents)
    return hint_and_word[0], hint_and_word[1].strip("\n")


def to_dictionary(contents):
    answers = dict()
    for token in contents:
        hint_and_word = token.split(":")
        answers[hint_and_word[1].strip("\n")] = hint_and_word[0].strip("\n")
    return answers


def print_dictionary(my_dictionary):
    for key, value in my_dictionary.items():
        print key, '->', value


def play_game(hint, answer):
    number_of_tries = len(answer)*2
    print ("The word has " + str(len(answer)) + " letters.")
    print ("You have " + str(number_of_tries) + " tries")
    print ("Hint: " + hint)
    print ("Answer: " + answer)
    print ("Try to guess the word.")
    dashes = ["_"] * (len(answer))
    points = 1000

    tries = 0
    failures = 0
    while tries < number_of_tries:
        dashes, points, failures = get_user_input(answer.lower().strip(), dashes, points, failures)
        if "_" in dashes:
            if tries == number_of_tries-1:
                print ("The number of tries has expired. You lost.")
        else:
            print ("You have found the word successfully. Good job.")
            break
        tries = tries + 1
    return tries


def get_user_input(answer, dashes, points, failures):
    user_guess = raw_input("What letter do you guess?\n")
    user_guess = user_guess.lower()
    orig_dashes = copy(dashes)
    if len(user_guess) != 1:
        if user_guess == answer:
            failures = failures - 1
            dashes = list(user_guess)
        else:
            print ("That is wrong. Please try again...")
            failures = failures + 1
    else:
        for position in range(0, len(answer)):
            print(str(position) + ":" + user_guess + ":" + answer[position])
            if user_guess == answer[position]:
                print ("There is a " + user_guess + " in the word.")
                dashes[position] = user_guess

        if orig_dashes == dashes:
            failures = failures + 1
        else:
            if failures > 0:
                failures = failures - 1

        print (dashes)

    if orig_dashes == dashes:
        if points > 200:
            points = points - 2 ** failures
        else:
            points = points - 10 * failures

        if points <= 200:
            if points <= 0:
                print (points)
                print ("Game over")
                exit(0)
            else:
                failures = 0

    print ("You have " + str(points) + " points")
    return dashes, points, failures


if __name__ == '__main__':
    contents = readFile("words.txt")
    (hint, answer) = random_word(contents)
    my_dictionary = to_dictionary(contents)
    print_dictionary(my_dictionary)
    #play_game(hint, answer)

