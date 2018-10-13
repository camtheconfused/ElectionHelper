# SRC Election Helper
# by Cameron Stewart
# Version 0.2
# Test Cases complied by Dane Luo
# Released Under a MIT licenceg

import pandas as pd
import numpy as np
from options import *

def gen_dataframe():
    """creates a dataframe with the candidates position and name. Returns A dataframe"""
    candidates = {}
    num_candidates = int(input("How many candidates are there?"))
    header = booths.copy()
    header.insert(len(header),"Total Votes")
    for i in range(num_candidates):
        position = str(chr(i + 65))
        position = str(chr(i + 65))
        name = input(F"What is the name of candidate {position}")
        l = [name]
        for n in range(len(header)):
            l.append("")
        candidates[position] = l
    pres = pd.DataFrame.from_dict(data=candidates, orient="index")
    header.insert(0,"Name")
    pres.columns = header
    save(pres)
    return pres



def get_sheetname(count):
    """returns the name of the sheet. Count is an int."""
    if count == 1:
        return "Primary Vote"
    else:
        return "Count_" + str(count)


def save(dataframe):
    """Saves the dataframe as an xlx
    dataframe is a datrame, count is an int"""
    try:
        writer = pd.ExcelWriter('presidential.xlsx', engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name=get_sheetname(count))
    except:
        #TODO fix exception handling when file is open
        print("Warning: 'presidential.xlsx' may be open, please exit.")


print("Welcome to SRC Election Helper - Presidential Edition \n\nThis Script will assist in counting and distributing "
      "the votes for President")
print("Please Note, inputs are not case sensitive, except where noted.")
response = ""
print("\nWhat would you like to do today? Enter LOAD to load an in progress vote, START to begin a new vote"
      "or QUIT")
response = input().upper()
while not (response == "LOAD" or response == "START" or response == "QUIT"):
    response = input("Invalid response.").upper()

if response == "LOAD":
    count = ""
    try:
        count = int(input("What count (number) are you on? Please enter a number"))
    except ValueError:\
        count = (int(input("Oops, please enter a number")))
    try:
        presidential = pd.read_excel("presidential.xlsx", sheet_name=get_sheetname(count), index_col=0)
    except IOError:
        print("File not Found")
    if np.nan in presidential.loc[:,"Total Votes"]:
        print("This works")

elif response == "START":
    count = 1
    gen_dataframe()

elif response == "QUIT":
    print("Goodbye!")
    quit()

