from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import insert, select
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
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Inventory(bar_code={self.barcode!r}, product={self.product!r}, quantity={self.quantity!r})"


Base.metadata.create_all(engine)


print("Welcome to Inventory-Pi")

while True:
    task_code = input("Please scan a task code... ")

    if task_code == "multiple-in":
        print("'multiple-in' selected.")

        while True:
            input_barcode = input(
                "Please scan a product or the 'done' barcode... "
            )

            if input_barcode == "done":
                break

            with Session(engine) as session:
                barcodes_in_inventory = session.execute(
                    select(Inventory.barcode)
                ).scalars()

                if input_barcode in barcodes_in_inventory:
                    product_to_update = session.execute(
                        select(Inventory).
                        filter_by(barcode=input_barcode)
                    ).scalar_one()
                    product_to_update.quantity += 1


                else:
                    product_name = input(
                        "Please enter the name of the product... "
                    ).lower().strip().replace(' ', '_')

                    new_product = Inventory(
                        barcode=input_barcode,
                        product=product_name,
                        quantity=1
                    )
                    session.add(new_product)

                session.commit()

    #
    # elif task_code == "multiple-out":
    #     print("'Multiple out' selected.")
    #
    #     while True:
    #         input_code_tuple = input("Please scan a product or the 'done' code... "),
    #         if input_code_tuple[0] == "done":
    #             break
    #
    #         product_row = list(cursor.execute("SELECT bar_code FROM inventory WHERE bar_code = ?", input_code_tuple))
    #
    #         if input_code_tuple in product_row:
    #             qty = list(cursor.execute("SELECT qty FROM inventory WHERE bar_code = ?", input_code_tuple))
    #             if qty[0][0] > 0:
    #                 cursor.execute("UPDATE inventory SET qty = qty - 1 WHERE bar_code = ?", input_code_tuple)
    #                 item = list(cursor.execute("SELECT * FROM inventory WHERE bar_code = ?", input_code_tuple))
    #                 print(f"Item {item[0][0]} {item[0][1]} quantity is now {item[0][2]}")
    #             else:
    #                 item = list(cursor.execute("SELECT * FROM inventory WHERE bar_code = ?", input_code_tuple))
    #                 print(f"Item {item[0][0]} {item[0][1]} quantity is already 0.")
    #         else:
    #             print(f"Item {input_code_tuple[0]} not in inventory.")
    #
    #         connection.commit()

    elif task_code == "exit":
        break
    else:
        print(f"Invalid task code: {task_code}")
