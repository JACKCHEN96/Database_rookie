
from src.CSVDataTable import CSVDataTable
import logging
import os
import time
import json


# The logging level to use should be an environment variable, not hard coded.
logging.basicConfig(level=logging.DEBUG)

# Also, the 'name' of the logger to use should be an environment variable.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# This should also be an environment variable.
# Also not the using '/' is OS dependent, and windows might need `\\`
data_dir = os.path.abspath("../Data/Baseball")


def t_load():

    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }

    csv_tbl = CSVDataTable("salaries", connect_info, None)

    print("Created table = " + str(csv_tbl))


def t_find_by_primary_key_and_template():
    connect_info={
        "directory":data_dir,
        "file_name":"Salaries.csv"
    }
    csv_tbl=CSVDataTable("Salaries", connect_info, key_columns=['playerID'])
    r=csv_tbl.find_by_primary_key(['barkele01'],
        field_list=['yearID','teamID','lgID','playerID','salary'])
    print("find by key return:"+str(r))
    # t={"playerID":"willite01"}
    t = {"yearID": "1985","playerID":"barkele01","salary":"870000"}

    r=csv_tbl.find_by_template(t,
                               field_list=['yearID','teamID','lgID','playerID','salary'])

    print("find by template return:"+str(r))


def insert_test():
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, key_columns=['playerID'])
    new_record = {"yearID":"1977","playerID":"EEEE"}
    csv_tbl.insert(new_record)
    # new_record["yearID"] = "1998"
    # csv_tbl.insert(new_record)
    # new_record["yearID"] = "1997"
    # csv_tbl.insert(new_record)
    tmp= {"yearID": "1977","playerID":"EEEE"}
    r=csv_tbl.find_by_template(template=tmp)
    print("inserted:"+str(r))


def delete_by_key_test(key_fields=None):
    """
    :param data_table:
    :param key_fields:
    :return:
    """
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, key_columns=['playerID'])
    # csv_tbl = CSVDataTable("Salaries", connect_info, key_columns=['salary'])
    key_fields = ["barkele01"]
    affected_num = csv_tbl.delete_by_key(key_fields)
    print("performing delete_by_key_test")
    print("deleted and the affected_num is:")
    print(affected_num)


def delete_by_template_test(template=None):
    """
    :param data_table:
    :param template:
    :return:
    """
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, key_columns=['playerID'])
    template = {'playerID':'barkele01'}
    affected_num = csv_tbl .delete_by_template(template)
    print("performing delete_by_template_test")
    print("deleted and affected_num is:")
    print(affected_num)
    # print("Lets check if its deletd")
    # res = csv_tbl.find_by_template(template,
    #                            ['yearID','teamID','lgID','playerID','salary'])
    # print(res)


def update_by_template_test(template=None, new_values=None):
    """
    :param data_table:
    :param template:
    :param new_values:
    :return:
    """
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, key_columns=['playerID'])
    template = {"playerID":"barkele01","yearID": "1985"}
    new_values = {"yearID": "1777"}
    affected_num = csv_tbl.update_by_template(template=template, new_values=new_values)
    print("performing update_by_template_test")
    print("updated and the affected_num is:")
    print(affected_num)


def update_by_key_test(key_fields=None, new_values=None):
    """
    :param data_table:
    :param key_fields:
    :param new_values:
    :return:
    """
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, key_columns=['playerID'])
    key_fields = ["barkele01"]
    new_values = {"playerID": "barkele01"}
    affected_num = csv_tbl.update_by_key(key_fields=key_fields, new_values=new_values)
    print("performing update_by_key_test")
    print("updated and the affected_num is:")
    print(affected_num)


t_load()
t_find_by_primary_key_and_template()
# insert_test()
# delete_by_key_test()
# delete_by_template_test()
# update_by_template_test()
# update_by_key_test()