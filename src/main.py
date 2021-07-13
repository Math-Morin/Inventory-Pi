from transactions import single_in, single_out, multiple_in, multiple_out

print("Welcome to Inventory-Pi")

while True:
    task_code = input("Please scan a task code... ")

    if task_code == "exit":
        break

    elif task_code == "single-in":
        print("'single-in' selected")
        input_barcode = input("Please scan an item or the 'done' barcode...")
        single_in(input_barcode)

    elif task_code == "single-out":
        print("'single-out' selected")
        input_barcode = input("Please scan an item or the 'done' barcode...")
        single_out(input_barcode)

    elif task_code == "multiple-in":
        print("'multiple-in' selected.")
        multiple_in()

    elif task_code == "multiple-out":
        print("'multiple out' selected.")
        multiple_out()

    else:
        print(f"Invalid task code: {task_code}")
