import datetime


class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg in ['Product', 'Order', 'Catalog', 'Shop']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        if table_name == 'Product' and key_name == 'id_product' \
                or table_name == 'Order' and key_name == 'id_order' \
                or table_name == 'Catalog' and key_name == 'id_catalog' \
                or table_name == 'Shop' and key_name == 'id_shop':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val, count):
        try:
            value = int(val)
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if count and not count == (0,):
                return value
            else:
                return 0

    def check_key_names(self, table_name: str, key: str):
        if table_name == 'Product' and key in ['id_product', 'id_catalog', 'id_order', 'price', 'title', 'category']:
            return True
        elif table_name == 'Order' and key in ['id_order', 'id_shop', 'customer_name', 'date']:
            return True
        elif table_name == 'Catalog' and key in ['id_catalog', 'id_shop', 'pid_catalog', 'name']:
            return True
        elif table_name == 'Shop' and key in ['id_shop', 'name', 'address']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        if table_name == 'Product':
            if key in ['id_product', 'id_catalog', 'id_order']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['title', 'category']:
                return True
            elif key == 'price':
                try:
                    value = float(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct price value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Product table'
                print(self.error)
                return False
        elif table_name == 'Order':
            if key in ['id_order', 'id_shop']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'customer_name':
                return True
            elif key == 'date':
                try:
                    arr = [int(x) for x in val.split(sep='.')]
                    datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])
                except TypeError:
                    self.er_flag = True
                    self.error = f'{val} is not correct date value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Order table'
                print(self.error)
                return False
        elif table_name == 'Catalog':
            if key in ['id_catalog', 'id_shop', 'pid_catalog']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'name':
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Product table'
                print(self.error)
                return False
        elif table_name == 'Shop':
            if key == 'id_shop':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['name', 'address']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for Product table'
                print(self.error)
                return False
