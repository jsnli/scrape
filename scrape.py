from bs4 import BeautifulSoup
import requests
import json
import os

base = "http://darksouls.wikidot.com"
page = requests.get(f"{base}/weapons")
soup = BeautifulSoup(page.content, "html.parser")

content = soup.select_one("#page-content")
td = content.select("td")[1]
links = td.select("a")

os.mkdir(f"{os.getcwd()}/data")


def get_key_index(arr, value):
    try:
        return arr.index(value)
    except ValueError as ve:
        return -1


def scrape_weapon_data(url):
    weapon_page = requests.get(url)
    weapon_page_soup = BeautifulSoup(weapon_page.content, "html.parser")
    weapon_page_content = weapon_page_soup.select_one("#page-content")
    table = weapon_page_content.select(".wiki-content-table")
    headers = table[0].select("th")
    keys = []
    values = table[0].select("td")
    for index, th in enumerate(headers):
        keys.append(th.text.replace("\n", " "))
    weapon_dictionary = {}
    # region parse and insert name
    name_index = get_key_index(keys, "Name")
    if name_index > 0:
        weapon_dictionary[keys[name_index]] = values[name_index].text
    else:
        return
    # endregion

    # region parse and insert description
    description = ""
    description_start = weapon_page_content.find("h2")
    for sibling in description_start.next_siblings:
        if hasattr(sibling, 'name'):
            if sibling.name == "h2":
                break
            if sibling.name == "p":
                description += sibling.text + " "
    description = description.replace('\r', ' ').replace('\n', ' ')
    description = description[:-1]

    weapon_dictionary["Description"] = description
    # endregion

    # region parse and insert damage
    damage_index = get_key_index(keys, "Damage")
    if damage_index > 0:

        breaks = values[damage_index].findAll("br")
        for br in breaks:
            br.decompose()

        damage = values[damage_index].text.split('\n')
        damage[:] = [d for d in damage if d]
        damage_stats = damage[0].split('/')
        damage_type = "-"
        if len(damage) == 2:
            damage_type = damage[1]
        if len(damage) == 3:
            damage_type = damage[2]

        damage_type = damage_type.replace("(", "").replace(")", "")
        weapon_dictionary["Damage"] = {
            "Stats": {
                "Physical": damage_stats[0],
                "Magical": damage_stats[1],
                "Fire": damage_stats[2],
                "Lightning": damage_stats[3]
            },
            "Type": damage_type
        }
    # endregion

    # region parse and insert critical
    critical_index = get_key_index(keys, "Critical")
    if critical_index > 0:
        weapon_dictionary[keys[critical_index]] = values[critical_index].text
    # endregion

    # region parse and insert durability
    durability_index = get_key_index(keys, "Durability")
    if durability_index > 0:
        weapon_dictionary[keys[durability_index]] = values[durability_index].text
    # endregion

    # region parse and insert weight
    weight_index = get_key_index(keys, "Weight")
    if weight_index > 0:
        weapon_dictionary[keys[weight_index]] = values[weight_index].text
    # endregion

    # region parse and insert stats
    stats_index = get_key_index(keys, "Stats Needed Stat Bonuses")
    if stats_index > 0:
        breaks = values[stats_index].findAll("br")
        for br in breaks:
            br.decompose()
        sups = values[stats_index].findAll("sup")
        for sup in sups:
            sup.decompose()
        stats = values[stats_index].text.split('\n')
        stats[:] = [s for s in stats if s]

        stats_requirements = stats[0].split('/')
        stats_bonuses = stats[1].split('/')
        weapon_dictionary["Stats"] = {
            "Requirements": {
                "Strength": stats_requirements[0],
                "Dexterity": stats_requirements[1],
                "Intelligence": stats_requirements[2],
                "Faith": stats_requirements[3]
            },
            "Bonuses": {
                "Strength": stats_bonuses[0],
                "Dexterity": stats_bonuses[1],
                "Intelligence": stats_bonuses[2],
                "Faith": stats_bonuses[3]
            }
        }
    # endregion

    # region parse and insert damage reduction
    reduction_index = get_key_index(keys, "Damage Reduction %")
    if reduction_index > 0:
        reduction = values[reduction_index].text.split('/')
        weapon_dictionary["Reduction"] = {
            "Physical": reduction[0],
            "Magical": reduction[1],
            "Intelligence": reduction[2],
            "Faith": reduction[3]
        }
    # endregion

    # region parse and insert stability
    stability_index = get_key_index(keys, "Stability")
    if stability_index > 0:
        weapon_dictionary[keys[stability_index]] = values[stability_index].text
    # endregion

    # region write to file
    json_object = json.dumps(weapon_dictionary, indent=4)

    filename = ''.join(weapon_dictionary["Name"].split()).lower().replace("'","").replace("-","")
    print(f"writing to file {filename}")
    with open(f"{os.getcwd()}/data/{filename}.json", "w") as outfile:
        outfile.write(json_object)
    # endregion


for link in links:
    scrape_weapon_data(f"{base}{link["href"]}")
