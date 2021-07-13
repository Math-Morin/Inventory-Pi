from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base


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
