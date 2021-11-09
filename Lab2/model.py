import datetime
import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                # "postgres", "postgres", "AnnaA.Korzh333:", "127.0.0.1", "5432"
                database="postgres",
                user='postgres',
                password="AnnaA.Korzh333:",
                host='127.0.0.1',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("[INFO] Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.\"{table_name}\"")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.\"{table_name}\" where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.\"{table_name}\"")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.\"{table_name}\"")

    def print_products(self) -> None:
        table = self.get(f"SELECT * FROM public.\"Product\"")
        print('Product table:')
        for row in table:
            print('id_product:', row[0], '\ttitle:', row[1], '\tprice:', row[2], '\tcategory:', row[3],
                  '\tid_catalog:', row[4], '\tid_order:', row[5])
            print('_____________________________________')

    def print_order(self) -> None:
        table = self.get(f"SELECT * FROM public.\"Order\"")
        print('Order table:')
        for row in table:
            print('id_order:', row[0], '\tcustomer_name:', row[1], '\tid_shop:', row[2], '\tdate:', row[3])
            print('_____________________________________')

    def print_catalog(self) -> None:
        table = self.get(f"SELECT * FROM public.\"Catalog\"")
        print('Catalog table:')
        for row in table:
            print('id_catalog:', row[0], '\tname:', row[1], '\tid_shop:', row[2], '\tpid_catalog:', row[3])
            print('_____________________________________')

    def print_shop(self) -> None:
        table = self.get(f"SELECT * FROM public.\"Shop\"")
        print('Shop table:')
        for row in table:
            print('id_shop:', row[0], '\taddress:', row[1], '\tname:', row[2])
            print('_____________________________________')

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.\"{table_name}\" WHERE {key_name}={key_value};")

    def update_data_product(self, key_value: int, title: str, price: float, category: str,
                            id_catalog: int, id_order: int) -> None:
        self.request(f"UPDATE public.\"Product\" SET title=\'{title}\', price={price}, category=\'{category}\', "
                     f"id_catalog={id_catalog}, id_order={id_order} WHERE id_product={key_value};")

    def update_data_order(self, key_value: int, customer_name: str, id_shop: int, date: datetime.datetime) -> None:
        self.request(f"UPDATE public.\"Order\" SET customer_name=\'{customer_name}\', id_shop={id_shop}, "
                     f"date=\'{date}\' WHERE id_order={key_value};")

    def update_data_catalog(self, key_value: int, name: str, id_shop: int, pid_catalog: int) -> None:
        self.request(f"UPDATE public.\"Catalog\" SET name=\'{name}\', id_shop={id_shop}, "
                     f"pid_catalog={pid_catalog} WHERE id_order={key_value};")

    def update_data_shop(self, key_value: int, address: str, name: str) -> None:
        self.request(f"UPDATE public.\"Shop\" SET address=\'{address}\', "
                     f"name=\'{name}\' WHERE id_shop={key_value};")

    def insert_data_product(self, id_product: int, title: str, price: float, category: str, id_catalog: int,
                            id_order: int) -> None:
        self.request(f"insert into public.\"Product\" (id_product, title, price, category, id_catalog, id_order) "
                     f"VALUES ({id_product}, \'{title}\', {price}, \'{category}\', {id_catalog}, {id_order});")

    def insert_data_order(self, id_order: int, customer_name: str, id_shop: int, date: datetime.datetime) -> None:
        self.request(f"insert into public.\"Order\" (id_order, customer_name, id_shop, date) "
                     f"VALUES ({id_order}, \'{customer_name}\', {id_shop}, \'{date}\');")

    def insert_data_catalog(self, id_catalog: int, name: str, id_shop: int, pid_catalog: int) -> None:
        self.request(f"insert into public.\"Catalog\" (id_catalog, name, id_shop, pid_catalog) "
                     f"VALUES ({id_catalog}, \'{name}\', {id_shop}, {pid_catalog});")

    def insert_data_shop(self, id_shop: int, address: str, name: str) -> None:
        self.request(f"insert into public.\"Shop\" (id_shop, address, name) "
                     f"VALUES ({id_shop}, \'{address}\', \'{name}\');")

    def product_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Product\""
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
            self.request("insert into public.\"Order\" select (SELECT (MAX(id_order)+1) FROM public.\"Order\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                         "(SELECT id_shop FROM public.\"Shop\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id_shop) FROM public.\"Shop\")-1)))), "
                         "(SELECT to_timestamp(1549634400+random()*70071999));")

    def catalog_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Catalog\" select (SELECT MAX(id_catalog)+1 FROM public.\"Catalog\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(15-5)+5):: integer)), ''), "
                         "(SELECT id_shop FROM public.\"Shop\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id_shop) FROM public.\"Shop\")-1)))), "
                         "(SELECT id_catalog FROM public.\"Catalog\" LIMIT 1 OFFSET "
                         "(round(random() * ((SELECT COUNT(id_catalog) FROM public.\"Catalog\")-1))));")

    def shop_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.\"Shop\" select (SELECT MAX(id_shop)+1 FROM public.\"Shop\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        found = self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                         f"on one.\"{table1_key}\"=two.\"{table2_key}\" "
                         f"where {search}")
        print('search result:')
        for row in found:
            for i in range(0, len(row)):
                print(row[i])
            print('_____________________________________')

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        found = self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                         f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                         f"on three.\"{table3_key}\"=one.\"{table13_key}\""
                         f"where {search}")
        print('search result:')
        for row in found:
            for i in range(0, len(row)):
                print(row[i])
            print('_____________________________________')

    def search_data_all_tables(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                               table1_key, table2_key, table3_key, table13_key,
                               table4_key, table24_key,
                               search: str):
        found = self.get(f"select * from public.\"{table1_name}\" as one inner join public.\"{table2_name}\" as two "
                         f"on one.\"{table1_key}\"=two.\"{table2_key}\" inner join public.\"{table3_name}\" as three "
                         f"on three.\"{table3_key}\"=one.\"{table13_key}\" inner join public.\"{table4_name}\" as four "
                         f"on four.\"{table4_key}\"=two.\"{table24_key}\""
                         f"where {search}")
        print('search result:')
        for row in found:
            for i in range(0, len(row)):
                print(row[i])
            print('_____________________________________')

    def numeric_search(self, a: int, b: int, key: str):
        return f"{a}<{key} and {key}<{b}"

    def string_search(self, string: str, key: str):
        return f"{key} LIKE \'{string}\'"

    def date_search(self, datetime1: datetime.datetime, datetime2: datetime.datetime, key: str):
        return f"{key} BETWEEN \'{datetime1}\' AND \'{datetime2}\'"
