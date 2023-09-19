from Docx_operands import *
from Data_base import *
from Graph_operands import *
import os

class Report_operands:

    def __Add_image(self, file, link_):
        file.Add_pic(link_)

        if os.path.exists(link_):
            os.remove(link_)
    
    def __Delta_text(self, delta):  
        res = ""
        day_sec = 24 * 3600
        if delta > day_sec:
            res = res + str(delta // day_sec) + " days "
            delta = delta % day_sec

        hour_sec = 3600
        if delta > hour_sec:
            res = res + str(delta // hour_sec) + " hours "
            delta = delta % hour_sec

        min_sec = 60
        if delta > min_sec:
            res = res + str(delta // min_sec) + " minits "
            delta = delta % min_sec

        if delta > 0:
            res = res + str(delta) + " seconds"

        res = res.strip()
        return res

    def __Column_to_array(self, cols, data):
        for i in cols:
            buff = list()

            for i2 in range(0, len(data), 1):
                buff.append(data[i2][i])

            yield buff

    def __Insert_graph(self, data, file, label_, xlabel_, ylabel_, text_before_, int_x = True, 
                                    int_y = True, width_ = 12, heigth_ = 7):
         file.Add_text(text_before_, True, 'L', 14, bold_ = False)
         file.New_lines()

         graph = Graph(width_, heigth_, int_x, int_y)
         graph.Set_labels(label_, xlabel_, ylabel_)
         for pair in data:
            graph.Create_plot(pair[0], pair[1], alpha_ = 0.7, color_ = pair[2])
         
         self.__Add_image(file, graph.Save_figure())

    def __Create_periodic_table_rows(self, base, cols, table_name, oper_fields, oper_names, group_field, 
                                                                field_values, time_field, where_exps, start, finish, delta):

        statistic = base.Periodic_report(table_name, oper_fields, oper_names, group_field, field_values, time_field, where_exps, start, finish, delta)

        dates = statistic[0]
        data = statistic[2]

        rows = list()
        for i in range(0, len(dates), 1):
            row = list()

            row.append(i + 1)
            row.append(dates[i])
            for i2 in range(0, len(field_values), 1):
                for i3 in cols:
                    row.append(data[i2][i][i3])
           
            rows.append(row)

        return rows
                
    def __Title_text(self, file, report, start, finish, delta):
        file.Add_text(f"Отчет о {report}", True, 'C', 18, bold_ = True)
        file.New_lines()

        lines_ = [                 f"     Это отчет о {report}.", 
                  "Период: " + str(start) + " до "  + str(finish) + ".",
                  "Интервал деления: " + self.__Delta_text(delta)
        ]

        file.Add_many_lines(lines_, True, 'L', 14)

    def new_users(self, file, base, start, finish, delta):
      
        self.__Title_text(file, "новореганных пользователях", start, finish, delta)

        titles = ("Номер", "Период", "Клиенты", "Эксперты", "Сумма")
        rows = self.__Create_periodic_table_rows(base, [0], "Users", ["u_id"], ["COUNT"], "u_type", ["C", "E"], "u_regdate", [], start, finish, delta)

        for row in rows:
            row.append(row[2] + row[3])
        
        file.Add_text("    Таблица о новых пользователях с данными по периодам:", False, 'L', 14, bold_ = False)
        width_ = (1 , 2, 1 , 1, 1)
        file.Fill_table(titles, rows, width_, True, index_ = False)

        if len(rows) > 1:
            X = range(1, len(rows) + 1, 1)
            clients, experts, users_sum = self.__Column_to_array([2, 3, 4], rows)
        
            file.New_lines(2)
            self.__Insert_graph([[X, clients, "green"]], file, "Зарегестрированные клиенты", "Номер периода", "Их число",
                                "Новые клиенты в указанный период")        
            file.New_lines()

            self.__Insert_graph([[X, experts, "blue"]], file, "Зарегестрированные эксперты", "Номер периода",  "Их число",
                                "Новые эксперты в указанный период")      
            file.New_lines()

            self.__Insert_graph([[X, clients, "green"], [X, experts, "blue"], [X, users_sum, "orange"]], 
                                                file, "Общий график", "Номер периода",  "Количество",
                                                    "Общий график. Зеленая - клиенты, синяя - эксперты, оранжевый - сумма")   
            file.New_lines(3)                
        
    def orders(self, file, base, start, finish, delta, kind):

        field_values = []
        if kind == "all":
            field_values = ["S", "D", "F"]
        else:
            field_values.append(kind[0:1].upper())

        diction = {"S" :  "созданных заказах", "D" : "выполняемых заказах" , "F" : "завершенных заказах" }
            
        for field_value in field_values:
            
            self.__Title_text(file, diction[field_value], start, finish, delta)

            titles = ("Номер", "Период", "Число заказов", "Сумма заказов", "Средняя стоимость")
            rows = self.__Create_periodic_table_rows(base,  [0 , 1], "Orders", ["o_id", "o_price"], ["COUNT", "SUM"], 
                                            "o_status", [field_value], "o_startdate", [f"o_status = '{field_value}'"], start, 
                                            finish, delta)
       
            for row in rows:
                if row[2] != 0:
                    row.append(round(row[3] / row[2], 2))
                else:
                    row.append(" - ")
             
            file.Add_text("    Таблица о заказах с данными по периодам:", False, 'L', 14, bold_ = False)
            width_ = (2 , 4, 3 , 3, 3)
            file.Fill_table(titles, rows, width_, True, index_ = False)
            file.New_lines(2)

            file.Add_text(f"Графики о {diction[field_value]}", True, 'C', 14, bold_ = True)
            file.New_lines()

            X, num, cost, mid = self.__Column_to_array([0, 2, 3, 4], rows)

            for i in range(0, len(mid), 1):
                if mid[i] == " - ":
                    mid[i] = 0
         
            self.__Insert_graph([[X, num, "green"]], file, "Число заказов", "Номер периода",  "Количество",
                                                    "Число заказов:")   
            file.New_lines()
            
            self.__Insert_graph([[X, cost, "blue"]], file, "Сумма за период", "Номер периода",  "Сумма",
                                                    "Общая сумма заказов в период:", int_y = False)   
            file.New_lines()
            
            self.__Insert_graph([[X, mid, "orange"]], file, "Средняя стоимость за период", "Номер периода",  
                                "Средняя стоимость",  "Средняя величина оплаты за один заказ (0 - это отсутствие заказов)", int_y = False)   
            file.New_lines()
        
    def select_top(self, file, base, start, finish, delta, object_type, num, value, direct):

        if direct == "up":
             d_text_ = "Наибольшие."
        else:
             d_text_ = "Наименьшие."

        match object_type:
            case "experts" | "clients":

                if object_type == "experts":
                    text_ = "Рейтинговый отчет об экспертах, "
                else:
                    text_ = "Рейтинговый отчет о клиентах, "

                if   value == "compls":
                    text_ += "число жалоб. "

                    table_names = ["Users", "Orders", "Complaints"]
                    fields = ["u_id", "u_login", "u_name", "u_surname", "COUNT(c_id) AS comp_num"]
                    where_exps = ["o_id = c_order_id"]
                    order_fields = ["comp_num" , "u_id"]

                    if object_type == "experts":
                        where_exps.append("u_id = o_expert_id")
                    else:
                        where_exps.append("u_id = o_client_id")

                    time_field = "c_startdate"
                    group_fields = ["u_id", "u_name", "u_surname"]  

                    output = base.Top_report(table_names, fields, where_exps, time_field, group_fields, order_fields, num, direct, start, finish, delta)
                    
                    text_ += d_text_                 
                    file.Add_text(text_, True, 'C', 18, bold_ = True)
                    file.New_lines()

                    titles = ["Рейтинг", "Номер пользователя", "Логин", "Имя", "Фамилия", "Число жалоб"]
                    cols_width_ = [2, 3, 3, 3, 3, 3]

                    for i, one_date in enumerate(output[0]):
                        file.Add_text("Рейтинг пользователей по периоду: " + one_date, False)
                        file.Fill_table(titles, output[1][i], cols_width_, index_ = True)
                        file.New_lines()
                            
                else:
                    table_names = ["Users", "Orders"]
                    fields = ["u_id", "u_login", "u_name", "u_surname"]

                    match value:
                        case "ord_num":
                            text_ += "число заказов. "
                            order_fields = ["ord_num" , "u_id"]
                            fields.append("COUNT(o_id) AS ord_num")
                            titles = ["Рейтинг", "Номер пользователя", "Логин", "Имя", "Фамилия", "Число заказов"]
                            cols_width_ = [2, 3, 3, 3, 3, 3]
                        case "ord_cost":
                            text_ += "общая стоимость заказов. "
                            fields.append("SUM(o_price) AS ord_cost")
                            order_fields = ["ord_cost" , "u_id"]
                            titles = ["Рейтинг", "Номер пользователя", "Логин", "Имя", "Фамилия", "Сумма за заказы"]
                            cols_width_ = [2, 3, 3, 3, 3, 3]
                        case "ord_mid":
                            text_ += "средняя стоимость заказов. "
                            fields.append("ROUND(AVG(o_price), 2) AS ord_mid")
                            order_fields = ["ord_mid" , "u_id"]
                            titles = ["Рейтинг", "Номер пользователя", "Логин", "Имя", "Фамилия", "Средняя стоимость за период"]
                            cols_width_ = [2, 3, 3, 3, 3, 4]

                    where_exps = ["o_status = 'F'"]
                    if object_type == "experts":
                        where_exps.append("o_expert_id = u_id")
                    else:
                        where_exps.append("o_client_id = u_id")

                    time_field = "o_finishdate"
                    group_fields = ["u_id", "u_login", "u_name", "u_surname"]  
                    
                    output = base.Top_report(table_names, fields, where_exps, time_field, group_fields, order_fields, num, direct, start, finish, delta)
                    text_ += d_text_                 
                    file.Add_text(text_, True, 'C', 18, bold_ = True)
                    file.New_lines()
                   

                    for i, one_date in enumerate(output[0]):
                        file.Add_text("Рейтинг пользователей по периоду: " + one_date, False)
                        file.Fill_table(titles, output[1][i], cols_width_, index_ = True)
                        file.New_lines(2)

            case "orders":
                 table_names = ["Orders", "Subjects"]
                 fields = ["o_id", "o_price", "o_finishdate", "s_name", "o_client_id", "o_expert_id"]         
                 order_fields = ["o_price", "o_id"]
                      
                 where_exps = ["o_status = 'F'", "s_id = o_subject_id"]
                 time_field = "o_finishdate"
                 group_fields = []  
                    
                 output = base.Top_report(table_names, fields, where_exps, time_field, group_fields, order_fields, num, direct, start, finish, delta)
                              
                 file.Add_text("Рейтинговый отчет о заказах. " + d_text_, True, 'C', 18, bold_ = True)
                 file.New_lines()

                 titles = ["Рейтинг", "Номер заказа", "Cтоимость", "Дата окончания", "Предмет", "Номер клиента", "Номер эксперта"]
                 cols_width_ = [1, 1, 1,  2, 2, 1, 1]

                 for i, one_date in enumerate(output[0]):
                        file.Add_text("Рейтинг заказов за период: " +  one_date, False)
                        
                        file.Fill_table(titles, output[1][i], cols_width_, True, index_ = True)
                        file.New_lines()

    def complaints(self, file, base, start, finish, delta, kind) :
        if kind == "num":
            self.__Title_text(file, "числе жалоб", start, finish, delta)
            
            titles = ("Номер", "Период", "Созданы", "Закрыты")
            rows = base.Periodic_many_report("Complaints", ["COUNT(c_id)"], ["c_startdate", "c_finishdate"], [], start, finish, delta)
            
            file.Add_text("    Таблица о жалобах с данными по периодам:", False, 'L', 14, bold_ = False)
            width_ = (3 , 4, 3 , 3)
            file.Fill_table(titles, rows, width_, True, index_ = True)

            if len(rows) > 1:
                file.New_lines(2)

                X = range(1, len(rows) + 1, 1)
                opened, closed = self.__Column_to_array([1, 2], rows)

                self.__Insert_graph([[X, opened, "blue"]], file, "Число жалоб", "Номер периода",  "Количество",
                                    "Число созданных жалоб в периоды")      
                file.New_lines(2)

                self.__Insert_graph([[X, closed, "green"]], file, "Число жалоб", "Номер периода",  "Количество",
                                    "Число закрытых жалоб в периоды")      
                file.New_lines()

        if kind == "list":
             self.__Title_text(file, "созданных жалобах", start, finish, delta)
             table_names = [ "Orders", "Complaints"]
             fields = ["c_startdate", "c_id", "c_status", "o_id", "o_price" ]
             where_exps = ["o_id = c_order_id"]
             order_fields = ["c_startdate", "c_id"]
             
             time_field = "c_startdate"
             group_fields = []  
             num = 1000000
             direct = "down"
             output = base.Top_report(table_names, fields, where_exps, time_field, group_fields, order_fields, num, direct, start, finish, delta)

             titles = ["Рейтинг", "Дата создания", "Номер жалобы", "Статус", "Номер заказа", "Стоимость заказа"]
             cols_width_ = [1, 3, 2, 1, 2, 2]

             file.New_lines()
             for i, one_date in enumerate(output[0]):
                  file.Add_text("Список жалоб за период: " +  one_date, False, 'L', 14, bold_ = False)
               
                  file.Fill_table(titles, output[1][i], cols_width_, True, index_ = True)
                  file.New_lines()
             

            


        
