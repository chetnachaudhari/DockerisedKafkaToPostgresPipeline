class Order(object):

    def __init__(self, order_id, customer_id, product_id, order_date, order_state, order_quantity):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.order_date = order_date
        self.order_state = order_state
        self.order_quantity = order_quantity

    def __str__(self):
        pass

    def __repr__(self):
        return 'Order class: [order_id={}, customer_id={}, product_id={}, order_date={}, order_state={}, order_quantity={}]'.format(
            self.order_id, self.customer_id, self.product_id, self.order_date, self.order_state, self.order_quantity)

    def get_dictionary(self):
        return dict(order_id=self.order_id,
                    customer_id=self.customer_id,
                    product_id=self.product_id,
                    order_date=str(self.order_date),
                    order_state=self.order_state,
                    order_quantity=self.order_quantity)