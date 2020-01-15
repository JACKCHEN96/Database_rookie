import pymysql
from src.RDBDataTable import RDBDataTable


def init_data_table_test(table_name=None,connect_info=None,key_columns=None):
    table_name="people"
    connect_info={
        'host': 'localhost',
        'user': 'root',
        # 'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'HW1_0918',
        # 'db': 'ClassicModels',
        'charset':'utf8mb4',
        'port': 3306
    }
    key_columns=['playerID']
    # key_columns=['nameFirst']
    csv_data_table=RDBDataTable(table_name=table_name,connect_info=connect_info,key_columns=key_columns)
    return csv_data_table


def find_by_template_test(data_table, template=None, field_list=None):
    """
    :param data_table:
    :param key_fields:
    :param field_list:
    :return:
    """

    template = {"nameFirst": "wenjie", "nameLast": "Chen","birthYear":"1996"}
    res = data_table.find_by_template(template)
    print("perfoming find_by_template_test:")
    print(res)


def find_by_primary_key_test(data_table, key_fields=None, field_list=None):
    """
    :param data_table:
    :param key_fields:
    :param field_list:
    :return:
    """
    key_fields = ["wc2685"]
    field_list=['playerID','nameLast','nameFirst']
    res = data_table.find_by_primary_key(key_fields=key_fields, field_list=field_list)
    print("perfoming find_by_primary_key_test:")
    print(res)


def delete_by_template_test(data_table, template=None):
    """
    :param data_table:
    :param template:
    :return:
    """
    template = {"nameFirst": "Wenjie", "nameLast": "Chen"}
    affected_num = data_table.delete_by_template(template)
    print("performing delete_by_template_test:")
    print("deleted and the affected_num is:")
    print(affected_num)


def delete_by_key_test(data_table, key_fields=None):
    """
    :param data_table:
    :param key_fields:
    :return:
    """
    # test case
    key_fields = ["wc2685"]
    affected_num = data_table.delete_by_key(key_fields)
    print("perfoming delete_by_key_test:")
    print("deleted and the affected_num is:")
    print(affected_num)


def insert_test(data_table,key_fields=None):
    new_record={
        "playerID": "wc2685",
        "nameLast": "Chen",
        "nameFirst":"Wenjie",
        "birthYear":"1996"
    }
    data_table.insert(new_record)
    template={"playerID":"1996"}
    new_values={"playerID":"WC2685"}
    affected_num=data_table.update_by_template(template=template,new_values=new_values)
    print("insert:")
    print(new_record)
    # print("affected_num:")
    # print(affected_num)


def update_by_key_test(data_table, key_fields=None, new_values=None):
    """
    :param data_table:
    :param key_fields:
    :param new_values:
    :return:
    """
    key_fields = ["abbeybe01"]
    new_values = {"playerID": "wc2685", "nameFirst": "Jack"}
    affected_num = data_table.update_by_key(key_fields=key_fields, new_values=new_values)
    print("perfoming update_by_key_test:")
    print("updated and the affected_num is:")
    print(affected_num)


def update_by_template_test(data_table, template=None, new_values=None):
    """
    :param data_table:
    :param template:
    :param new_values:
    :return:
    """
    template = {"playerID": "abbeych01", "nameFirst": "Charlie"}
    new_values = {"playerID": "wc2685", "nameFirst": "WENJIE"}
    affected_num = data_table.update_by_template(template=template, new_values=new_values)
    print("perfoming update_by_template_test:")
    print("updated and the affected_num is:")
    print(affected_num)


data_table_1=init_data_table_test()
insert_test(data_table=data_table_1)
# delete_by_template_test(data_table=data_table_1)
# delete_by_key_test(data_table=data_table_1)
# find_by_template_test(data_table=data_table_1)
# find_by_primary_key_test(data_table=data_table_1)
# update_by_key_test(data_table=data_table_1)
# update_by_template_test(data_table=data_table_1)

