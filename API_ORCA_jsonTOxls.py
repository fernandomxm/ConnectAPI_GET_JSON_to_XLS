import json
import pandas as pd
import requests
import openpyxl
from openpyxl import Workbook
from pprint import pprint

# ______________________________________________________________________________________________________

headers = {"Authorization": "Token "}
response = requests.get("https://api.orcasecurity.io/api/alerts?state.risk_level=critical,high", headers=headers)

if response.status_code == 200:
    new_data = response.json()

    try:
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    existing_data.append(new_data)

    with open("data.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
        print("Arquivo data.json criado com sucesso!")
else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)
# ________________________________________________________________________________________________________

json_file = "data.json"
xlsx_file = "data.xlsx"

with open(json_file, "r", encoding="utf-8") as file:
    json_data = json.load(file)

records = json_data[0].get("data", [])  # Pegamos a lista de registros
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Alertas"
headers = ["Nome_Conta", "Titulo", "Descricao", "Severidade"]
ws.append(headers)

for record in records:
    ws.append([
        record.get("account_name", "N/A"),
        record.get("description", "N/A"),
        record.get("details", "N/A"),
        record.get("state", {}).get("risk_level", "N/A")  # Lidando com JSON aninhado
    ])

wb.save(xlsx_file)
print(f"Arquivo {xlsx_file} criado com sucesso!")
