# SRC Election Helper
# by Cameron Stewart
# Version 0.1
# Test Cases complied by Dane Luo
# Released Under a MIT licence


def gen_file():
    """
    builds a spreadsheet for the presidential count. relies on user input.
    Returns a pandas spreadsheet that is also saved to the directory as presidential.xlsx
    """
    candidates = {"Position": columns}

    num_candidates = int(input("How many candidates are there?"))
    for i in range(num_candidates):
        total = 0
        position = str(chr(i+65))
        name = input(F"What is the name of candidate {position}")
        counts = [name]
        for n in range(len(booths)):
            count = int(input(F"What is the result of candidate {name} at {booths[n]}?"))
            counts.append(count)
        for i in counts:
            if type(i) == int:
                total += i
        counts.append(total)
        candidates[position] = counts
    counts = ["Informal"]
    for n in range(len(booths)):
        count = int(input(F"What is the number of informal votes  at {booths[n]}?"))
        counts.append(count)
    total = 0
    for i in counts:
        if type(i) == int:
            total += i
    counts.append(total)
    candidates["Informal"] = counts
    pres = pd.DataFrame.from_dict(data=candidates, orient="index")
    print(pres)
    # if input("Would you like to correct a mistake?") == "Y":
    # TODO add in correction
    writer = pd.ExcelWriter('presidential.xlsx', engine='xlsxwriter')
    pres.to_excel(writer, sheet_name='presidential.xlsx')
    writer.save()

    return pres

def distribute(candidate):
    """
    Allocates the preferences of an eliminated candidate and modifies the count.
    Candidate is the name of eliminated candidate.
    """


import pandas as pd
import os
import xlsxwriter

# This program distributes the Presidential Votes according to an optional preferential system.

# To change the booths, adjust this line. Note booth names should be enclosed by "" followed by a , (comma)
booths = ["Pre-Poll", "JFR", "Fisher", "Manning", "Cumberland", "Engineering","SCA", "Conservatorium", "Declaration",
          "Postal"]

columns = ["Name"]
for i in booths:
    columns.append(i)
columns.append("Total Votes")
print("Welcome to Election Helper. This Script assists with the count and distribution of the Presidential Count")
file = os.path.isfile("presidential.xlsx")
if file:
    presidential = pd.read_excel("presidential.xlsx")
    print("Loaded presidential spreadsheet")
    print(presidential)
else:
    print("Presidential spreadsheet not found")
    response = input("Would you like to generate it? Y/N")
    response = response.upper()
    # TODO fix up non y/n responses.
    if response == "Y":
        presidential = gen_file()

# Begin the elimination and distributed process.
# Drop informal votes
total = sum(presidential.iloc[1:6,11])
informal = presidential.iloc[5,11]
print(F"\nRemoving informal votes, there were {total} informal votes or {round(informal/total *100)}% of ballots issued.")
presidential.drop(labels="Informal",inplace=True)

print("\nFirst Count")
primary = presidential.iloc[1:5,11]
Winner = False
for count in primary:
    if count > (0.5 * total  + 1):
        print("Winner Found...")
        Winner = True
        # TODO add in winner finding code
    else:
        Winner = False
if Winner is False:
    print("No candidate has a majority on count 1, going to preferences.")
lowest = (min(presidential.iloc[1:5,11]))
remove = (presidential.loc[presidential[11] == lowest])
remove = str(remove[0])
remove = remove.split()
remove = str(remove[1])
print(F"Candidate {remove} was eliminated having received a primary vote of {lowest}")
presidential.drop(labels=remove[0], inplace=True)




