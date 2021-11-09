import json
import random
from datetime import timedelta, datetime

from Order import Order

order_states = ['NEW', 'CLOSED', 'IN-TRANSIT', 'READY', 'SHIPPED', 'DELIVERED']


def get_date_constraints():
    date_time_format = '%Y-%m-%d %H:%M:%S'
    start_date = datetime.strptime('2020-01-01 00:00:00', date_time_format)
    end_date = datetime.strptime('2021-11-07 00:00:00', date_time_format)
    return start_date, end_date


def get_random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_json(order):
    return order.get_dictionary()


class FakeDataGenerator:
    def generate_data(self):

        order_id = random.randint(1000, 50000)
        customer_id = random.randint(1000, 40000)
        product_id = random.randint(10, 40)
        start_date, end_date = get_date_constraints()
        order_date = get_random_date(start_date, end_date)
        order_state = random.choice(order_states)
        order_quantity = random.randint(1, 100)
        order = Order(order_id, customer_id, product_id, order_date, order_state, order_quantity)

        return order

    def generate_json_payload(self):
        order = self.generate_data()
        order = get_json(order)
        return order



