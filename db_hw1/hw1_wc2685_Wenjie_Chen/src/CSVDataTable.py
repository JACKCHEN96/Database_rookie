
from src.BaseDataTable import BaseDataTable
import copy
import csv
import logging
import json
import os
import pandas as pd

pd.set_option("display.width", 256)
pd.set_option('display.max_columns', 20)


class Index():

    def __init__(self, index_name, index_columns, index_kind):
        self._data={
            "index_name":index_name,
            "index_columns":index_columns,
            "index_kind":index_kind
        }
        self._buckets = {}

    def compute_index_value(self, row):
        vs=[row[k] for k in self._data["index_columns"]]
        i_string = ("_").join(vs)
        return i_string

    def add_row(self, rid, row):
        i_value=self.compute_index_value(row)
        b=self._buckets.get(i_value)
        if b is None:
            b = []
        b.append(rid)
        self._buckets[i_value]=b

    def get_by_key(self,cols):
        k="_".join(cols)
        result=self._buckets.get(k)
        return result

    def get_key_columns(self):
        return self._data["index_columns"]


class CSVDataTable(BaseDataTable):
    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """

    _rows_to_print = 10
    _no_of_separators = 2

    def __init__(self, table_name, connect_info, key_columns, debug=True, load=True, rows=None):
        """

        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """

        self._data = {
            "table_name": table_name,
            "connect_info": connect_info,
            "key_columns": key_columns,
            "debug": debug
        }

        self._logger = logging.getLogger()

        self._logger.debug("CSVDataTable.__init__: data = " + json.dumps(self._data, indent=2))

        self._indexes={}

        if key_columns is not None and len(key_columns)>0:
            self._add_index("PRIMARY",key_columns)

        if rows is not None:
            self._rows = self._import_rows()
        else:
            self._rows = []
            self._load()

    def __str__(self):

        result = "CSVDataTable: config data = \n" + json.dumps(self._data, indent=2)

        no_rows = len(self._rows)
        if no_rows <= CSVDataTable._rows_to_print:
            rows_to_print = self._rows[0:no_rows]
        else:
            temp_r = int(CSVDataTable._rows_to_print / 2)
            rows_to_print = self._rows[0:temp_r]
            keys = self._rows[0].keys()

            for i in range(0,CSVDataTable._no_of_separators):
                tmp_row = {}
                for k in keys:
                    tmp_row[k] = "***"
                rows_to_print.append(tmp_row)

            rows_to_print.extend(self._rows[int(-1*temp_r)-1:-1])

        df = pd.DataFrame(rows_to_print)
        result += "\nSome Rows: = \n" + str(df)

        return result

    def _add_index(self,i_name,columns):
        self._indexes[i_name]=Index(i_name,columns,"PRIMARY")

    def _add_row(self, r):
        if self._rows is None:
            self._rows = []
        self._rows.append(r)

    def _load(self):

        dir_info = self._data["connect_info"].get("directory")
        file_n = self._data["connect_info"].get("file_name")
        full_name = os.path.join(dir_info, file_n)

        with open(full_name, "r") as txt_file:
            csv_d_rdr = csv.DictReader(txt_file)
            for r in csv_d_rdr:
                self._add_row(r)

        self._logger.debug("CSVDataTable._load: Loaded " + str(len(self._rows)) + " rows")

    def _import_rows(self,rows):
        raise NotImplementedError()

    def save(self):
        """
        Write the information back to a file.
        :return: None
        """

    def _find_by_index(self,i_name,key_fields):
        idx=self._indexes.get(i_name)
        b=idx.get_by_key(key_fields)
        return b

    def find_by_primary_key(self, key_fields, field_list=None):
        """

        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        :param field_list: A subset of the fields of the record to return.
        :return: None, or a dictionary containing the requested fields for the record identified
            by the key.
        """
        idx=self._indexes['PRIMARY']
        key_cols=idx.get_key_columns()
        tmp=dict(zip(key_cols,key_fields))
        result=self.find_by_template(template=tmp, field_list=field_list)
        if result is not None and len(result)>0:
            result=result[0]
        else:
            result=None

        return result

    def find_by_primary_key_fast(self,key_fields,field_list=None):
        """

        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        :param field_list: A subset of the fields of the record to return.
        :return: None, or a dictionary containing the requested fields for the record identified
            by the key.
        """
        result=self._find_by_index("PRIMARY",key_fields)
        if result:
            final_result = dict(self._rows[result[0]])
            final_result = CSVDataTable.__project(final_result, field_list)
            return final_result
        else:
            return None

    @staticmethod
    def matches_template(row, template):
        result = True
        if template is not None:
            for k, v in template.items():
                if v != row.get(k, None):
                    result = False
                    break

        return result

    def __project(row, field_list):
        result = {}

        if field_list is None:
            return row

        for f in field_list:
            result[f] = row[f]

        return result

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None):
        """

        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
        :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A list containing dictionaries. A dictionary is in the list representing each record
            that matches the template. The dictionary only contains the requested fields.
        """
        result=[]
        for r in self._rows:
            if CSVDataTable.matches_template(r,template):
                new_r=CSVDataTable.__project(r,field_list)
                result.append(new_r)
        return result

    def delete_by_key(self, key_fields):
        """

        Deletes the record that matches the key.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        #
        idx=self._indexes['PRIMARY']
        key_cols=idx.get_key_columns()
        tmp=dict(zip(key_cols, key_fields))

        rows_new = []
        num = 0

        for r in self._rows:
            if self.matches_template(r, tmp):
                del r
                num += 1
            else:
                rows_new.append(r)
        self._rows = rows_new
        return num

    def delete_by_template(self, template):
        """

        :param template: Template to determine rows to delete.
        :return: Number of rows deleted.
        """
        #
        rows_new = []
        num = 0
        for r in self._rows:
            if self.matches_template(r, template):
                del r
                num += 1
            else:
                rows_new.append(r)
        self._rows = rows_new
        return num

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of value for the key fields.
        :param new_values: A dict of field:value to set for updated row.
        :return: Number of rows updated.
        """
        idx=self._indexes['PRIMARY']
        key_cols=idx.get_key_columns()
        tmp=dict(zip(key_cols, key_fields))

        num = 0
        for r in self._rows:
            if self.matches_template(r, tmp):
                num += 1
                for k, v in new_values.items():
                    r[k] = v
        return num

    def update_by_template(self, template, new_values):
        """

        :param template: Template for rows to match.
        :param new_values: New values to set for matching fields.
        :return: Number of rows updated.
        """
        num = 0
        for row in self._rows:
            if self.matches_template(row, template):
                num += 1
                for k, v in new_values.items():
                    print(k,v)
                    print(row)
                    row[k] = v
        return num

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records.
        :return: None
        """

        if len(self._rows) == 0:
            self._rows.append(copy.deepcopy(new_record))
        else:
            # check new record
            # assert len(new_record) == len(self._rows[0]), "new record missed some required fields!"
            for k in new_record:
                if k not in self._rows[0]:
                    raise ValueError("new record has illegal field %s" % k)
            self._rows.append(copy.deepcopy(new_record))
        # self.save()

    # def save(self, fileName=None):
    #     """
    #     Write the information back to a file. We can also assign the output path is fileName is not None.
    #     :param fileName: output file name
    #     :return: None
    #     """
    #     if fileName is None:
    #         dir_info = self._data["connect_info"].get("directory")
    #         file_n = self._data["connect_info"].get("file_name")
    #         fileName = os.path.join(dir_info, file_n)
    #     delimiter = self._data["connect_info"].get("delimiter") if "delimiter" in self._data["connect_info"] else ","
    #     with open(fileName, "w") as out_file:
    #         csv_writer = csv.DictWriter(out_file, fieldnames=self._data["connect_info"].get("key_columns"),
    #                                     delimiter=delimiter)
    #         csv_writer.writeheader()
    #         csv_writer.writerows(self._rows)


    def get_rows(self):
        return self._rows





