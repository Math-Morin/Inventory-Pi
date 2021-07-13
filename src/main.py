from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import select
from sqlalchemy.orm import Session, declarative_base


Base = declarative_base()
engine = create_engine(
    'sqlite+pysqlite:///inventory.db',
    echo=False,
    future=True
)


class Inventory(Base):
    __tablename__ = 'inventory'

    barcode = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Inventory(bar_code={self.barcode!r}, " \
               f"name={self.name!r}, " \
               f"quantity={self.quantity!r})"


Base.metadata.create_all(engine)


print("Welcome to Inventory-Pi")

while True:
    task_code = input("Please scan a task code... ")

    if task_code == "multiple-in":
        print("'multiple-in' selected.")

        while True:
            input_barcode = input(
                "Please scan an item or the 'done' barcode... "
            )

            if input_barcode == "done":
                break

            with Session(engine) as session:
                barcodes_in_inventory = session.execute(
                    select(Inventory.barcode)
                ).scalars()

                if input_barcode in barcodes_in_inventory:
                    item_to_update = session.execute(
                        select(Inventory).
                        filter_by(barcode=input_barcode)
                    ).scalar_one()
                    item_to_update.quantity += 1

                else:
                    item_name = input(
                        "Please enter the name of the item... "
                    ).lower().strip().replace(' ', '_')

                    new_item = Inventory(
                        barcode=input_barcode,
                        name=item_name,
                        quantity=1
                    )
                    session.add(new_item)

                session.commit()

                updated_item = session.execute(
                    select(Inventory).
                    filter_by(barcode=input_barcode)
                ).scalar_one()
                print(f"Item {updated_item.barcode} '{updated_item.name}' "
                      f"quantity is now {updated_item.quantity}.")

    elif task_code == "multiple-out":
        print("'multiple out' selected.")

        while True:
            input_barcode = input(
                "Please scan an item or the 'done' barcode... "
            )

            if input_barcode == "done":
                break

            with Session(engine) as session:
                barcodes_in_inventory = session.execute(
                    select(Inventory.barcode)
                ).scalars()

                if input_barcode in barcodes_in_inventory:
                    item_to_update = session.execute(
                        select(Inventory).
                        filter_by(barcode=input_barcode)
                    ).scalar_one()

                    if item_to_update.quantity > 0:
                        item_to_update.quantity -= 1

                        session.commit()

                        updated_item = session.execute(
                            select(Inventory).
                            filter_by(barcode=input_barcode)
                        ).scalar_one()

                        print(f"Item {updated_item.barcode} "
                              f"'{updated_item.name}' "
                              f"quantity is now {updated_item.quantity}.")
                    else:
                        print(f"ERROR: Quantity can't ben decremented.")
                        print(f"Item {item_to_update.barcode} "
                              f"'{item_to_update.name}' "
                              f"quantity is {item_to_update.quantity}.")

                else:
                    print(f"Item {input_barcode} not in inventory.")

    elif task_code == "exit":
        break
    else:
        print(f"Invalid task code: {task_code}")
