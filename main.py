# Python script to export orders from DecoNetwork into Monday tasks

import sys
import deco
import monday


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    try:
        days_back = int(sys.argv[1])
    except:
        days_back = 14
    orders = deco.get_orders(days_back)
    print(f"Number of orders retrieved from Deco: {len(orders)}")
    monday.write_new_orders(orders)
