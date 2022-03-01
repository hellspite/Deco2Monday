# Python script to export orders from DecoNetwork into Monday tasks

import deco


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    orders = deco.get_orders()
    print(len(orders))
    for order in orders:
        print(order["order_id"])
