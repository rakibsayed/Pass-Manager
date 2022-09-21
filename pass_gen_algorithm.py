import math
from random import *
import pyperclip

lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u',
              'v', 'w', 'x', 'y', 'z']
upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
              'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '/', '|', '@']

LABEL_FONT = ("Century Gothic", 13, "bold")
logo_dict = {
    'google': 'gmail_logo.png',
    'amazon': 'amazon_logo.png',
    'microsoft': 'outlook_logo.png',
    'twitter': 'twitter_logo.png',
}


def generate_pass(pass_range, all_keys, password_entry, division=4):
    password_list = []
    shuffle(all_keys)
    for key in all_keys:
        if all_keys.index(key) == len(all_keys) - 1:
            pass_key_range = int(pass_range)
        else:
            pass_key_range = math.ceil(pass_range / division)
        temp_pass_list = [choice(key) for _ in range(pass_key_range)]
        password_list += temp_pass_list
        division -= 1
        pass_range -= pass_key_range

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)
