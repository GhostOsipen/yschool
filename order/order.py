import json

with open("order/input.txt") as f:
    data = json.load(f)

order_dict = {}

for object in data:
    if object["order_id"] not in order_dict:
        order_dict.setdefault(object["order_id"], [object])
    else:
        order_dict[object["order_id"]].append(object)        

output_orders = []

for order in order_dict.values():
    order_dict = {}
    item_list = []
    items_in_order_dict = {}

    for event in order:
        if event["item_id"] not in items_in_order_dict:
            items_in_order_dict.setdefault(event["item_id"], [event])
        else:
            items_in_order_dict[event["item_id"]].append(event)
    
    
    for item_events in items_in_order_dict.values():
        last_event = max(item_events, key=lambda ev: ev["event_id"])# max event id

        count = 0
        if last_event["status"] != "CANCEL":
            count = last_event['count'] - last_event["return_count"]
        if count != 0:
            item_list.append({"count": count, "id": last_event["item_id"]})
            
            if last_event["order_id"] not in order_dict:
                order_dict.setdefault("id", last_event["order_id"])
                order_dict.setdefault("item", item_list)
            else:
                order_dict["item"].append(item_list)

    output_orders.append(order_dict)
print(json.dumps(output_orders, sort_keys=True, indent=4))

with open("order/output.txt ", 'w') as f:
    json.dump(output_orders, f, sort_keys=True, indent=4)
