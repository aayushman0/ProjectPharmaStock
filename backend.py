import re
import json
from datetime import date, datetime
from sqlalchemy import func
from models import session
from models import Item, Batch, Bill, ServiceBill


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

no_of_rows = 22


def get_item_by_id(id: int) -> Item | None:
    item = session.query(Item).filter(Item.id == id).scalar()
    return item


def get_item_by_code(code: str) -> Item | None:
    item = session.query(Item).filter(Item.code == code).first()
    return item


def get_paginated_items(page: int) -> tuple[list[tuple[int, str, str, str, float, int]], int]:
    items = session.query(Item)
    count = items.count()
    paginated_items = items.slice((page-1) * no_of_rows, page * no_of_rows)
    response = [(item.id, item.name, item.type, item.code, item.price, item.best_before) for item in paginated_items]
    return response, count


def get_filtered_items(code: str) -> list[tuple[int, str, str, str, float, int]]:
    if code[:3] in type_dict.values():
        code_filter = f"%{code}%"
    else:
        code_filter = f"___{code}%"
    items = session.query(Item).filter(Item.code.like(code_filter)).order_by(Item.name)
    response = [(item.id, item.name, item.type, item.code, item.price, item.best_before) for item in items]
    return response


def get_batch(item_code: str, batch_no: str) -> Batch | None:
    item: Item | None = session.query(Item).filter(Item.code == item_code).scalar()
    if not item:
        return None
    batch = session.query(Batch).filter(Batch.item_id == item.id, Batch.batch_no == batch_no).first()
    return batch


def get_batch_nos_from_item_id(item_id: int) -> list[str] | None:
    batch_nos = session.query(Batch.batch_no).filter(Batch.item_id == item_id).all()
    return [batch_no[0] for batch_no in batch_nos]


def get_paginated_batches(page: int, code: str | None = None) -> tuple[list[tuple[str, str, int, float, float, str, str, str]], int]:
    if code:
        batches = session.query(Batch).join(Item).filter(Item.code.like(f"%{code}%")).order_by(Batch.exp_date)
    else:
        batches = session.query(Batch).order_by(Batch.exp_date)

    count = batches.count()
    paginated_batches = batches.slice((page-1) * no_of_rows, page * no_of_rows)
    response = [
        (batch.item, batch.batch_no, batch.quantity, batch.price, round(batch.quantity * batch.price, 2), str(batch.mfg_date)[:-3], str(batch.exp_date)[:-3], batch.distributor)
        for batch in paginated_batches
    ]
    return response, count


def get_sum_total_of_all() -> float:
    batches = session.query(Batch)
    total = 0.0
    for batch in batches:
        total += batch.price * batch.quantity
    return round(total, 3)


def get_bill(id: int) -> Bill | None:
    bill = session.query(Bill).filter(Bill.id == id).scalar()
    return bill


def get_bill_json_by_id(id: int) -> list[tuple[int, str, str, str, str, int, float, float]]:
    bill: Bill | None = session.query(Bill).filter(Bill.id == id).scalar()
    if not bill:
        return None
    bill_json = json.loads(bill.bill_json)
    response = [
        (row.get("sn", 0), row.get("particular"), row.get("batch_no"),
         str(row.get("mfg_date")), str(row.get("exp_date")),
         row.get("quantity", 0), row.get("price", 0), row.get("total", 0))
        for row in bill_json
    ]
    return response


def get_bills_by_date(date: date) -> list[tuple[int, str, float, str]]:
    bills = session.query(Bill).filter(func.DATE(Bill.bill_date) == date).order_by(Bill.bill_date.desc())
    response = [
        (bill.id, bill.customer_name, bill.net_amount, str(bill.bill_date)[:16])
        for bill in bills
    ]
    return response


def get_service_bill(id: int) -> ServiceBill | None:
    service_bill = session.query(ServiceBill).filter(ServiceBill.id == id).scalar()
    return service_bill


def get_service_bills_by_date(date: date) -> list[tuple[int, str, float, str]]:
    service_bills = session.query(ServiceBill).filter(func.DATE(ServiceBill.bill_date) == date).order_by(ServiceBill.bill_date.desc())
    response = [
        (bill.id, bill.patient_name, bill.net_amount, str(bill.bill_date)[:16])
        for bill in service_bills
    ]
    return response


