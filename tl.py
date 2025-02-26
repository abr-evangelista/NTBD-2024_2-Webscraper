import json
import re
import sqlite3

def split_address(address):
    parts = [part.strip() for part in address.split(",")]

    # If there are more than 3 parts, concatenate all except the last two
    if len(parts) > 3:
        # Concatenate all parts except the last two into the first part
        parts = [", ".join(parts[:-2])] + parts[-2:]

    first_part = parts[0]
    first_split = re.split(r"(\d+)\s", first_part, maxsplit=1)[1:]

    state_part = parts[-1].split(" ")[0]

    final_parts = first_split + parts[1:-1] + [state_part]

    return final_parts

with open("rawdealerdata.json", "r") as file:
    data = json.load(file)

listDealers = []
listLocals = []
entryCount = 1
for list in data:
    for entry in list:
        name = entry.get("name")
        localization = entry.get("localization")
        bfh = entry.get("bfh")

        newlocal = split_address(localization)
        newlocal.append(entryCount)
        listLocals.append(newlocal)

        newDealer = []
        newDealer.append(entryCount)
        newDealer.append(name)
        newDealer.append(entryCount)
        newDealer.append(bfh)
        listDealers.append(newDealer)
        entryCount += 1

with open("dealerdata.json", "w") as file:
        json.dump(listDealers, file)

with open("localdata.json", "w") as file:
        json.dump(listLocals, file)

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()


with open("localdata.json", "r") as file:
    data = json.load(file)
for entry in data:
    print(entry)
    try:
        cursor.execute("""
            INSERT INTO Localizacao (Numero, Rua, Cidade, Estado, PK_Localizacao)
            VALUES (?, ?, ?, ?, ?)
        """, entry)
    except:
        print("Formato errado! Inserindo outras entradas....")
        continue

with open("dealerdata.json", "r") as file:
    data = json.load(file)
for entry in data:
    print(entry)
    try:
        cursor.execute("""
            INSERT INTO Negociante (PK_Negociante, Nome, FK_Localizacao, Buy_from_home)
            VALUES (?, ?, ?, ?)
        """, entry)
    except:
        print("Formato errado! Inserindo outras entradas....")
        continue

# Commit changes and close connection
conn.commit()
conn.close()
