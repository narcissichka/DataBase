import controller as con
from psycopg2 import Error
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    print('no command name specified, type help to see possible commands')
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            print('no table name specified')
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            name = sys.argv[2]
            key = sys.argv[3]
            val = sys.argv[4]
        except IndexError:
            print('no needed arguments specified')
        else:
            c.delete(name, key, val)

    elif command == 'update_record':
        try:
            name = sys.argv[2]
            key = sys.argv[3]
            if name == 'Product':
                title = sys.argv[4]
                price = sys.argv[5]
                category = sys.argv[6]
                id_catalog = sys.argv[7]
                id_order = sys.argv[8]
            elif name == 'Order':
                customer = sys.argv[4]
                id_shop = sys.argv[5]
                date = sys.argv[6]
            elif name == 'Catalog':
                catalog_name = sys.argv[4]
                id_shop = sys.argv[5]
                pid_catalog = sys.argv[6]
            elif name == 'Shop':
                address = sys.argv[4]
                shop_name = sys.argv[5]
            else:
                print('wrong table name')
        except IndexError:
            print('no required arguments specified')
        else:
            if name == 'Product':
                c.update_product(key, title, price, category, id_catalog, id_order)
            elif name == 'Order':
                c.update_order(key, customer, id_shop, date)
            elif name == 'Catalog':
                c.update_catalog(key, catalog_name, id_shop, pid_catalog)
            elif name == 'Shop':
                c.update_shop(key, address, shop_name)

    elif command == 'insert_record':
        try:
            name = sys.argv[2]
            key = sys.argv[3]
            if name == 'Product':
                title = sys.argv[4]
                price = sys.argv[5]
                category = sys.argv[6]
                id_catalog = sys.argv[7]
                id_order = sys.argv[8]
            elif name == 'Order':
                customer = sys.argv[4]
                id_shop = sys.argv[5]
                date = sys.argv[6]
            elif name == 'Catalog':
                catalog_name = sys.argv[4]
                id_shop = sys.argv[5]
                pid_catalog = sys.argv[6]
            elif name == 'Shop':
                address = sys.argv[4]
                shop_name = sys.argv[5]
            else:
                print('wrong table name')
        except IndexError:
            print('no required arguments specified')
        else:
            if name == 'Product':
                c.insert_product(key, title, price, category, id_catalog, id_order)
            elif name == 'Order':
                c.insert_order(key, customer, id_shop, date)
            elif name == 'Catalog':
                c.insert_catalog(key, catalog_name, id_shop, pid_catalog)
            elif name == 'Shop':
                c.insert_shop(key, address, shop_name)

    elif command == 'generate_randomly':
        try:
            name = sys.argv[2]
            n = int(sys.argv[3])
        except (IndexError, Error):
            print(Error, IndexError)
        else:
            c.generate(name, n)

    elif command == 'search_records':
        table4_name = ''
        table3_name = ''
        fl = True
        if len(sys.argv) == 6:
            table1_name = sys.argv[2]
            table2_name = sys.argv[3]
            key1_name = sys.argv[4]
            key2_name = sys.argv[5]
        elif len(sys.argv) == 9:
            table1_name = sys.argv[2]
            table2_name = sys.argv[3]
            table3_name = sys.argv[4]
            key1_name = sys.argv[5]
            key2_name = sys.argv[6]
            key3_name = sys.argv[7]
            key13_name = sys.argv[8]
        elif len(sys.argv) == 12:
            table1_name = sys.argv[2]
            table2_name = sys.argv[3]
            table3_name = sys.argv[4]
            table4_name = sys.argv[5]
            key1_name = sys.argv[6]
            key2_name = sys.argv[7]
            key3_name = sys.argv[8]
            key13_name = sys.argv[9]
            key4_name = sys.argv[10]
            key24_name = sys.argv[11]
        else:
            print('wrong number of attributes')
            fl = False

        if fl:
            search_num = input('specify the number of attributes you`d like to search by: ')
            try:
                search_num = int(search_num)
            except ValueError:
                print('should be number different from 0')
            else:
                if search_num > 0:
                    search = ''
                    for i in range(0, search_num):
                        while True:
                            search_type = input('specify the type of data you want to search for '
                                                '(numeric, string or date): ')
                            if search_type == 'numeric' or search_type == 'string' or search_type == 'date':
                                break
                        key = input('specify the name of key by which you`d like to perform search '
                                    'in form: table_number.key_name: ')

                        if search_type == 'numeric':
                            a = input('specify the left end of search interval: ')
                            b = input('specify the right end of search interval: ')
                            if search == '':
                                search = c.num_search(a, b, key)
                            else:
                                search += ' and ' + c.num_search(a, b, key)

                        elif search_type == 'date':
                            data = input('specify the left end of search interval '
                                         'in form: year.month.day.hour.minute.second: ')
                            datb = input('specify the right end of search interval '
                                         'in form: year.month.day.hour.minute.second: ')
                            if search == '':
                                search = c.date_search(data, datb, key)
                            else:
                                search += ' and ' + c.date_search(data, datb, key)

                        elif search_type == 'string':
                            string = input('specify the string you`d like to search for: ')
                            if search == '':
                                search = c.str_search(string, key)
                            else:
                                search += ' and ' + c.str_search(string, key)

                    if table4_name != '':
                        c.search_four(table1_name, table2_name, table3_name, table4_name,
                                      key1_name, key2_name, key3_name, key13_name, key4_name,
                                      key24_name, search)
                    elif table3_name != '':
                        c.search_three(table1_name, table2_name, table3_name,
                                       key1_name, key2_name, key3_name, key13_name,
                                       search)
                    else:
                        c.search_two(table1_name, table2_name, key1_name, key2_name,
                                     search)
                else:
                    print('should be number different from 0')

    elif command == 'help':
        print('print_table - outputs the specified table \n\targument (table_name) is required')
        print('delete_record - deletes the specified record from table \n'
              '\targuments (table_name, key_name, key_value) are required')
        print('update_record - updates record with specified id in table\n'
              '\tProduct args (table_name, id_product, title, price, category, id_catalog, id_order)\n'
              '\tOrder args (table_name, id_order, customer_name, id_shop, date)\n'
              '\tCatalog args (table_name, id_catalog, name, id_shop, pid_catalog)\n'
              '\tShop args (table_name, id_shop, address, name)')
        print('insert_record - inserts record into specified table \n'
              '\tProduct args (table_name, id_product, title, price, category, id_catalog, id_order)\n'
              '\tOrder args (table_name, id_order, customer_name, id_shop, date)\n'
              '\tCatalog args (table_name, id_catalog, name, id_shop, pid_catalog)\n'
              '\tShop args (table_name, id_shop, address, name)')
        print('generate_randomly - generates n random records in table\n'
              '\targuments (table_name, n) are required')
        print('search_records - search for records in two or more tables using one or more keys \n'
              '\targuments (table1_name, table2_name, table1_key, table2_key) are required, \n'
              '\tif you want to perform search in more tables: \n'
              '\t(table1_name, table2_name, table3_name, table1_key, table2_key, table3_key, table13_key) \n'
              '\t(table1_name, table2_name, table3_name, table4_name, table1_key, table2_key, table3_key, table13_key, '
              'table4_key, table24_key)')
    else:
        print('unknown command name, type "help" to see possible commands')
