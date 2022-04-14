"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.id_producer = 0
        self.id_consumer = 0

        self.producers_dictionary = {} # Dictionary for producers
        self.carts_dictionary = {} # Dictionary for carts
        self.lock_add_cart = Lock() # Lock when add product in cart
        self.lock_publish = Lock() # Lock when publish product in marketplace

    def register_producer(self):
        self.id_producer += 1 # Returns an id for the producer that calls this.
        self.producers_dictionary[self.id_producer] = [] # Initialize producer with an empty list
        
        return self.id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace
        :type producer_id: String
        :param producer_id: producer id
        :type product: Product
        :param product: the Product that will be published in the Marketplace
        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # A single producer can publish a product in a time
        self.lock_publish.acquire()
        producers_list = self.producers_dictionary[producer_id]

        if len(producers_list) >= self.queue_size_per_producer:
            return False

        producers_list.append(product)

        # Free the lock for the producer id
        self.lock_publish.release()
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        self.id_consumer += 1
        # Initialize a cart for the consumer with an empty list
        self.carts_dictionary[self.id_consumer] = []

        return self.id_consumer

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to add to cart
        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # Find producer id wich have the product
        find_product = False
        keys = list(self.producers_dictionary.keys())

        self.lock_add_cart.acquire()

        # Iterate in list of list of producers
        for key in keys:
            for prod in self.producers_dictionary[key]:
                # If the product is available for consumer
                if prod == product:
                    find_product = True
                    # Remove product from producer with id
                    self.producers_dictionary[key].remove(product)
                    # Add product in cart 
                    self.carts_dictionary[cart_id].append([product, key])
                    break
            if find_product == True:
                break
        # Free the lock for the consumer 
        self.lock_add_cart.release()

        return find_product

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        # Take the list of products with id from carts dictionary
        list_product = self.carts_dictionary[cart_id]
        find_id_prod= None
        # Iterate in the list to find the id for producer
        for prod, id_prod in list_product:
            if prod == product:
                list_product.remove([product, id_prod])
                self.carts_dictionary[cart_id] = list_product
                self.producers_dictionary[id_prod].append(product)
                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        return [] + [prod for prod, _ in self.carts_dictionary[cart_id]]