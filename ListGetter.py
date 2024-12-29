import requests
from bs4 import BeautifulSoup
import json
import deckProcessor
import pandas as pd
import itertools as it


class DeckList:
    def __init__(self, leader, url, placement, decklist = None):
        self.leader = leader
        self.url = url
        self.placement = placement

def get_links(url):
    """
    Retrieves all the links from a website.

    Args:
        url (str): The URL of the website.

    Returns:
        A list of links found on the website.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the website
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the anchor tags (links) on the website
    # grab the leader, the decklist, and the placement
    links = soup.find_all('a')
    deckLists = []
    for link in links:
        if (link.get('href').startswith('https://deckbuilder.egmanevents.com/?deck=')):
            deckList = DeckList(link.next_element, link.get('href'), link.previous_element)
            deckLists.append(deckList)

    # Return the List of deckList objects
    return deckLists
def parse_json_file(file_path):
    """
    Reads JSON from a file and parses out the field "Key" based on the field "Category" being equal to "Leader".

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        A list of "Key" values where the "Category" is equal to "Leader".
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    leader_keys = [item['Key'] for item in data if item.get('Category', '') == 'Leader']

    return leader_keys

def return_links_by_leader(links, leaders):
    """
    Returns an object with the leader along with the list of links that include that leader.

    Args:
        links (list): A list of links, where each link is a dictionary with a 'leader' key.
        leaders (list): A list of leaders.

    Returns:
        A list of objects with the leader and the list of links that include that leader.
    """
    result = []
    for leader in leaders:
        leader_links = list(filter(lambda x: any(obj["Card"] == leader for obj in x), links))
        result.append({'leader': leader, 'links': leader_links})

    return result

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

    card_names = [{"Id" : item['Key'], "Name" : item["Card Name"]} for item in data]

    return card_names

def get_deckList_data(url):
    LEADERS = parse_json_file('optcg_op08.json')
    links = get_links(url)
    links = deckProcessor.processDecks(links)
    return links

def update_card_names(listObjects):
    names = get_card_names('optcg_op08.json')
    for deck in listObjects:
        for card in deck.deckList:
            card['Card'] = card['Card'] + ' - ' + list(filter(lambda x: x['Id'] == card["Card"], names))[0]['Name']
    return listObjects

def create_dataframes(output):
    objlists =[]
    unique_leaders = []
    output.sort(key=lambda x: x.leader)
    grouped_deck_lists = it.groupby(output, key=lambda x: x.leader)

    for k, g, in grouped_deck_lists:
        objlists.append({'leader': k, 'decks': list(g)})

    dataframes = []
    for obj in objlists:
        leader = obj['leader']
        links = obj['decks']
        lists = [link.deckList for link in links]
                  
        # Get unique card values
        cards = list(set([link['Card'] for sublist in lists for link in sublist]))

        # Create a dictionary to store the data
        data = {'Card': cards}

        # Calculate the average count for each card
        avg_counts = {}
        for card in cards:
            counts = [link['Count'] for sublist in lists for link in sublist if link['Card'] == card]
            avg_counts[card] = round(sum(counts) / len(links), 2)
        data['Average Count'] = [avg_counts.get(card, 0) for card in cards]

        # Add the count for each list
        for deck in links:
            counts = []
            for card in cards:
                count = [list['Count'] for list in deck.deckList if list['Card'] == card]
                counts.append(count[0] if count else 0)
            data[f'{deck.placement[:-2]}'] = counts

        # Create the DataFrame
        df = pd.DataFrame(data)
        df.columns = ['Card', 'Average Count'] + [f'{deck.placement[:-2]}' for deck in links]

        # Set the title of the DataFrame
        df.title = leader

        dataframes.append(df)

    return dataframes

url = ''
links = get_deckList_data(url)
lists = update_card_names(links)
dataframes = create_dataframes(lists)
html_string= '<h1> title </h1>'
for df in dataframes:
    html_string += f'<h2> {df.title} </h2>'
    html_string += df.to_html()
    html_string += '\n'
    print(df.title)
    print(df)
    print('\n')

with open('output.html', 'w') as f:
    f.write(html_string)

def do_it_all(url):
    links = get_deckList_data(url)
    lists = update_card_names(links)
    dataframes = create_dataframes(lists)
    return dataframes