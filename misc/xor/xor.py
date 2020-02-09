import random

def random_binary(n):
    return random.getrandbits(n)

def count_ones(x):
    binary = f'{x:032b}'
    cnt = 0
    for bit in binary:
        if int(bit):
            cnt += 1
    return cnt

# randomly select the secret number s
s = random_binary(32)

def find_s():
    """
    this function guesses s with only two operations:
        1) Xor a chosen number with s
        2) count the 1s in the Xor result
    """

    ones_in_s = count_ones(0^s) # s Xor 0 = s
    x_list = [2**n for n in range(32)][::-1] # build x choices list

    s_guess = b'' # create variable to store guesses in

    for x in x_list: # run through choices and guess s
        if count_ones(x^s) > ones_in_s:
            s_guess += b'0'
        elif count_ones(x^s) < ones_in_s:
            s_guess += b'1'

    return int(s_guess, 2)

guessed_s = find_s()

if guessed_s == s:
    print("You guessed s!")
    print(f"Actual s: {s:032b}")
    print(f"Guessed s: {guessed_s:032b}")
