# I write and test methods one at a time.
# This file contains unit tests of individual methods.

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
        "file_name":"People.csv"
    }
    csv_tbl=CSVDataTable("people", connect_info, key_columns=['playerID'])
    r=csv_tbl.find_by_primary_key(['willite01'],
        field_list=['playerID','nameLast','throws','bats','birthCountry'])
    print("find by key return:"+str(r))
    # t={"playerID":"willite01"}
    t={"nameLast":"Williams"}

    r=csv_tbl.find_by_template(t,
                               field_list=['playerID','nameLast','throws','bats','birthCountry'])

    print("find by template return:"+str(r))


def t3():
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, None)

    new_record= {
        "yearID": "1985",
        "teamID": "ATM",
        "lgID": "nl",
        "playerID": "BARKELE07",
        "salary": "f870000",
    }
    csv_tbl.insert(new_record)
    new_record["yearID"] = "1998"
    csv_tbl.insert(new_record)
    new_record["yearID"] = "1997"
    csv_tbl.insert(new_record)
    template = {"yearID": "1997"}
    new_values = {"yearID": "2011"}
    affected_num = csv_tbl.update_by_template(template=template, new_values=new_values)
    print(affected_num)

    # connect_info = {
    #     "directory": data_dir,
    #     "file_name": "Salaries.csv"
    # }
    # csv_tbl = CSVDataTable("Salaries", connect_info, None)
    #
    # new_record= {
    #     "yearID": "111",
    #     "teamID": "Tiritth",
    #     "lgID": "eee",
    #     "playerID": "eeee",
    #     "salary": "fffff",
    # }
    # sql, args = csv_tbl.insert(new_record)
    # print("SQL = ", sql, ", args = ", args)
def delete_by_key_test(key_fields=None):
    """
    :param data_table:
    :param key_fields:
    :return:
    """
    # test case
    connect_info = {
        "directory": data_dir,
        "file_name": "Salaries.csv"
    }
    csv_tbl = CSVDataTable("Salaries", connect_info, None)

    key_fields = ["KCA"]
    affected_num = csv_tbl.delete_by_key(key_fields)
    print(affected_num)

t_load()
# delete_by_key_test()
t_find_by_primary_key_and_template()
