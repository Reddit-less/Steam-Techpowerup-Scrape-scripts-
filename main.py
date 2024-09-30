import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os

def get_html(url):
    """Retrieve HTML content of the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def sanitize_text(text):
    """Remove non-ASCII characters and extra spaces from the text."""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # non-ASCII characters with a space
    text = re.sub(r'\s+', ' ', text).strip()  #multiple spaces with a single space
    return text

def parse_system_requirements(soup):
    """Extract and sanitize system requirements from the HTML."""
    sys_reqs = {}
    sys_req_blocks = soup.find_all('div', class_='game_area_sys_req', attrs={'data-os': True})

    for block in sys_req_blocks:
        os_type = block['data-os'].capitalize()
        sys_reqs[os_type] = {'Minimum': '', 'Recommended': ''}

        # Parsing minimum requirements
        min_reqs = block.find('div', class_='game_area_sys_req_leftCol')
        if min_reqs:
            min_text = min_reqs.get_text(separator="\n", strip=True)
            sys_reqs[os_type]['Minimum'] = sanitize_text(min_text)

        # Parsing recommended requirements
        rec_reqs = block.find('div', class_='game_area_sys_req_rightCol')
        if rec_reqs:
            rec_text = rec_reqs.get_text(separator="\n", strip=True)
            sys_reqs[os_type]['Recommended'] = sanitize_text(rec_text)

    return sys_reqs

def parse_steam_page(html):
    """Parse the given HTML to extract game name, description, and system requirements."""
    soup = BeautifulSoup(html, 'html.parser')

    #game name
    name_tag = soup.find('div', class_='apphub_AppName')
    game_name = sanitize_text(name_tag.text) if name_tag else "Unknown Game"

    # description
    desc_tag = soup.select_one('div.game_description_snippet')
    description = sanitize_text(desc_tag.text) if desc_tag else "No description available."

    # system requirements
    sys_reqs = parse_system_requirements(soup)

    return {
        "name": game_name,
        "description": description,
        "system_requirements": sys_reqs
    }

def save_all_data_as_json(data, base_directory='B:\\Json info', filename='All_game_information.json'):
    """Save all game data to a single JSON file."""
    os.makedirs(base_directory, exist_ok=True)
    full_path = os.path.join(base_directory, filename)
    with open(full_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"All data saved to {full_path}")

all_game_data = []

urls = [

]



cooldown_seconds = 7  # Cooldown duration in seconds

for url in urls:
    html_content = get_html(url)
    if html_content:
        game_data = parse_steam_page(html_content)
        all_game_data.append(game_data)  #  game data to the list

        # Cooldown to avoid overwhelming the server//Looking like a ddos
        print(f"Waiting for {cooldown_seconds} seconds before the next request...")
        time.sleep(cooldown_seconds)
    else:
        print("Failed to retrieve or parse the game page.")

save_all_data_as_json(all_game_data)
