from asyncio.windows_events import NULL
import sqlite3
from datetime import *
from random import * 
from string import *
from math import exp

class Data_base():

    def Timedelta_sec(self, delta):
        res = delta.seconds + 3600 * 24 * delta.days
        return res

    def __init__(self, base_name):
        self.con = sqlite3.connect(base_name)
        self.curs = self.con.cursor()

    def Get_cursor(self):
        return self.curs

    def Create_tables(self):
        curs = self.curs

        buff = '''
                        CREATE TABLE Users 
                        (
                                u_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                                u_name VARCHAR(50), 
                                u_surname VARCHAR(50), 
                                u_login VARCHAR(50),
                                u_regdate VARCHAR(40),
                                u_rating FLOAT,
                                u_ratnum FLOAT,
                                u_type CHAR,
                                u_info TEXT
                         );

                         CREATE TABLE Orders
                        (
                                o_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                o_client_id INTEGER,
                                o_expert_id INTEGER,
                                o_subject_id INTEGER,  
                                o_price FLOAT, 
                                o_startdate VARCHAR(40),
                                o_dealdate VARCHAR(40),
                                o_finishdate VARCHAR(40),
                                o_status CHAR,
                                o_info TEXT
                         );
                 
                         CREATE TABLE  Complaints
                        (
                                c_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                c_order_id INTEGER, 
                                c_startdate VARCHAR(40),
                                c_finishdate VARCHAR(40),
                                c_status CHAR,
                                c_info TEXT
                         );

                          CREATE TABLE  Subjects
                        (
                                s_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                s_name VARCHAR (400)
                         );
        '''
        quary_array = buff.split(";")
        for quary in quary_array:
            curs.execute(quary)

    def Show_tables(self, outfile):
        curs =  self.curs

        f = open(outfile, "w")
        curs.execute("SELECT name FROM sqlite_master WHERE type = 'table';") 
        res = curs.fetchall()

        for tables in res:
            for table in tables:
                if table != "sqlite_sequence":
                    quary = "SELECT * FROM " + table + ";"
                    curs.execute(quary)
                    rows = curs.fetchall()

                    f.write(str(table) + " (")

                    quary = "PRAGMA table_info('" + str(table) + "');"
                    curs.execute(quary)
                    table_info = curs.fetchall()

                    leng = len(table_info) - 1
                    i = 0
                    while i < leng:
                        f.write(str(table_info[i][1]) + "  " + str(table_info[i][2]) + ", ")
                        i += 1

                    f.write(str(table_info[i][1]) + "  " + str(table_info[i][2]))
                    f.write("):\n")
   
                    for row in rows:
                        f.write("\t")

                        for elem in row:
                            f.write(str(elem) + "\t")
                        f.write("\n")

                    f.write("\n")
    
        f.close()
 
    def Drop_tables(self):
        
        curs =  self.curs
    
        curs.execute("SELECT name FROM sqlite_master WHERE type = 'table';") 
        res = curs.fetchall()
        quaryes = list()

        for tables in res:
            for table in tables:
                if table != "sqlite_sequence":
                    buff = "DROP TABLE " + table;
                    quaryes.append(buff)

        for quary in quaryes:
                curs.execute(quary)
      
    def Fill_base(self, exp_num, cl_num, min_date, max_date, ord_num):
    
        curs =  self.curs
        def get_random_date(start, end):
            delta_sec = self.Timedelta_sec(end - start)
            return start + timedelta(seconds = randint(0, delta_sec))

        def Rand_str(leng): 
            liters = 'abcdefghijklmnopqrstuvwxyz'
            rand_string = ''.join(choice(liters) for i in range(leng))
            return rand_string

        user_num = exp_num + cl_num
        diff = (max_date - min_date).seconds +  (max_date - min_date).days * 24 * 3600

        for i in range(user_num):
             u_name = Rand_str(5 + round(random() * 5)) 
             u_surname = Rand_str(8 + round(random() * 5)) 
             u_login =  Rand_str(10 + round(random() * 10))

             u_regdate = min_date + timedelta(seconds=round(diff * random()))
             u_rating = 1 + random() * 4
             u_ratnum = 1 + round(random() * 10)

             if i < exp_num:
                u_type  = 'E'
             else:
                u_type = 'C'

             u_info =  Rand_str(40 + round(random() * 100)) 

             quary = f'''
                     INSERT INTO Users
                              (
                                    u_name, 
                                    u_surname, 
                                    u_login,
                                    u_regdate,
                                    u_rating,
                                    u_ratnum,
                                    u_type,
                                    u_info
                             ) 
                    VALUES
                            (
                                    '{u_name}', 
                                    '{u_surname}', 
                                    '{u_login}',
                                    '{u_regdate}',
                                    '{u_rating}',
                                    '{u_ratnum}',
                                    '{u_type}',
                                    '{u_info}'
                            );
              '''
             curs.execute(quary)

        for i in range(ord_num):
            
            o_client_id = randint(cl_num + 1, user_num)
            o_expert_id = NULL
            o_subject_id = randint(1, 5)
            o_price = randint(100, 3000) 
            o_startdate = min_date + timedelta(seconds=round(diff * random()))
            o_dealdate = NULL
            o_finishdate = NULL

            date_diff = self.Timedelta_sec(datetime.now() -  o_startdate)
            deal_var = exp(-self.Timedelta_sec(timedelta(days = 10)) /  date_diff)

            if random() < deal_var:
                 o_expert_id = randint(1, exp_num)

                 max_date = o_startdate + timedelta(days = 15)
                 if max_date > datetime.now():
                    max_date = datetime.now()
                 o_dealdate = get_random_date(o_startdate, max_date)

                 rand_sec = int(random() * 10 * 24 * 3600)
                 o_finishdate = o_dealdate  + timedelta(seconds = rand_sec)

                 if o_finishdate > datetime.now():
                     o_finishdate = NULL
                     o_status = 'D'
                 else:
                     o_status = 'F'
            else:
                o_status = 'S'

            o_info = Rand_str(40 + round(random() * 100)) 
            quary = f'''
                    INSERT INTO Orders
                              (
                                    o_client_id,
                                    o_expert_id,
                                    o_subject_id,  
                                    o_price, 
                                    o_startdate,
                                    o_dealdate,
                                    o_finishdate,
                                    o_status,
                                    o_info
                             ) 
                    VALUES
                            (
                                    '{o_client_id}',
                                    '{o_expert_id}',
                                    '{o_subject_id}',  
                                    '{o_price}', 
                                    '{o_startdate}',
                                    '{o_dealdate}',
                                    '{o_finishdate}',
                                    '{o_status}',
                                    '{o_info}'
                             );
              '''
            curs.execute(quary)
    
        subjects = list()
        subjects.append("math")
        subjects.append("inform")
        subjects.append("english")
        subjects.append("chimistry")
        subjects.append("history")

        for sub in subjects:

            s_name = sub
            quary = f'''
                    INSERT INTO Subjects
                              (
                                    s_name
                             ) 
                    VALUES
                            (
                                    '{s_name}'
                             );
              '''
            curs.execute(quary)

        for i in range(int(ord_num / 20)):

            c_order_id = randint(1, ord_num) 
            c_startdate = min_date + timedelta(seconds=round(diff * random()))

            c_finishdate = c_startdate + timedelta(seconds=round(24 * 10 * 3600 * random()))
            if c_finishdate > datetime.now():
                c_finishdate = NULL
                c_status = 'S'
            else:
                c_status = 'F'

            c_info =  Rand_str(100 + round(random() * 200))

            quary = f'''
                    INSERT INTO Complaints
                        (
                                c_order_id, 
                                c_startdate,
                                c_finishdate,
                                c_status,
                                c_info
                         )
                    VALUES
                            (
                                    '{c_order_id}', 
                                    '{c_startdate}',
                                    '{c_finishdate}',
                                    '{c_status}',
                                    '{c_info}'
                             );
              '''
            curs.execute(quary)

    def __Dates_table(self, start, finish, delta):
        dates = list()
        curr_date = start
        while(curr_date < finish):
            next_date = curr_date + timedelta(seconds=delta)
            if(next_date > finish):
                next_date = finish

            buff = str(curr_date) + " - " + str(next_date)
            dates.append(buff)

            curr_date = next_date

        return dates

    def Periodic_report(self, table_name, oper_fields, oper_names, group_field, field_values, time_field, where_exps, start, finish, delta):
        
        quary = '''SELECT  \n'''
        for i in range(0, len(oper_names), 1):
             quary += f"{oper_names[i]}({oper_fields[i]}),\n"

        quary += f"{group_field},\n"
        quary += f'''
(
    cast( 
            (
                    JULIANDAY({time_field}) - JULIANDAY('{str(start)}')
                ) * 3600 * 24 / {delta}   AS INTEGER
            )
) AS per_number\n
     '''
        quary += f"FROM {table_name}"
        quary += f" WHERE {time_field} >= '{str(start)}' AND {time_field} < '{str(finish)}'\n" 
        for where_exp in where_exps:
            quary += ("AND " + where_exp + "\n")
        quary += "GROUP BY\n"
        quary += f"\t{group_field},\n"
        quary += f"\tper_number\n"
      
        self.curs.execute(quary)
        rows = self.curs.fetchall()

        dates = self.__Dates_table(start, finish, delta)

        data = list()
        dictionary = {}
        for i, value in enumerate(field_values):
            dictionary[value]  = i

            buff = list()
            for i2 in range(0, len(dates), 1):
                row = list()

                for i3 in range(0, len(oper_fields), 1):
                    row.append(0)
                buff.append(row)       

            data.append(buff)

        inter = len(oper_fields)
        for row in rows:
            ind = dictionary[row[inter]]

            for i in range(0, len(oper_fields), 1):
                data[ind][row[inter + 1]][i] = row[i]
        
        return [dates, field_values, data]

    def Top_report(self, table_names, fields, where_exps, time_field, group_fields, order_fields, num, direct, start, finish, delta):

        dates = self.__Dates_table(start, finish, delta)

        data = list()
        for pair in dates:
            inters = pair.split(" - ")
                
            quary = "SELECT\n\t"
        
            quary += ",\n\t".join(fields)

            quary += "\nFROM\n\t"
            quary += ",\n\t".join(table_names)

            quary += "\nWHERE\n\t"
            quary += " AND \n\t".join(where_exps)
            if len(where_exps) > 0:
                quary += " AND"

            quary += (f"\n\t{time_field} >= '{str(inters[0])}' AND {time_field} < '{str(inters[1])}'\n")

            if len(group_fields) != 0:
                quary += "GROUP BY \n\t"
                quary += ",\n\t".join(group_fields)

            if direct == "up":
                sql_order =  "DESC"
            else:
                sql_order  = "ASC"

            quary += "\nORDER BY\n\t"
            quary += f" {sql_order},\n\t".join(order_fields)
            quary += f" {sql_order}"

            quary += f"\nLIMIT {num}"

            #print(quary)

            self.curs.execute(quary)
            buff = self.curs.fetchall()
            data.append(buff)

        return [dates, data]

    def Periodic_many_report(self, table_name, field_names, time_fields, group_fields, start, finish, delta):
        dates = self.__Dates_table(start, finish, delta)

        rows = list()
        leng = len(field_names) * len(time_fields)
        for per in dates:
            row = list()
            row.append(per)
            for i in range(0, leng, 1):
                row.append(0)

            rows.append(row)

        count = 0
        field_num = len(field_names)

        for time_field in time_fields:
            quary = "SELECT \n\t"
            quary += f'''(CAST( 
            (
                    JULIANDAY({time_field}) - JULIANDAY('{str(start)}')
                ) * 3600 * 24 / {delta}   AS INTEGER
            )
) AS per_number,\n\t'''
            quary += ",\n\t".join(field_names)
            quary += f"\nFROM\n\t{table_name}\n"
            quary += "WHERE\n\t"
            quary += f"{time_field} >= '{start}' AND {time_field} < '{finish}'\n"

            quary += f"GROUP BY \n\tper_number"
            if len(group_fields) > 0:
                quary += ",\n\t"
                quary += ", \n\t".join(group_fields)
            #print(quary)
            self.curs.execute(quary)
            table = self.curs.fetchall()

            for row in table:
                ind = row[0]

                for i in range(1, field_num + 1, 1):
                    rows[ind][count + i] += row[i]

            count += field_num

        return rows


            

        



        









            

       









                        
                      
                             











   








