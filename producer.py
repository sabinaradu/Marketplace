"""
This module represents the Producer.
Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.
        @type products: List()
        @param products: a list of products that the producer will produce
        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace
        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available
        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    def publish_product(self, product, quantity, wait_time, id_producer):
        iterator = 0
        wait_publish = True
        # Publish a product in a quantity
        while iterator < quantity:
            # Producer must wait until the marketplace becomes available
            if self.marketplace.publish(id_producer, product) != True:
                time.sleep(self.republish_wait_time)
            else:
                iterator += 1
                time.sleep(wait_time)

    def run(self):
        while True:
            # Register the producer
            for i in range(len(self.products)):
                self.publish_product(self.products[i][0], self.products[i][1], 
                    self.products[i][2], self.marketplace.register_producer())