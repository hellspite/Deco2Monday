# Python script to export orders from DecoNetwork into Monday tasks

import deco
import monday


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    orders = deco.get_orders()
    print(f"Number of orders retrieved from Deco: {len(orders)}")
    monday.write_new_orders(orders)
