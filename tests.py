import json
from app import get_quarter_points, get_round_points, get_points_per_two_items, get_store_chars, \
    get_item_description_points, get_purchase_day_points, get_purchase_time_points, score_total_receipt

with open('my_tests/round-receipt.json', 'r') as round_receipt:
    test1_data = json.load(round_receipt)

with open('my_tests/janky_receipt.json', 'r') as janky_receipt:
    janky_data = json.load(janky_receipt)

with open('my_tests/quarter_receipt.json', 'r') as quarter_receipt:
    quarter_data = json.load(quarter_receipt)

with open('my_tests/empty_receipt.json', 'r') as empty_receipt:
    empty_data = json.load(empty_receipt)

with open('examples/longer_receipt.json', 'r') as longer_receipt:
    longer_test_data = json.load(longer_receipt)

with open('examples/shorter_receipt.json', 'r') as shorter_receipt:
    shorter_test_data = json.load(shorter_receipt)

with open('examples/simple-receipt.json', 'r') as simple_receipt:
    simple_data = json.load(simple_receipt)

#Simple Receipt
assert get_store_chars(simple_data) == 6
assert get_round_points(simple_data) == 0
assert get_points_per_two_items(simple_data) == 0

#Test Receipt with Round Total
assert get_store_chars(test1_data) == 3
assert get_round_points(test1_data) == 50
assert get_purchase_day_points(test1_data) == 6

#Receipt with Messed up inputs
assert get_store_chars(janky_data) == 0
assert get_round_points(janky_data) == 0

#Test Receipt with Quarter Total
assert get_quarter_points(quarter_data) == 25
assert get_points_per_two_items(quarter_data) == 5

#Test Receipt with No Items
assert get_points_per_two_items(empty_data) == 0
assert get_purchase_day_points(empty_data) == 0

#Test Receipt from Problem Desc with Longer Items
assert get_points_per_two_items(longer_test_data) == 10
assert get_item_description_points(longer_test_data) == 6
assert get_purchase_day_points(longer_test_data) == 6
assert get_purchase_time_points(longer_test_data) == 0
assert score_total_receipt(longer_test_data) == 28

#Test Receipt from Problem Desc with Fewer Items
assert get_store_chars(shorter_test_data) == 14
assert get_round_points(shorter_test_data) == 50
assert get_quarter_points(shorter_test_data) == 25
assert get_points_per_two_items(shorter_test_data) == 10
assert get_purchase_time_points(shorter_test_data) == 10
assert score_total_receipt(shorter_test_data) == 109