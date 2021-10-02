import json
import os


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {'wallet': 100, 'bank': 0}
    with open("storage_data/bank.json", "w") as f:
        json.dump(users, f, indent=4)
    return True


async def get_bank_data():
    with open("storage_data/bank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("storage_data/bank.json", "w") as f:
        json.dump(users, f, indent=4)

    return [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]


mainshop = [
    {"name": "Watch", "price": 100, "description": "Time"},
    {"name": "Laptop", "price": 1000, "description": "Work"},
    {"name": "PC", "price": 10000, "description": "Gaming"},
]


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ is None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t is None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)

    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("storage_data/bank.json", "w") as f:
        json.dump(users, f, indent=4)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]
