from sqlalchemy import select
from sqlalchemy.orm import Session
from base import engine, Inventory
from bs4 import BeautifulSoup

import requests

MULTIPLE_MSG = "Please scan an item, the 'quantity' or the 'done' barcode..."
QTY_IN_MSG = "Please enter the quantity of items to add..."
QTY_IN_MSG = "Please enter the quantity of items to substract..."
SCAN_MSG = "Please scan an item..."


def multiple_in():
    while True:
        input_barcode = input(MULTIPLE_MSG)

        if input_barcode == "done":
            break

        qty = 1
        if input_barcode == "quantity":
            qty = input(QTY_IN_MSG)
            barcode = input(SCAN_MSG)

        single_in(input_barcode, qty)


def multiple_out():
    while True:
        input_barcode = input(MULTIPLE_MSG)

        if input_barcode == "done":
            break

        qty = 1
        if input_barcode == "quantity":
            qty = input(QTY_OUT_MSG)
            barcode = input(SCAN_MSG)

        single_out(input_barcode, qty)


def single_in(input_barcode, qty):
    with Session(engine) as session:
        barcodes_in_inventory = session.execute(select(Inventory.barcode)).scalars()

        if input_barcode in barcodes_in_inventory:
            increment(session, input_barcode, qty)

        else:
            create_new_item(session, input_barcode, qty)


def single_out(input_barcode, qty):
    with Session(engine) as session:
        barcodes_in_inventory = session.execute(select(Inventory.barcode)).scalars()

        if input_barcode in barcodes_in_inventory:
            decrement(session, input_barcode, qty)

        else:
            print(f"Item {input_barcode} not in inventory.")


def increment(session, input_barcode, qty):
    item_to_update = session.execute(
        select(Inventory).filter_by(barcode=input_barcode)
    ).scalar_one()
    item_to_update.quantity += qty
    session.commit()
    print_update_msg(session, input_barcode)


def decrement(session, input_barcode, qty):
    item_to_update = session.execute(
        select(Inventory).filter_by(barcode=input_barcode)
    ).scalar_one()

    if item_to_update.quantity - qty >= 0:
        item_to_update.quantity -= qty
        session.commit()
        print_update_msg(session, input_barcode)

    else:
        print(f"ERROR: Not enough item in enventory.")
        print(
            f"Item {item_to_update.barcode} "
            f"'{item_to_update.name}' "
            f"quantity is {item_to_update.quantity}."
        )


def create_new_item(session, input_barcode, qty):

    url = "https://world.openfoodfacts.org/api/v2/search?code=" + input_barcode
    response = requests.get(url)
    json_data = response.json() if response and response.status_code == 200 else None
    item_name = (
        json_data["products"][0]["product_name"] if json_data["count"] == 1 else None
    )

    if item_name:
        print(f"Product name found : {item_name}")
        item_name = item_name.lower().strip().replace(" ", "_")
    else:
        print("Product name not found.")
        item_name = (
            input("Please enter the name of the item... ")
            .lower()
            .strip()
            .replace(" ", "_")
        )

    new_item = Inventory(barcode=input_barcode, name=item_name, quantity=qty)
    session.add(new_item)
    session.commit()
    print_update_msg(session, input_barcode)


def print_update_msg(session, input_barcode):
    updated_item = session.execute(
        select(Inventory).filter_by(barcode=input_barcode)
    ).scalar_one()
    print(
        f"Item {updated_item.barcode} '{updated_item.name}' "
        f"quantity is now {updated_item.quantity}."
    )
