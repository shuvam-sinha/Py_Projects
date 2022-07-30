# def print_table(table):
#     if len(table) is not 9:
#         print ("There needs to be 9 elements in the list")
#     else:
#         print (table[0] + " | " + table[1] + " | " + table[2])
#         print ("---------")
#         print (table[3] + " | " + table[4] + " | " + table[5])
#         print ("---------")
#         print (table[6] + " | " + table[7] + " | " + table[8])
# from random import seed
# from random import randint
import random
import time

def print_table(table):
    if len(table) is not 9:
        print ("There needs to be 9 elements in the list")
    else:
        for i in range(0, len(table)/3):
            print (table[i*3] + " | " + table[i*3+1] + " | " + table[i*3+2])
            if i is not 2:
                print ("---------")


def get_user_input(table):
    user_answer = input("Where do you want to place your token?\n")
    user_answer = int(user_answer) - 1
    if validate(table, user_answer):
        table[user_answer] = "X"
        return table
    else:
        print ("Incorrect input, try again.")
        return get_user_input(table)


def get_computer_input(table):
    computer_spot = get_valid_spot(table, "O")
    user_spot = get_valid_spot(table, "X")
    if computer_spot is not None:
        computer_answer = computer_spot
    elif user_spot is not None:
        computer_answer = user_spot
    else:
        random.seed(time.time())
        computer_answer = random.randint(0, 8)

    if validate(table, computer_answer):
        print ("Computer's input")
        table[computer_answer] = "O"
        return table
    else:
        return get_computer_input(table)


def is_complete(table, answer):
    if (
            (table[0] == answer and table[1] == answer and table[2] == answer) or
            (table[3] == answer and table[4] == answer and table[5] == answer) or
            (table[6] == answer and table[7] == answer and table[8] == answer) or
            (table[0] == answer and table[3] == answer and table[6] == answer) or
            (table[1] == answer and table[4] == answer and table[7] == answer) or
            (table[2] == answer and table[5] == answer and table[8] == answer) or
            (table[0] == answer and table[4] == answer and table[8] == answer) or
            (table[2] == answer and table[4] == answer and table[6] == answer)
    ):
        return True
    else:
        return False


def get_valid_spot(table, answer):
    option1 = get_this_valid_spot(table, 0, 1, 2, answer)
    option2 = get_this_valid_spot(table, 3, 4, 5, answer)
    option3 = get_this_valid_spot(table, 6, 7, 8, answer)
    option4 = get_this_valid_spot(table, 0, 3, 6, answer)
    option5 = get_this_valid_spot(table, 1, 4, 7, answer)
    option6 = get_this_valid_spot(table, 2, 5, 8, answer)
    option7 = get_this_valid_spot(table, 0, 4, 8, answer)
    option8 = get_this_valid_spot(table, 2, 4, 6, answer)
    if option1 is not None:
        return option1
    elif option2 is not None:
        return option2
    elif option3 is not None:
        return option3
    elif option4 is not None:
        return option4
    elif option5 is not None:
        return option5
    elif option6 is not None:
        return option6
    elif option7 is not None:
        return option7
    elif option8 is not None:
        return option8
    else:
        return None


def get_this_valid_spot(table, x, y, z, answer):
    total_true = int(table[x] == answer) + int(table[y] == answer) + int(table[z] == answer)
    if total_true == 2:
        if table[x] == " ":
            return x
        elif table[y] == " ":
            return y
        elif table[z] == " ":
            return z
        else:
            return None
    else:
        return None


def validate(table, answer):
    # return table[answer] == " "
    if table[answer] == " ":
        return True
    else:
        return False


if __name__ == '__main__':
    table = [" "] * 9
    print_table(table)
    random.seed(time.time())
    user_or_computer = random.randint(0, 1)
    if user_or_computer == 0:
        for i in range(0, len(table)/2):
            table = get_user_input(table)
            print_table(table)
            if is_complete(table, "X"):
                print ("User wins")
                exit(0)
            table = get_computer_input(table)
            print_table(table)
            if is_complete(table, "O"):
                print ("Computer wins")
                exit(0)
        table = get_user_input(table)
        print_table(table)
        if is_complete(table, "X"):
            print ("User wins")
            exit(0)
        else:
            print ("Game drawn")
            exit(0)
    else:
        for i in range(0, len(table)/2):
            table = get_computer_input(table)
            print_table(table)
            if is_complete(table, "O"):
                print ("Computer wins")
                exit(0)
            table = get_user_input(table)
            print_table(table)
            if is_complete(table, "X"):
                print ("User wins")
                exit(0)
        table = get_computer_input(table)
        print_table(table)
        if is_complete(table, "O"):
            print ("Computer wins")
            exit(0)
        else:
            print ("Game drawn")
            exit(0)
