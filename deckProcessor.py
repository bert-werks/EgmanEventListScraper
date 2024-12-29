import numpy as np
import pandas as pd
import json

def get_card_names(file_path):
    """
    Reads JSON from a file and parses out the field "Key" based on the field "Category" being equal to "Leader".

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        A list of "Key" values where the "Category" is equal to "Leader".
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    card_names = [{item['Key'], item["Card Name"]} for item in data]

    return card_names


def processDecks(decks):
    for deck in decks:
        split = deck.url.split("=")
        deckL = split[1]
        url = deckL.split("&")
        cards = url[0].split(",")
        deckList = []
        for card in cards:
            splitcard = card.split(":")
            deckList.append({"Card": splitcard[0], "Count": int(splitcard[1])})

        deck.deckList = deckList

    return decks

def create_table(dict_list):
    """
    Creates a table from a list of dictionaries.

    Args:
        dict_list (list of dictionaries): The list of dictionaries.

    Returns:
        A pandas DataFrame representing the table.
    """
    # Get the unique keys from the dictionaries
    keys = set()
    for d in dict_list:
        keys.update(d.keys())
    keys = list(keys)

    # Create a list to store the data
    data = []

    # Iterate over the keys
    for key in keys:
        # Get the values for the key from the dictionaries
        values = [d.get(key, 0) for d in dict_list]

        # Calculate the average of the values
        avg = sum(values) / len(values)

        # Add the data to the list
        data.append([key, avg] + values)

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=['Key', 'Average'] + [f'Dict {i+1}' for i in range(len(dict_list))])
    print(df)
    return df

def print_matrix(matrix):
    """
    Prints a matrix to the console.

    Args:
        matrix (list of lists): The matrix to print.
    """
    for row in matrix:
        print(" | ".join(str(x) for x in row))
        print("-" * (len(row) * 4 - 1))
