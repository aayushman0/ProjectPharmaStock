# from models import session
# from models import Batch
# from backend import add_item
# from datetime import datetime


# code_to_type = {
#         "tab": "Tablet",
#         "cap": "Capsule",
#         "syp": "Syrup",
#         "ont": "Ointment",
#         "crm": "Cream",
#         "drp": "Drops",
#         "oth": "Other"
#     }

# with open("migrate_data.txt", "r") as f:
#     items_and_batches = list()
#     data = list()
#     for line in f.readlines():
#         if line == "\n":
#             items_and_batches.append(data)
#             data = list()
#         else:
#             data.append(line[:-1])

# for item_and_batches in items_and_batches:
#     item = item_and_batches[0].split(">>")
#     batches = [batch.split(">>") for batch in item_and_batches[1:]]
#     db_item = add_item(item[1], code_to_type.get(item[0], "Other"), float(item[2]), int(item[3]))
#     session.add(db_item)
#     session.commit()
#     print(db_item.id, db_item.code)
#     for batch in batches:
#         db_batch = Batch(
#             db_item.id,
#             batch[0],
#             int(batch[1]),
#             float(batch[2]),
#             datetime.strptime(batch[3], "%Y-%m-%d"),
#             datetime.strptime(batch[4], "%Y-%m-%d"),
#             None
#         )
#         session.add(db_batch)
#         session.commit()
#         print("\t", db_batch.item, db_batch.batch_no)
