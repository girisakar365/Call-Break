from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ['Bid', 'Total Point','Cards']

def show_table(bid: float or int, tp: float or int, card: str):
    table.add_row((str(bid), str(tp), card))
    print(table)