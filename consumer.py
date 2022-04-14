"""
This module represents the Consumer.
Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.
        :type carts: List
        :param carts: a list of add and remove operations
        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace
        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available
        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs
        
    def run(self):
        id_cart = self.marketplace.new_cart()
        # Iterate in lists from carts and then extract elements from dictionary
        for list_element in self.carts:
            for dict_element in list_element:
                type_command = dict_element["type"]
                id_prod = dict_element["product"]
                quantity_prod = dict_element["quantity"]
                # Add product in marketplace
                if type_command == "remove":
                    iterator = 0
                    while iterator < quantity_prod:
                        # Remove product from marketplace
                        self.marketplace.remove_from_cart(id_cart, id_prod)
                        iterator += 1
                else:
                    iterator = 0
                    # Add product in quantity
                    while iterator < quantity_prod:
                        if self.marketplace.add_to_cart(id_cart, id_prod) != True:
                            # wait time to become available
                            time.sleep(self.retry_wait_time)
                        else:
                            iterator  += 1
        # Get the list with all the products from the cart
        for product in self.marketplace.place_order(id_cart):
            print(self.name, "bought", product)