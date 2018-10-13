President ElectionHelper

Uses optional preferential voting.

Inspired by the University of Sydney Student Representative Council election. 
Testing data compiled by Dane Luo.

Requires: List of booth names.

1. Checks if a dataframe exists. 
1 a. if not, prompts the user to enter the data.
1 b. Generates an empty spreadsheet containing the Candidates Name's and ballot position.
1 c. asks the user if they wish to enter vote totals.
2. loops through each candidate and adds their votes at each booth to the dataframe.
3. Totals the votes for each candidate and adds to the dataframe.
4. Checks whether a candidate has recieved a majority (50% + 1) of the total formal votes
4. a) if there is a winner, displays the winner and their total votes.
4. b) if there isn't a winner, displays the candidate with the lowest votes and eliminates.
5. Prompts the user to input their redistributed votes. Goes to 4. Repeats step 4 and 5 until there is a winner.

While this program is running, it saves regularly to a excel spreadsheet. The spreadsheet should not be open whilst
the program is running as that will prevent saving. It may be opened safely whilst input is requested from the user 
providing that it is closed before the input is entered.
