from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum

class Payment(Enum):
    NOT_YET_ORDERED = 0
    ORDERED = 1
    PENDING = 2
    PROCESSING = 3
    SUCCESS = 4

class ID:
    def __init__(self):
        self.__uuid = uuid4()

    @property
    def id(self):
        return self.__uuid

@dataclass(order=True)
class Customer(ID):
    # id: str #= field(default_factory=uuid4)
    name: str
    baskets: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__()

    def create_basket(self):
        new_basket = Basket(customer_id=self.id)
        self.baskets.update(
            {
                new_basket.id: new_basket
            }
        )

    def add_to_basket(self, basket_id: str, item_id: str, total: float):
        self.baskets[basket_id].items.append(item_id)
        self.baskets[basket_id].total += total

@dataclass(order=True)
class Grocer(ID):
    # id: str #= field(default_factory=uuid4)
    name: str

    def __post_init__(self):
        super().__init__()

@dataclass(order=True)
class Transaction(ID):
    # id: str #= field(default_factory=uuid4)
    customer_id: str
    grocer_id: str
    amount: float
    status: Payment.NOT_YET_ORDERED

    def __post_init__(self):
        super().__init__()

@dataclass(order=True)
class Order(ID):
    # id: str #= field(default_factory=uuid4)
    customer_id: str
    grocer_id: str
    basket_id: str
    total: float
    payment: Transaction
    items: list = field(default_factory=list)

    def __post_init__(self):
        super().__init__()

@dataclass(order=True)
class OrderQueue(ID):
    # id: str #= field(default_factory=uuid4)
    grocer_id: str
    baskets: list = field(default_factory=list)

    def __post_init__(self):
        super().__init__()

@dataclass(order=True)
class Menu(ID):
    # id: str #= field(default_factory=uuid4)
    grocer_id: str
    items: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__init__()

    def add_new_item_to_menu(self, new_item):
        self.items.update(
            {
                new_item.id: new_item
            }
        )

    def add_many_new_items(self, *args):
        for new_item in args:
            self.add_new_item_to_menu(new_item)
    

@dataclass(order=True)
class SingleItem(ID):
    # id: str
    name: str
    menu_id: str
    grocer_id: str
    price: float

    def __post_init__(self):
        super().__init__()

@dataclass(order=True)
class SingleWeightedItem(ID):
    # id: str
    name: str
    menu_id: str
    grocer_id: str
    price: float
    # weight: float

    def __post_init__(self):
        super().__init__()

@dataclass(order=True)
class BasketItem(ID):
    # id: str #= field(default_factory=uuid4)
    item_id: str
    basket_id: str
    customer_id: str
    total: float
    amount: float

    def __post_init__(self):
        super().__init__()

    def get_total(self):
        if self.price_by_weight:
            return self.total * self.amount

@dataclass(order=True)
class Basket(ID):
    # id: str #= field(default_factory=uuid4)
    customer_id: str

    def __post_init__(self):
        super().__init__()


if __name__ == "__main__":
    c1 = Customer(name="Adolf Johnson")
    c1.create_basket()
    c2 = Customer(name="Michelle Hitler")
    c2.create_basket()

    print(c2)

    g1 = Grocer(name="Shuk Givatayim")
    m1 = Menu(grocer_id=g1.id)
    i1 = SingleItem(name="1L Milk", grocer_id=g1.id, menu_id=m1.id, price=10.90)
    i2 = SingleItem(name="Egg Carton (12)", grocer_id=g1.id, menu_id=m1.id, price=18.90)
    i3 = SingleItem(name="Honey (250ml)", grocer_id=g1.id, menu_id=m1.id, price=13.60)
    i4 = SingleItem(name="Cottage Cheese (200ml)", grocer_id=g1.id, menu_id=m1.id, price=9.90)
    i5 = SingleItem(name="Belmont Cigarettes (King Size)", grocer_id=g1.id, menu_id=m1.id, price=45.00)
    
    wi1 = SingleWeightedItem(name="Banana", grocer_id=g1.id, menu_id=m1.id, price=7.90)
    wi2 = SingleWeightedItem(name="Granny Smith Apple", grocer_id=g1.id, menu_id=m1.id, price=13.90)
    wi3 = SingleWeightedItem(name="Blood Orange", grocer_id=g1.id, menu_id=m1.id, price=11.60)
    m1.add_many_new_items(*[i1, i2, i3, i4, i5, wi1, wi2, wi3])
    print(m1)