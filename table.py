from prettytable import PrettyTable

table = PrettyTable()
table.field_names = ['Bot', 'Bid', 'Total Point', 'Cards']

def show_table(data: tuple):
    for i in data:
        table.add_row(i)
    print(table)