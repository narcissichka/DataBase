import psycopg2
from psycopg2 import Error
import model
import view
import datetime
import time

class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.check_table_name(table_name)
        if t_name:
            if t_name == 'Product':
                self.m.print_products()
            elif t_name == 'Order':
                self.m.print_order()
            elif t_name == 'Catalog':
                self.m.print_catalog()
            elif t_name == 'Shop':
                self.m.print_shop()

    def delete(self, table_name, key_name, value):
        t_name = self.v.check_table_name(table_name)
        k_name = self.v.check_pk_name(table_name, key_name)
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.check_pk(value, count)
            if k_val:
                if t_name == 'Order' or t_name == 'Catalog':
                    count_p = self.m.find('Product', k_name, value)[0]
                    if count_p:
                        print('this record is connected with Product table, deleting will '
                              'throw error')
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            print("[INFO] Error while working with Postgresql", _ex)
                elif t_name == 'Shop':
                    count_c = self.m.find('Catalog', k_name, value)[0]
                    count_o = self.m.find('Order', k_name, value)[0]
                    if count_c or count_o:
                        print('this record is connected with another table, deleting will '
                              'throw error')
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            print("[INFO] Error while working with Postgresql", _ex)
                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        print("[INFO] Error while working with Postgresql", _ex)
            else:
                print('record with such id does not exist')

    def update_product(self, key: str, title: str, price: str, category: str, id_catalog: str, id_order: str):
        if self.v.check_possible_keys('Product', 'id_product', key):
            count_p = self.m.find('Product', 'id_product', int(key))
            p_val = self.v.check_pk(key, count_p)
        if self.v.check_possible_keys('Catalog', 'id_catalog', id_catalog):
            count_c = self.m.find('Catalog', 'id_catalog', int(id_catalog))
            c_val = self.v.check_pk(id_catalog, count_c)
        if self.v.check_possible_keys('Order', 'id_order', id_order):
            count_o = self.m.find('Order', 'id_order', int(id_order))
            o_val = self.v.check_pk(id_order, count_o)

        if c_val and o_val and p_val and self.v.check_possible_keys('Product', 'price', price):
            try:
                self.m.update_data_product(p_val, title, float(price),
                                           category, c_val, o_val)
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id does not exist or inappropriate foreign key value)')

    def update_order(self, key: str, customer_name: str, id_shop: str, date: str):
        if self.v.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find('Shop', 'id_shop', int(id_shop))
            s_val = self.v.check_pk(id_shop, count_s)
        if self.v.check_possible_keys('Order', 'id_order', key):
            count_o = self.m.find('Order', 'id_order', int(key))
            o_val = self.v.check_pk(key, count_o)

        if s_val and o_val and self.v.check_possible_keys('Order', 'date', date):
            try:
                arr = [int(x) for x in date.split(sep='.')]
                self.m.update_data_order(o_val, customer_name, s_val,
                                         datetime.datetime(arr[0], arr[1], arr[2],
                                                           arr[3], arr[4], arr[5]))
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id does not exist or inappropriate foreign key value)')

    def update_catalog(self, key: str, name: str, id_shop: str, pid_catalog: str):
        if self.v.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find('Shop', 'id_shop', int(id_shop))
            s_val = self.v.check_pk(id_shop, count_s)
        if self.v.check_possible_keys('Catalog', 'id_catalog', key):
            count_c = self.m.find('Catalog', 'id_catalog', int(key))
            c_val = self.v.check_pk(key, count_c)
        if self.v.check_possible_keys('Catalog', 'pid_catalog', pid_catalog):
            count_pc = self.m.find('Catalog', 'id_catalog', int(pid_catalog))
            pc_val = self.v.check_pk(pid_catalog, count_pc)

        if s_val and c_val and pc_val:
            try:
                self.m.update_data_catalog(c_val, name, s_val, pc_val)
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id does not exist or inappropriate foreign key value)')

    def update_shop(self, key: str, address: str, name: str):
        if self.v.check_possible_keys('Shop', 'id_shop', key):
            count_s = self.m.find('Shop', 'id_shop', int(key))
            s_val = self.v.check_pk(key, count_s)

        if s_val:
            try:
                self.m.update_data_shop(s_val, address, name)
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id does not exist)')

    def insert_product(self, key: str, title: str, price: str, category: str, id_catalog: str, id_order: str):
        if self.v.check_possible_keys('Product', 'id_product', key):
            count_p = self.m.find('Product', 'id_product', int(key))[0]
        if self.v.check_possible_keys('Catalog', 'id_catalog', id_catalog):
            count_c = self.m.find('Catalog', 'id_catalog', int(id_catalog))
            c_val = self.v.check_pk(id_catalog, count_c)
        if self.v.check_possible_keys('Order', 'id_order', id_order):
            count_o = self.m.find('Order', 'id_order', int(id_order))
            o_val = self.v.check_pk(id_order, count_o)

        if (not count_p or count_p == (0,)) and c_val and o_val and self.v.check_possible_keys('Product', 'id_product', key) \
                and self.v.check_possible_keys('Product', 'price', price):
            try:
                self.m.insert_data_product(int(key), title, float(price),
                                           category, c_val, o_val)
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id exists or inappropriate foreign key values)')

    def insert_order(self, key: str, customer_name: str, id_shop: str, date: str):
        if self.v.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find('Shop', 'id_shop', int(id_shop))
            s_val = self.v.check_pk(id_shop, count_s)
        if self.v.check_possible_keys('Order', 'id_order', key):
            count_o = self.m.find('Order', 'id_order', int(key))[0]

        if (not count_o or count_o == (0,)) and s_val and self.v.check_possible_keys('Order', 'id_order', key) \
                and self.v.check_possible_keys('Order', 'date', date):
            try:
                arr = [int(x) for x in date.split(sep='.')]
                self.m.insert_data_order(int(key), customer_name, s_val,
                                         datetime.datetime(arr[0], arr[1], arr[2],
                                                           arr[3], arr[4], arr[5]))
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id exists or inappropriate foreign key values)')

    def insert_catalog(self, key: str, name: str, id_shop: str, pid_catalog: str):
        if self.v.check_possible_keys('Shop', 'id_shop', id_shop):
            count_s = self.m.find('Shop', 'id_shop', int(id_shop))
            s_val = self.v.check_pk(id_shop, count_s)
        if self.v.check_possible_keys('Catalog', 'id_catalog', key):
            count_c = self.m.find('Catalog', 'id_catalog', int(key))[0]
        if self.v.check_possible_keys('Catalog', 'pid_catalog', pid_catalog):
            count_pc = self.m.find('Catalog', 'id_catalog', int(pid_catalog))
            pc_val = self.v.check_pk(pid_catalog, count_pc)

        if (not count_c or count_c == (0,)) and s_val and pc_val and self.v.check_possible_keys('Catalog', 'id_catalog', key):
            try:
                self.m.insert_data_catalog(int(key), name, s_val, pc_val)
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id exists or inappropriate foreign key values)')

    def insert_shop(self, key: str, address: str, name: str):
        if self.v.check_possible_keys('Shop', 'id_shop', key):
            count_s = self.m.find('Shop', 'id_shop', int(key))[0]

        if not (not count_s or count_s == (0,)) and self.v.check_possible_keys('Shop', 'id_shop', key):
            try:
                self.m.insert_data_shop(int(key), address, name)
            except (Exception, Error) as _ex:
                print("[INFO] Error while working with Postgresql", _ex)
        else:
            print('Something went wrong (record with such id exists or inappropriate foreign key values)')

    def generate(self, table_name: str, n: int):
        t_name = self.v.check_table_name(table_name)
        if t_name:
            if t_name == 'Product':
                self.m.product_data_generator(n)
            elif t_name == 'Order':
                self.m.order_data_generator(n)
            elif t_name == 'Catalog':
                self.m.catalog_data_generator(n)
            elif t_name == 'Shop':
                self.m.shop_data_generator(n)

    def num_search(self, a: str, b: str, key: str):
        try:
            search = self.m.numeric_search(int(a), int(b), key)
        except ValueError:
            print('invalid interval input')
        else:
            return search

    def date_search(self, a: str, b: str, key: str):
        try:
            arr = [int(x) for x in a.split(sep='.')]
            brr = [int(x) for x in b.split(sep='.')]
            search = self.m.date_search(
                    datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]),
                    datetime.datetime(brr[0], brr[1], brr[2], brr[3], brr[4], brr[5]),
                    key)
        except ValueError:
            print('invalid interval input')
        else:
            return search

    def str_search(self, string: str, key: str):
        search = self.m.string_search(string, key)
        return search

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.check_table_name(table1_name)
        t2_n = self.v.check_table_name(table2_name)
        if t1_n and self.v.check_key_names(t1_n, table1_key) and t2_n and self.v.check_key_names(t2_n, table2_key):
            start_time = time.time()
            self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                          search)
            print("--- %s seconds ---" % (time.time() - start_time))

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.check_table_name(table1_name)
        t2_n = self.v.check_table_name(table2_name)
        t3_n = self.v.check_table_name(table3_name)
        if t1_n and self.v.check_key_names(t1_n, table1_key) and self.v.check_key_names(t1_n, table13_key) and \
           t2_n and self.v.check_key_names(t2_n, table2_key) and \
           t3_n and self.v.check_key_names(t3_n, table3_key) and self.v.check_key_names(t3_n, table13_key):
            start_time = time.time()
            self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                            table1_key, table2_key, table3_key, table13_key,
                                            search)
            print("--- %s seconds ---" % (time.time() - start_time))

    def search_four(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                    table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                    table4_key: str, table24_key: str,
                    search: str):
        t1_n = self.v.check_table_name(table1_name)
        t2_n = self.v.check_table_name(table2_name)
        t3_n = self.v.check_table_name(table3_name)
        t4_n = self.v.check_table_name(table2_name)
        if t1_n and self.v.check_key_names(t1_n, table1_key) and self.v.check_key_names(t1_n, table13_key) and \
           t2_n and self.v.check_key_names(t2_n, table2_key) and self.v.check_key_names(t2_n, table24_key) and \
           t3_n and self.v.check_key_names(t3_n, table3_key) and self.v.check_key_names(t3_n, table13_key) and \
           t4_n and self.v.check_key_names(t4_n, table4_key) and self.v.check_key_names(t4_n, table24_key):
            start_time = time.time()
            self.m.search_data_all_tables(table1_name, table2_name, table3_name, table4_name,
                                          table1_key, table2_key, table3_key, table13_key,
                                          table4_key, table24_key,
                                          search)
            print("--- %s seconds ---" % (time.time() - start_time))

    def test(self):
        print(self.m.find('Product', 'id_order', 1300)[0])