def get_service_bill_json_by_id(id: int) -> list[tuple[int, str, float]]:
    service_bill: ServiceBill | None = session.query(ServiceBill).filter(ServiceBill.id == id).scalar()
    if not service_bill:
        return None
    bill_json = json.loads(service_bill.bill_json)
    response = [
        (row.get("sn", 0), row.get("procedure"), row.get("amount", 0))
        for row in bill_json
    ]
    return response


def add_item(name: str, type: str, price: float, best_before: int) -> Item:
    code = f"{type_dict.get(type.lower(), 'oth')}{re.sub('[^A-Za-z0-9]+', '', name).lower()}"

    item = session.query(Item).filter(Item.code == code).scalar()
    if not item:
        item = Item(name, type, code, price, best_before)
        session.add(item)
        session.commit()

    return item


def add_batch(item_id: str, batch_no: str, price: float, quantity: int, mfg_date: date, exp_date: date, distributor: str) -> Batch:
    item: Item | None = session.query(Item).filter(Item.id == item_id).scalar()
    if not item:
        return None
    item.price = price

    batch: Batch | None = session.query(Batch).filter(Batch.batch_no == batch_no, Batch.item_id == item_id).scalar()
    if not batch:
        batch = Batch(item_id, batch_no, quantity, price, mfg_date, exp_date, distributor)
    else:
        batch.quantity += quantity
        batch.price = price
        batch.mfg_date = mfg_date
        batch.exp_date = exp_date
        batch.distributor = distributor
    session.add(batch)
    session.commit()
    return batch


def add_bill(customer_name: str, bill_json: list[dict], total_amount: float, discount: float, net_amount: float, payment_type: str) -> Bill:
    bill = Bill(customer_name, json.dumps(bill_json), total_amount, discount, net_amount, payment_type, datetime.now())
    session.add(bill)

    for batch_dict in bill_json:
        batch_id: int = batch_dict.get("batch_id")
        quantity: int = batch_dict.get("quantity")
        if not batch_id:
            continue
        batch: Batch | None = session.query(Batch).filter(Batch.id == batch_id).scalar()
        if batch is None:
            continue
        if batch.quantity <= quantity:
            session.delete(batch)
        else:
            batch.quantity -= quantity
    session.commit()
    return bill


def add_service_bill(patient_name: str, bill_json: list[dict], total_amount: float, discount: float, net_amount: float, payment_type: str) -> ServiceBill:
    service_bill = ServiceBill(patient_name, json.dumps(bill_json), total_amount, discount, net_amount, payment_type, datetime.now())
    session.add(service_bill)
    session.commit()
    return service_bill


def edit_item(code: str, name: str, type: str, price: float, best_before: int) -> Item | None:
    item: Item | None = session.query(Item).filter(Item.code == code).scalar()
    if not item:
        return None
    item.name = name
    item.type = type
    item.code = code = f"{type_dict.get(type.lower(), 'oth')}{re.sub('[^A-Za-z0-9]+', '', name).lower()}"
    item.price = price
    item.best_before = best_before
    session.commit()
    return item


def edit_batch(code: str, batch_no: str, price: float, quantity: int, mfg_date: date, exp_date: date, distributor: str) -> Batch | None:
    batch = session.query(Batch).join(Item).filter(Item.code == code, Batch.batch_no == batch_no).first()
    if not batch:
        return None
    if quantity == 0:
        session.delete(batch)
        session.commit()
        return None
    batch.price = price
    batch.quantity = quantity
    batch.mfg_date = mfg_date
    batch.exp_date = exp_date
    batch.distributor = distributor
    session.commit()
    return batch


def delete_expired_batches(date: date) -> list[tuple[str, str]]:
    batches = session.query(Batch).filter(Batch.exp_date <= date).order_by(Batch.item_id)
    deleted_batches = list()
    for batch in batches:
        deleted_batches.append((batch.item, batch.batch_no))
        session.delete(batch)
    session.commit()
    return deleted_batches
