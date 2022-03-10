import requests
import os
import json

API_URL = "https://api.monday.com/v2"
API_KEY = os.environ["MONDAY_API"]
BOARD_ID = "2241731758"
GROUP_ID = "nuovo_gruppo74198"
headers = {"Authorization": API_KEY}

# query = '{ boards (ids: 2241731758) {name id description columns{id title}} }'


def write_new_orders(orders):
    """input list
    return boolean

    Take a list of orders from Deco and generate new items on Monday.com
    """

    for order in orders:
        try:
            if order["is_priority"] == "true":
                is_priority = "Tassativo"
            else:
                is_priority = ""

            query = "mutation ($myItemName: String!, $boardId: Int!, $groupId: String!, $columnVals: JSON!) " \
                    "{ create_item (board_id:$boardId, item_name:$myItemName, " \
                    "group_id:$groupId, column_values:$columnVals) { id } }"
            query_vars = {
                "myItemName": order["job_name"],
                "boardId": int(BOARD_ID),
                "groupId": GROUP_ID,
                "columnVals": json.dumps({
                    "numero_d_ordine": str(order["order_id"]),
                    # "nome_cliente": "cliente test",
                    "data_dell_ordine": order["date_ordered"][:-9],
                    "data_di_consegna_o_spedizione3": order["date_due"][:-9],
                    "priority": is_priority
                })
            }

            data = {'query': query, 'variables': query_vars}

            response = requests.post(url=API_URL, json=data, headers=headers)

            print(response.json())
        except TypeError:
            print(f"TypeError with order: {order['order_id']}")
