# Python script to export orders from DecoNetwork into Monday tasks

import sys
import deco
import monday


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    days_back = 14
    no_write = False

    argv1 = sys.argv[1]
    if type(argv1) is int:
        days_back = argv1
    elif type(argv1) is str:
        if argv1 == "no-write":
            no_write = True

    if len(sys.argv) > 2:
        argv2 = sys.argv[2]

        if type(argv2) is str:
            if argv2 == "no-write":
                no_write = True

    orders = deco.get_orders(days_back)
    print(f"Number of orders retrieved from Deco: {len(orders)}")
    if no_write:
        print("#-- No write mode --#")
        for order in orders:
            print(f"- Order {order['order_id']} \n")
    else:
        monday.write_new_orders(orders)
