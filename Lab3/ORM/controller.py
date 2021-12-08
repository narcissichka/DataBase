from psycopg2 import Error
import model
import view
import datetime


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Product':
                self.v.print_product(self.m.print_products())
            elif t_name == 'Order':
                self.v.print_order(self.m.print_order())
            elif t_name == 'Catalog':
                self.v.print_catalog(self.m.print_catalog())
            elif t_name == 'Shop':
                self.v.print_shop(self.m.print_shop())

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            k_val = self.v.valid.check_pk(value)
            count = 0
            if t_name == 'Product' and k_val:
                count = self.m.find_pk_product(k_val)
            elif t_name == 'Order' and k_val:
                count = self.m.find_pk_order(k_val)
            elif t_name == 'Catalog' and k_val:
                count = self.m.find_pk_catalog(k_val)
            elif t_name == 'Shop' and k_val:
                count = self.m.find_pk_shop(k_val)

            if count:
                if t_name == 'Order' or t_name == 'Catalog':
                    count_p = self.m.find_fk_product(k_val, t_name)
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'Order':
                                self.m.delete_data_order(k_val)
                            elif t_name == 'Catalog':
                                self.m.delete_data_catalog(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'Shop':
                    count_c = self.m.find_fk_catalog(k_val)
                    count_o = self.m.find_fk_order(k_val)
                    if count_c or count_o:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_shop(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data_products(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_product(self, key: str, title: str, price: str, category: str, id_catalog: str, id_order: str):
        if self.v.valid.check_possible_keys('Product', 'id_product', key):
            count_p = self.m.find_pk_product(int(key))
            p_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Catalog', 'id_catalog', id_catalog):
            count_c = self.m.find_pk_catalog(int(id_catalog))
            c_val = self.v.valid.check_pk(id_catalog)
        if self.v.valid.check_possible_keys('Order', 'id_order', id_order):
            count_o = self.m.find_pk_order(int(id_order))
            o_val = self.v.valid.check_pk(id_order)

        if count_p and count_c and count_o and \
                c_val and o_val and p_val and \
                self.v.valid.check_possible_keys('Product', 'price', price):
            try:
                self.m.update_data_product(p_val, title, float(price),
                                           category, c_val, o_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_order(self, key: str, customer_name: str, id_shop: str, date: str):
        if self.v.valid.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find_pk_shop(int(id_shop))
            s_val = self.v.valid.check_pk(id_shop)
        if self.v.valid.check_possible_keys('Order', 'id_order', key):
            count_o = self.m.find_pk_order(int(key))
            o_val = self.v.valid.check_pk(key)

        if count_s and count_o and \
                s_val and o_val and \
                self.v.valid.check_possible_keys('Order', 'date', date):
            try:
                arr = [int(x) for x in date.split(sep='.')]
                self.m.update_data_order(o_val, customer_name, s_val,
                                         datetime.datetime(arr[0], arr[1], arr[2],
                                                           arr[3], arr[4], arr[5]))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_catalog(self, key: str, name: str, id_shop: str, pid_catalog: str):
        if self.v.valid.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find_pk_shop(int(id_shop))
            s_val = self.v.valid.check_pk(id_shop)
        if self.v.valid.check_possible_keys('Catalog', 'id_catalog', key):
            count_c = self.m.find_pk_catalog(int(key))
            c_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Catalog', 'pid_catalog', pid_catalog):
            count_pc = self.m.find_pk_catalog(int(pid_catalog))
            pc_val = self.v.valid.check_pk(pid_catalog)

        if count_s and count_c and count_pc and \
                s_val and c_val and pc_val:
            try:
                self.m.update_data_catalog(c_val, name, s_val, pc_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_shop(self, key: str, address: str, name: str):
        if self.v.valid.check_possible_keys('Shop', 'id_shop', key):
            count_s = self.m.find_pk_shop(int(key))
            s_val = self.v.valid.check_pk(key)

        if count_s and s_val:
            try:
                self.m.update_data_shop(s_val, address, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_product(self, key: str, title: str, price: str, category: str, id_catalog: str, id_order: str):
        if self.v.valid.check_possible_keys('Product', 'id_product', key):
            count_p = self.m.find_pk_product(int(key))
        if self.v.valid.check_possible_keys('Catalog', 'id_catalog', id_catalog):
            count_c = self.m.find_pk_catalog(int(id_catalog))
            c_val = self.v.valid.check_pk(id_catalog)
        if self.v.valid.check_possible_keys('Order', 'id_order', id_order):
            count_o = self.m.find_pk_order(int(id_order))
            o_val = self.v.valid.check_pk(id_order)

        if (not count_p) and count_c and count_o and c_val and o_val \
                and self.v.valid.check_possible_keys('Product', 'id_product', key) \
                and self.v.valid.check_possible_keys('Product', 'price', price):
            try:
                self.m.insert_data_product(int(key), title, float(price),
                                           category, c_val, o_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_order(self, key: str, customer_name: str, id_shop: str, date: str):
        if self.v.valid.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find_pk_shop(int(id_shop))
            s_val = self.v.valid.check_pk(id_shop)
        if self.v.valid.check_possible_keys('Order', 'id_order', key):
            count_o = self.m.find_pk_order(int(key))

        if (not count_o) and count_s and s_val and self.v.valid.check_possible_keys('Order', 'id_order', key) \
                and self.v.valid.check_possible_keys('Order', 'date', date):
            try:
                arr = [int(x) for x in date.split(sep='.')]
                self.m.insert_data_order(int(key), customer_name, s_val,
                                         datetime.datetime(arr[0], arr[1], arr[2],
                                                           arr[3], arr[4], arr[5]))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_catalog(self, key: str, name: str, id_shop: str, pid_catalog: str):
        if self.v.valid.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find_pk_shop(int(id_shop))
            s_val = self.v.valid.check_pk(id_shop)
        if self.v.valid.check_possible_keys('Catalog', 'id_catalog', key):
            count_c = self.m.find_pk_catalog(int(key))
        if self.v.valid.check_possible_keys('Catalog', 'pid_catalog', pid_catalog):
            count_pc = self.m.find_pk_catalog(int(pid_catalog))
            pc_val = self.v.valid.check_pk(pid_catalog)

        if (not count_c) and count_s and count_pc and s_val and pc_val \
                and self.v.valid.check_possible_keys('Catalog', 'id_catalog', key):
            try:
                self.m.insert_data_catalog(int(key), name, s_val, pc_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_shop(self, key: str, address: str, name: str):
        if self.v.valid.check_possible_keys('Shop', 'id_shop', key):
            count_s = self.m.find_pk_shop(int(key))

        if (not count_s) and self.v.valid.check_possible_keys('Shop', 'id_shop', key):
            try:
                self.m.insert_data_shop(int(key), address, name)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'Product':
                self.m.product_data_generator(n)
            elif t_name == 'Order':
                self.m.order_data_generator(n)
            elif t_name == 'Catalog':
                self.m.catalog_data_generator(n)
            elif t_name == 'Shop':
                self.m.shop_data_generator(n)

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_all(self):
        result = self.m.search_data_all_tables()
        self.v.print_search(result)
