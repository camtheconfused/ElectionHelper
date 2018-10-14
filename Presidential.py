# SRC Election Helper
# by Cameron Stewart
# Version 0.2
# Test Cases complied by Dane Luo
# Released Under a MIT licenceg

import pandas as pd
import numpy as np
from options import *


def housekeeping():
    """performs various housekeeping functions to ensure that variables exist where they should"""
    header = booths.copy()
    header.insert(len(header),"Total Votes")
    header.insert(0, "Name")
    return header


def gen_dataframe():
    """creates a dataframe with the candidates position and name. Returns A dataframe"""
    candidates = {}
    num_candidates = int(input("How many candidates are there?"))
    header = booths.copy()
    header.insert(len(header),"Total Votes")
    for i in range(num_candidates):
        position = str(chr(i + 65))
        name = input(F"What is the name of candidate {position}")
        candidate = [name]
        for n in range(len(header)):
            candidate.append("")
        candidates[position] = candidate
    pres = pd.DataFrame.from_dict(data=candidates, orient="index")
    header.insert(0, "Name")
    pres.columns = header
    pres.index.name = "Position"
    save(pres)
    return pres


def get_votes(dataframe, candidate="Primary"):
    """Updates the dataframe with the votes of each candidate. Handles either primary or distribution counts.
     dataframe: a DataFrame from the previous count, contains their position, name and booth breakdowns.
     candidate: string containing the candidate's position who has been eliminated from the count, default is "Primary"
     """
    print(dataframe)
    candidates = {}
    # TODO improve the efficiency of this function
    for index, candidate in dataframe.iterrows():
        position = index
        name = candidate[0]
        candidates[position] = [name]
    for index, candidate in dataframe.iterrows():
        position = index
        name = candidate[0]
        votes = []
        for booth in booths:
            votes.append(int(input(F"What is the result of candidate {name} at {booth}?")))
        total = sum(votes)
        votes.append(total)
        votes.insert(0, name)
        candidates[position] = votes
        pres = pd.DataFrame.from_dict(data=candidates, orient="index")
        header = housekeeping()
        pres.columns = header
        pres.index.name = "Position"
        save(pres)
        print("\n")
    votes = []
    for booth in booths:
        votes.append(int(input(F"What is the number of informal votes at {booth}?")))
    position = "Informal Votes"
    name = "Informal Votes"
    total = sum(votes)
    votes.append(total)
    votes.insert(0, name)
    candidates[position] = votes
    pres = pd.DataFrame.from_dict(data=candidates, orient="index")
    header = housekeeping()
    pres.columns = header
    pres.index.name = "Position"
    save(pres)

def get_sheetname(count):
    """returns the name of the sheet. Count is an int or string."""
    if count == 1:
        return "Primary Vote"
    else:
        return "Count_" + str(count)

def get_total(dataframe):
    """returns the total votes"""
    total = sum(dataframe.loc["A":"D", "Total Votes"])
    return total


def get_informal(dataframe):
    """returns the  total informal vote"""
    print("TOdo")
    return None


def check_winner(dataframe, count = 1):
    """Checks if there is a winner, if there is a winner prints their position, name and vote %.
    if there isn't a winner, eliminates the candidate with the lowest vote total and calls get_distribution"""
    total_votes = dataframe.loc["A":"D", "Total Votes"]
    winner = False
    for vote in total_votes:
        if vote > (0.5 * (get_total(dataframe)) + 1):
            print("Winner Found...")
            winner = True
            # TODO add in winner finding code
        else:
            winner = False
    if winner is False:
        print(F"\nNo candidate has a majority on count {count}, going to preferences.")
        lowest_vote = min(total_votes)
        print(dataframe.loc[dataframe["Total Votes"] == lowest_vote,"Name"])
        name = dataframe.loc[dataframe['Total Votes'] == lowest_vote,'Name']
        name = name[0]
        if count == 1:
            print(F"Candidate {name} "
                  F"had the lowest primary vote of {lowest_vote} or"
                  F"{round((lowest_vote/get_total(dataframe))*100,2)}% of votes and has been eliminated")
        count += 1
        get_distribution(dataframe, 2, name, lowest_vote)


def get_distribution(dataframe, count,eliminated, votes):
    """Prompts the user to input the preferences for eliminated candidate, calls check winner"""
    candidates = {}
    preferences = presidential.copy()
    preferences.drop(preferences[preferences.Name == eliminated].index, inplace=True)
    for index, candidate in preferences.iterrows():
        position = index
        name = candidate[0]
        for booth in booths:
            vote = preferences.loc["A", booth]
            vote += int(input(F"What was {eliminated} preference flow for {name} at booth {booth}"))




def save(dataframe, count=1):
    """Saves the dataframe as an xlx
    dataframe is a datrame, count is an int"""
    try:
        writer = pd.ExcelWriter('presidential.xlsx', engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name=get_sheetname(count))
    except IOError:
        # TODO fix exception handling when file is open
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
    except ValueError:
        count = (int(input("Oops, please enter a number")))
    try:
        presidential = pd.read_excel("presidential.xlsx", sheet_name=get_sheetname(count), index_col=0)
    except IOError:
        print("File not Found")
    print("File Loaded")
    print(presidential)
    print("What would you like to do add vote totals,  continue the count, or fix a mistake?")
    response = input("Enter ADD to redo vote totals, CONT to continue the count or FIX to fix a mistake.").upper()
    while not (response == "ADD" or response == "CONT" or response == "FIX" or response == "QUIT"):
        response = input("Invalid response.")
    if response == "ADD":
        get_votes(presidential)
    elif response == "CONT":
        check_winner(presidential, count)
    elif response == "FIX":
        print("TODOO")
    else:
        print("Goodbye!")
        quit()

elif response == "START":
    count = 1
    gen_dataframe()

elif response == "QUIT":
    print("Goodbye!")
    quit()

