import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class Shop(Orders):
    __tablename__ = 'Shop'
    id_shop = Column(Integer, primary_key=True)
    address = Column(String)
    name = Column(String)
    catalogs = relationship("Catalog")
    orders = relationship("Order")

    def __init__(self, id_shop, address, name):
        self.id_shop = id_shop
        self.address = address
        self.name = name

    def __repr__(self):
        return "{:>10}{:>35}{:>15}" \
            .format(self.id_shop, self.address, self.name)


class Catalog(Orders):
    __tablename__ = 'Catalog'
    id_catalog = Column(Integer, primary_key=True)
    name = Column(String)
    id_shop = Column(Integer, ForeignKey('Shop.id_shop'))
    pid_catalog = Column(Integer, ForeignKey('Catalog.id_catalog'))
    products = relationship("Product")
    parent_catalogs = relationship("Catalog")

    def __init__(self, id_catalog, name, id_shop, pid_catalog):
        self.id_catalog = id_catalog
        self.name = name
        self.id_shop = id_shop
        self.pid_catalog = pid_catalog

    def __repr__(self):
        return "{:>10}{:>15}{:>10}{:>10}" \
            .format(self.id_catalog, self.name, self.id_shop, self.pid_catalog)


class Order(Orders):
    __tablename__ = 'Order'
    id_order = Column(Integer, primary_key=True)
    customer_name = Column(String)
    id_shop = Column(Integer, ForeignKey('Shop.id_shop'))
    date = Column(Date)
    products = relationship("Product")

    def __init__(self, id_order, customer_name, id_shop, date):
        self.id_order = id_order
        self.customer_name = customer_name
        self.id_shop = id_shop
        self.date = date

    def __repr__(self):
        return "{:>10}{:>25}{:>10}\t\t{}" \
            .format(self.id_order, self.customer_name, self.id_shop, self.date)


