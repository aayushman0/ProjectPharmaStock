from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date, datetime

BaseModel = declarative_base()
type_dict = {
        "tablet": "tab",
        "capsule": "cap",

        "syrup": "syp",
        "drops": "drp",

        "ointment": "ont",
        "cream": "crm",
        "gel": "gel",

        "powder": "pwd",
        "injection": "inj",
        "other": "oth"
    }


class Item(BaseModel):
    __tablename__ = "item"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(64), index=True, nullable=False)
    type = Column("type", String(64), index=True, nullable=False)
    code = Column("code", String(64), index=True, unique=True)
    price = Column("price", Float)
    best_before = Column("best_before", Integer)

    def __init__(self, name: str, type: str, code: str, price: float, best_before: int):
        self.name = name
        self.type = type
        self.code = code
        self.price = price
        self.best_before = best_before

    def __repr__(self):
        return f"{type_dict.get(self.type.lower(), "oth").capitalize()}. {self.name}"


class Batch(BaseModel):
    __tablename__ = "batch"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    batch_no = Column("batch_no", String(100), index=True)
    quantity = Column("quantity", Integer)
    price = Column("price", Float)
    mfg_date = Column("mfg_date", Date)
    exp_date = Column("exp_date", Date, index=True)
    distributor = Column("distributor", String(64), index=True)
    item_id = Column(String(64), ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    item = relationship("Item", backref="batches")

    def __init__(self, item_id: int, batch_no: str, quantity: int, price: float, mfg_date: date, exp_date: date, distributor: str):
        self.batch_no = batch_no
        self.quantity = quantity
        self.price = price
        self.mfg_date = mfg_date
        self.exp_date = exp_date
        self.distributor = distributor
        self.item_id = item_id

    def __repr__(self):
        return f"{self.item.name} Batch: {self.batch_no}"


class Bill(BaseModel):
    __tablename__ = "bill"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    customer_name = Column("name", String(64))
    bill_json = Column("bill_json", String)
    total_amount = Column("total_amount", Float)
    discount = Column("discount", Float)
    net_amount = Column("net_amount", Float)
    payment_type = Column("payment_type", String(64))
    bill_date = Column("bill_date", DateTime)

    def __init__(self, customer_name: str, bill_json: str, total_amount: float, discount: float, net_amount: float, payment_type: str, bill_date: datetime):
        self.customer_name = customer_name
        self.bill_json = bill_json
        self.total_amount = total_amount
        self.discount = discount
        self.net_amount = net_amount
        self.payment_type = payment_type
        self.bill_date = bill_date

    def __repr__(self):
        return f"{self.id}. {self.customer_name}"


class ServiceBill(BaseModel):
    __tablename__ = "service_bill"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    patient_name = Column("name", String(64))
    bill_json = Column("bill_json", String)
    total_amount = Column("total_amount", Float)
    discount = Column("discount", Float)
    net_amount = Column("net_amount", Float)
    payment_type = Column("payment_type", String(64))
    bill_date = Column("bill_date", DateTime)

    def __init__(self, patient_name: str, bill_json: str, total_amount: float, discount: float, net_amount: float, payment_type: str, bill_date: datetime):
        self.patient_name = patient_name
        self.bill_json = bill_json
        self.total_amount = total_amount
        self.discount = discount
        self.net_amount = net_amount
        self.payment_type = payment_type
        self.bill_date = bill_date

    def __repr__(self):
        return f"{self.id}. {self.patient_name}"


engine = create_engine("sqlite:///mydb.db", echo=False)
BaseModel.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
