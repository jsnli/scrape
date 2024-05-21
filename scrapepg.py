# import requests
# import soupsieve
# import psycopg2
# from bs4 import BeautifulSoup
#
# connection = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="1234", port=5432)
# cursor = connection.cursor()
# cursor.execute("""DROP TABLE IF EXISTS shortsword""")
# cursor.execute("""CREATE TABLE IF NOT EXISTS shortsword (
#     upgrade VARCHAR(255),
#     physical_attack VARCHAR(255),
#     magic_attack VARCHAR(255),
#     fire_attack VARCHAR(255),
#     lightning_attack VARCHAR(255),
#     strength CHAR,
#     dexterity  CHAR,
#     faith CHAR,
#     intelligence CHAR,
#     divine CHAR,
#     occult CHAR,
#     physical_defense VARCHAR(255),
#     magic_defense VARCHAR(255),
#     fire_defense VARCHAR(255),
#     lightning_defense VARCHAR(255),
#     stability VARCHAR(255)
# );
# """)
#
# insertSQL = ("INSERT INTO shortsword (upgrade, physical_attack, magic_attack, fire_attack, lightning_attack, strength, "
#              "dexterity, faith, intelligence, divine, occult, physical_defense, magic_defense, fire_defense, "
#              "lightning_defense, stability) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")
#
# url = "https://darksouls.wiki.fextralife.com/Shortsword"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")
#
# wikicontentblock = soup.find(id="wiki-content-block")
#
# tab = wikicontentblock.select_one(f".tabcontent.{soupsieve.escape('1-tab')}")
# rows = tab.select(".table-responsive .wiki_table tbody tr")
#
# print("Shortsword data")
# for row in rows[2:]:
#     data = []
#     cells = row.select("th, td")
#     for cell in cells:
#         data.append(cell.text)
#     print(tuple(data))
#
#     cursor.execute(insertSQL, data)
#
# connection.commit()
# cursor.close()
# connection.close()