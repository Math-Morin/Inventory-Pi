from sqlalchemy import select
from sqlalchemy.orm import Session
from base import engine, Inventory


def multiple_in():
    while True:
        input_barcode = input("Please scan an item or the 'done' barcode...")

        if input_barcode == "done":
            break

        single_in(input_barcode)


def multiple_out():
    while True:
        input_barcode = input("Please scan an item or the 'done' barcode...")

        if input_barcode == "done":
            break

        single_out(input_barcode)


def single_in(input_barcode):

    with Session(engine) as session:
        barcodes_in_inventory = session.execute(
            select(Inventory.barcode)
        ).scalars()

        if input_barcode in barcodes_in_inventory:
            increment(session, input_barcode)

        else:
            create_new_item(session, input_barcode)

        session.commit()
        print_update_msg(session, input_barcode)


def single_out(input_barcode):

    with Session(engine) as session:
        barcodes_in_inventory = session.execute(
            select(Inventory.barcode)
        ).scalars()

        if input_barcode in barcodes_in_inventory:
            decrement(session, input_barcode)

        else:
            print(f"Item {input_barcode} not in inventory.")


def increment(session, input_barcode):
    item_to_update = session.execute(
        select(Inventory).
        filter_by(barcode=input_barcode)
    ).scalar_one()
    item_to_update.quantity += 1


def decrement(session, input_barcode):
    item_to_update = session.execute(
        select(Inventory).
        filter_by(barcode=input_barcode)
    ).scalar_one()

    if item_to_update.quantity > 0:
        item_to_update.quantity -= 1
        session.commit()
        print_update_msg(session, input_barcode)

    else:
        print(f"ERROR: Quantity can't be negative.")
        print(f"Item {item_to_update.barcode} "
              f"'{item_to_update.name}' "
              f"quantity is {item_to_update.quantity}.")


def create_new_item(session, input_barcode):
    item_name = input(
        "Please enter the name of the item... "
    ).lower().strip().replace(' ', '_')

    new_item = Inventory(
        barcode=input_barcode,
        name=item_name,
        quantity=1
    )
    session.add(new_item)


def print_update_msg(session, input_barcode):
    updated_item = session.execute(
        select(Inventory).
        filter_by(barcode=input_barcode)
    ).scalar_one()
    print(f"Item {updated_item.barcode} '{updated_item.name}' "
          f"quantity is now {updated_item.quantity}.")
