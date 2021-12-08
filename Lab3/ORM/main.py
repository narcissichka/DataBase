import controller as con
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            args = {"name": sys.argv[2], "val": sys.argv[3]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["val"])

    elif command == 'update_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'Product':
                args["title"], args["price"], args["category"], args["id_catalog"], args["id_order"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
            elif args["name"] == 'Order':
                args["customer"], args["id_shop"], args["date"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Catalog':
                args["catalog_name"], args["id_shop"], args["pid_catalog"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Shop':
                args["address"], args["shop_name"] = \
                    sys.argv[4], sys.argv[5]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'Product':
                c.update_product(args["key"], args["title"], args["price"],
                                 args["category"], args["id_catalog"], args["id_order"])
            elif args["name"] == 'Order':
                c.update_order(args["key"], args["customer"], args["id_shop"], args["date"])
            elif args["name"] == 'Catalog':
                c.update_catalog(args["key"], args["catalog_name"], args["id_shop"], args["pid_catalog"])
            elif args["name"] == 'Shop':
                c.update_shop(args["key"], args["address"], args["shop_name"])

    elif command == 'insert_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'Product':
                args["title"], args["price"], args["category"], args["id_catalog"], args["id_order"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
            elif args["name"] == 'Order':
                args["customer"], args["id_shop"], args["date"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Catalog':
                args["catalog_name"], args["id_shop"], args["pid_catalog"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'Shop':
                args["address"], args["shop_name"] = \
                    sys.argv[4], sys.argv[5]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'Product':
                c.insert_product(args["key"], args["title"], args["price"],
                                 args["category"], args["id_catalog"], args["id_order"])
            elif args["name"] == 'Order':
                c.insert_order(args["key"], args["customer"], args["id_shop"], args["date"])
            elif args["name"] == 'Catalog':
                c.insert_catalog(args["key"], args["catalog_name"], args["id_shop"], args["pid_catalog"])
            elif args["name"] == 'Shop':
                c.insert_shop(args["key"], args["address"], args["shop_name"])

    elif command == 'test':
        print(not c.m.find_product(13))
    elif command == 'generate_randomly':
        try:
            args = {"name": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["name"], args["n"])

    elif command == 'search_records':
        while True:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num in [2, 3, 4]:
                    break
                else:
                    c.v.invalid_search_num()
        if search_num == 2:
            c.search_two()
        elif search_num == 3:
            c.search_three()
        elif search_num == 4:
            c.search_all()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
