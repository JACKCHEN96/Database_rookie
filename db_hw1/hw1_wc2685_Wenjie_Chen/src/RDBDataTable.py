
from src.BaseDataTable import BaseDataTable
import pymysql
import pandas as pd


class RDBDataTable(BaseDataTable):

    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """
    _default_connect_info = {
        'host': 'localhost',
        'user': 'root',
        # 'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'HW1_0918',
        # 'db': 'ClassisModels',
        'port': 3306
    }

    def __init__(self, table_name, connect_info, key_columns):
        """

        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """

        self._table_name = table_name
        self._connect_info = connect_info
        self._key_columns = key_columns

        if connect_info is None:
            self._connect_info=RDBDataTable._default_connect_info
        self._connections = pymysql.connect(
            host=self._connect_info['host'],
            user=self._connect_info['user'],
            password=self._connect_info['password'],
            db=self._connect_info['db'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def __str__(self):
        result = "RDBDataTable: table_name = " + self._table_name
        result += "\nKey fields: " + str(self._key_columns)

        qf = "SELECT count(*) as count from " + self._table_name
        rf = self._run_q(qf, fetch=True, commit=True)
        result += "\nNo. of rows = " + str(rf[0]['count'])

        q= "Select * from" + self._table_name+" limit 5"

        df=pd.read_sql(q,self._connections)
        result+="\nFirst five rows:\n"
        result+=df.to_string()
        return result

    def _run_q(self,q,args=None,fields=None,fetch=True,connections=None,commit=True):
        if connections is None:
            connections=self._connections
        if fields:
            q=q.format(",".join(fields))

        cursor=connections.cursor()
        connt=cursor.execute(q,args)
        if fetch:
            r=cursor.fetchall()
        else:
            r=connt
        if commit:
            connections.commit()
        return r

    def _run_insert(self,table_name,column_list,values_list,connections=None,commit=None):
        try:
            q = "insert into " + table_name + " "
            if column_list is not None:
                q += "(" + ",".join(column_list) + ") "
            values = ["%s"] * len(values_list)
            values = " ( " + ",".join(values) + ") "
            values = "values" + values
            q += values
            self._run_q(q, args=values_list, fields=None, fetch=False, connections=connections, commit=commit)
        except Exception as e:
            print("Got exception = ", e)
            raise e

    def _get_primary_key(self):
        q="SHOW KEYS FROM "+self._table_name+" WHERE Key_name= 'PRIMARY'"
        r=self._run_q(q=q,args=None)
        k=[m["Column_name"] for m in r]
        return k

    def find_by_primary_key(self, key_fields, field_list=None):
        """

        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        :param field_list: A subset of the fields of the record to return.
        :return: None, or a dictionary containing the requested fields for the record identified
            by the key.
        """
        template = dict(zip(self._key_columns, key_fields))
        return self.find_by_template(template=template)

    def _template_to_where_clause(self, template):
        """
        :param template: One of those weird templates
        :return: WHERE clause corresponding to the template.
        """

        if template is None or template == {}:
            result = ("", None)
        else:
            args = []
            terms = []
            for k, v in template.items():
                terms.append(" " + k + "=%s ")
                args.append(v)
            w_clause = "AND".join(terms)
            w_clause = " WHERE " + w_clause
            result = (w_clause, args)
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
        try:
            he = self._template_to_where_clause(template)
            if field_list:
                q = "select {} from " + self._table_name + " " + he[0]
            else:
                q = "select * from " + self._table_name + " " + he[0]
            result = self._run_q(q, args=he[1], fields=field_list, commit=True, fetch=True)
            return result
        except Exception as e:
            print("RDBDataTable.find_by_template: Exception = ", e)
            raise e

    def delete_by_key(self, key_fields):
        """

        Deletes the record that matches the key.

        :param template: A template.
        :return: A count of the rows deleted.
        """

        return self.delete_by_template(dict(zip(self._key_columns,key_fields)))

    def delete_by_template(self, template):
        """

        :param template: Template to determine rows to delete.
        :return: Number of rows deleted.
        """
        he = self._template_to_where_clause(template)
        q = "delete from " + self._table_name + " " + he[0]
        result = self._run_q(q=q, args=he[1], fetch=False)
        return result

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of value for the key fields.
        :param new_values: A dict of field:value to set for updated row.
        :return: Number of rows updated.
        """
        return self.update_by_template(dict(zip(self._key_columns,key_fields)),new_values)

    def update_by_template(self, template, new_values):
        """

        :param template: Template for rows to match.
        :param new_values: New values to set for matching fields.
        :return: Number of rows updated.
        """
        sargs=[]
        ts=[]
        for k,v in new_values.items():
            ts.append(k+"=%s")
            sargs.append(v)
        ts=",".join(ts)
        he=self._template_to_where_clause(template)
        sargs.extend(he[1])
        q="update "+self._table_name+" set "+str(ts)+" "+he[0]
        result=self._run_q(q,sargs,fetch=False)
        return result

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records.
        :return: None
        """
        try:
            c_list=list(new_record.keys())
            v_list=list(new_record.values())
            self._run_insert(self._table_name,c_list,v_list)
        except Exception as e:
            print("insert: Exception e=",e)
            raise e

    def get_rows(self):
        return self.find_by_template()





