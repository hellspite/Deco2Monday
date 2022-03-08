import requests
import os
import json

API_URL = "https://api.monday.com/v2"
API_KEY = os.environ["MONDAY_API"]
BOARD_ID = "2241731758"
GROUP_ID = "nuovo_gruppo74198"
headers = {"Authorization": API_KEY}

query = '{ boards (ids: 2241731758) {name id description columns{id title}} }'
# query = "mutation ($myItemName: String!, $boardId: Int!, $groupId: String!, $columnVals: JSON!) " \
#         "{ create_item (board_id:$boardId, item_name:$myItemName, " \
#         "group_id:$groupId, column_values:$columnVals) { id } }"
# query_vars = {
#     "myItemName": "TEST TEST TEST",
#     "boardId": int(BOARD_ID),
#     "groupId": GROUP_ID,
#     "columnVals": json.dumps({
#         "numero_d_ordine": "",
#         "nome_cliente": "cliente test",
#         "data_dell_ordine": "",
#         "data_di_consegna_o_spedizione3": "",
#         "priority": ""
#     })
# }
data = {'query': query}

response = requests.post(url=API_URL, json=data, headers=headers)

print(response.json())
