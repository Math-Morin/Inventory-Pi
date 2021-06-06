import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS inventory
                    (bar_code TEXT PRIMARY KEY NOT NULL,
                    product_name TEXT NOT NULL,
                    qty INT NOT NULL)''')

print("Welcome to Inventory-Pi")
item = tuple(cursor.execute("SELECT * FROM inventory WHERE bar_code = ?", ("045566000309",)))
print(item)

running = False
while running:
    task_code = input("Please scan a task code... ")

    if task_code == "multiple-in":
        print("'Multiple in' selected.")

        while True:
            input_code_tuple = input("Please scan a product or the 'done' code... "),  # tuple
            if input_code_tuple[0] == "done":
                break

            db = list(cursor.execute("SELECT bar_code FROM inventory WHERE bar_code = ?", input_code_tuple))

            if input_code_tuple in db:
                cursor.execute("UPDATE inventory SET qty = qty + 1 WHERE bar_code = ?", input_code_tuple)
                item = list(cursor.execute("SELECT * FROM inventory WHERE bar_core = ?", input_code_tuple))
                print(f"{item[0][0]} {item[0][1]} quantity is now {item[0][2]}")
            else:
                input_name = input("Please enter the name of the product... ").lower().strip().replace(' ', '_'),
                inputs = (input_code_tuple[0], input_name[0])
                cursor.execute("INSERT INTO inventory VALUES (?, ?, 1)", inputs)
                print(f"New item {inputs[0]} {inputs[1]} added to inventory with quantity 1")

            connection.commit()

    elif task_code == "multiple-out":
        print("'Multiple out' selected.")

        while True:
            input_code_tuple = input("Please scan a product or the 'done' code... "),
            if input_code_tuple[0] == "done":
                break

            db = list(cursor.execute("SELECT bar_code FROM inventory WHERE bar_code = ?", input_code_tuple))

            if input_code_tuple in db:
                qty = list(cursor.execute("SELECT qty FROM inventory WHERE bar_code = ?", input_code_tuple))
                if qty > 0:
                    cursor.execute("UPDATE inventory SET qty = qty - 1 WHERE bar_code = ?", input_code_tuple)
                    item = cursor.execute("SELECT * FROM inventory WHERE bar_code = ?", input_code_tuple)
                    print(f"Item {item[0][0]} {item[0][1]} quantity is now {item[0][2]}")
                else:
                    item = cursor.execute("SELECT * FROM inventory WHERE bar_code = ?", input_code_tuple)
                    print(f"ERROR. Item {item[0][0]} {item[0][1]} quantity is 0.")
            else:
                print(f"Item {input_code_tuple[0]} not in inventory.")

            connection.commit()