class Product(Orders):
    __tablename__ = 'Product'
    id_product = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    category = Column(String)
    id_catalog = Column(Integer, ForeignKey('Catalog.id_catalog'))
    id_order = Column(Integer, ForeignKey('Order.id_order'))

    def __init__(self, id_product, title, price, category, id_catalog, id_order):
        self.id_product = id_product
        self.title = title
        self.price = price
        self.category = category
        self.id_catalog = id_catalog
        self.id_order = id_order

    def __repr__(self):
        return "{:>10}{:>30}{:>10}{:>15}{:>10}{:>10}" \
            .format(self.id_product, self.title, self.price, self.category, self.id_catalog, self.id_order)


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_product(self, key_value: int):
        return self.session.query(Product).filter_by(id_product=key_value).first()

    def find_fk_product(self, key_value: int, table_name: str):
        if table_name == "Order":
            return self.session.query(Product).filter_by(id_order=key_value).first()
        elif table_name == "Catalog":
            return self.session.query(Product).filter_by(id_catalog=key_value).first()

    def find_pk_order(self, key_value: int):
        return self.session.query(Order).filter_by(id_order=key_value).first()

    def find_fk_order(self, key_value: int):
        return self.session.query(Order).filter_by(id_shop=key_value).first()

    def find_pk_catalog(self, key_value: int):
        return self.session.query(Catalog).filter_by(id_catalog=key_value).first()

    def find_fk_catalog(self, key_value: int):
        return self.session.query(Catalog).filter_by(id_shop=key_value).first()

    def find_pk_shop(self, key_value: int):
        return self.session.query(Shop).filter_by(id_shop=key_value).first()

    def print_products(self):
        return self.session.query(Product).order_by(Product.id_product.asc()).all()

    def print_order(self):
        return self.session.query(Order).order_by(Order.id_order.asc()).all()

    def print_catalog(self):
        return self.session.query(Catalog).order_by(Catalog.id_catalog.asc()).all()

    def print_shop(self):
        return self.session.query(Shop).order_by(Shop.id_shop.asc()).all()

    def delete_data_products(self, id_product) -> None:
        self.session.query(Product).filter_by(id_product=id_product).delete()
        self.session.commit()

    def delete_data_order(self, id_order) -> None:
        self.session.query(Order).filter_by(id_order=id_order).delete()
        self.session.commit()

    def delete_data_catalog(self, id_catalog) -> None:
        self.session.query(Catalog).filter_by(id_catalog=id_catalog).delete()
        self.session.commit()

    def delete_data_shop(self, id_shop) -> None:
        self.session.query(Shop).filter_by(id_shop=id_shop).delete()
        self.session.commit()

    def update_data_product(self, id_product: int, title: str, price: float, category: str,
                            id_catalog: int, id_order: int) -> None:
        self.session.query(Product).filter_by(id_product=id_product) \
            .update({Product.title: title, Product.price: price, Product.category: category,
                     Product.id_catalog: id_catalog, Product.id_order: id_order})
        self.session.commit()

    def update_data_order(self, id_order: int, customer_name: str, id_shop: int, date: datetime.datetime) -> None:
        self.session.query(Order).filter_by(id_order=id_order) \
            .update({Order.customer_name: customer_name, Order.id_shop: id_shop, Order.date: date})
        self.session.commit()

    def update_data_catalog(self, id_catalog: int, name: str, id_shop: int, pid_catalog: int) -> None:
        self.session.query(Catalog).filter_by(id_order=id_catalog) \
            .update({Catalog.name: name, Catalog.id_shop: id_shop, Catalog.pid_catalog: pid_catalog})
        self.session.commit()

    def update_data_shop(self, id_shop: int, address: str, name: str) -> None:
        self.session.query(Shop).filter_by(id_shop=id_shop) \
            .update({Shop.address: address, Shop.name: name})
        self.session.commit()

    def insert_data_product(self, id_product: int, title: str, price: float, category: str, id_catalog: int,
                            id_order: int) -> None:
        product = Product(id_product=id_product, title=title, price=price, category=category,
                          id_catalog=id_catalog, id_order=id_order)
        self.session.add(product)
        self.session.commit()

    def insert_data_order(self, id_order: int, customer_name: str, id_shop: int, date: datetime.datetime) -> None:
        order = Order(id_order=id_order, customer_name=customer_name, id_shop=id_shop, date=date)
        self.session.add(order)
        self.session.commit()

    def insert_data_catalog(self, id_catalog: int, name: str, id_shop: int, pid_catalog: int) -> None:
        catalog = Catalog(id_catalog=id_catalog, name=name, id_shop=id_shop, pid_catalog=pid_catalog)
        self.session.add(catalog)
        self.session.commit()

    def insert_data_shop(self, id_shop: int, address: str, name: str) -> None:
        shop = Shop(id_shop=id_shop, address=address, name=name)
        self.session.add(shop)
        self.session.commit()

    def product_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Product\""
                                    "select (SELECT MAX(id_product)+1 FROM public.\"Product\"), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                                    "FLOOR(RANDOM()*(100000-1)+1),"
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                                    "(SELECT id_catalog FROM public.\"Catalog\" LIMIT 1 OFFSET (round(random() * "
                                    "((SELECT COUNT(id_catalog) FROM public.\"Catalog\")-1)))),"
                                    "(SELECT id_order FROM public.\"Order\" LIMIT 1 OFFSET "
                                    "(round(random() * ((SELECT COUNT(id_order) FROM public.\"Order\")-1))));")

    def order_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"Order\" select (SELECT (MAX(id_order)+1) FROM public.\"Order\"), "
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                "(SELECT id_shop FROM public.\"Shop\" LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id_shop) FROM public.\"Shop\")-1)))), "
                "(SELECT to_timestamp(1549634400+random()*70071999));")

    def catalog_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.\"Catalog\" select (SELECT MAX(id_catalog)+1 FROM public.\"Catalog\"), "
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(15-5)+5):: integer)), ''), "
                "(SELECT id_shop FROM public.\"Shop\" LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id_shop) FROM public.\"Shop\")-1)))), "
                "(SELECT id_catalog FROM public.\"Catalog\" LIMIT 1 OFFSET "
                "(round(random() * ((SELECT COUNT(id_catalog) FROM public.\"Catalog\")-1))));")

    def shop_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Shop\" select (SELECT MAX(id_shop)+1 FROM public.\"Shop\"), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                                    "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                                    "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def search_data_two_tables(self):
        return self.session.query(Product) \
            .join(Catalog) \
            .filter(and_(
                Product.id_product.between(0, 10),
                Catalog.id_shop.between(9656, 9659),
                Catalog.name.ilike('%woman%')
            )) \
            .all()

    def search_data_three_tables(self):
        start_date = datetime.datetime(2021, 8, 31)
        end_date = datetime.datetime(2021, 10, 1)
        return self.session.query(Product) \
            .join(Catalog).join(Order) \
            .filter(and_(
                Product.price.between(400, 20000),
                Order.date.between(start_date, end_date),
                Catalog.name.ilike('%unisex%')
            )) \
            .all()

    def search_data_all_tables(self):
        start_date = datetime.datetime(2021, 9, 1)
        end_date = datetime.datetime(2021, 10, 15)
        return self.session.query(Product) \
            .join(Catalog).join(Order).join(Shop) \
            .filter(and_(
                Product.price.between(100, 1000000),
                Order.date.between(start_date, end_date),
                Shop.id_shop.between(9656, 9659),
                Catalog.name.ilike('%bags%')
            )) \
            .all()
