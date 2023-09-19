from Reports import *
from Docx_operands import *
from asyncio.windows_events import NULL
from datetime import datetime
import time

def Console(base):

    print(" Доброе время суток. Это консоль для создания отчетов по данным из БД.\n"
          "Для информации о командах введите 'info()'. Для завершения сеанса - 'end()'.")

    file = Docx_doc()
    reports = Report_operands()

    def Empty_comm(arg):

         if len(arg) == 0:
             return True
         i = 0
         while (arg[i] == ' ' or arg[i] == '\t') and i < len(arg):
            i += 1
         
         if i == len(arg) or arg[i] == ';':
            return True
         else:
            return False

    def Check_par_num(par_num, comm, right_num):
        if(par_num != right_num):
            print("Command '" + comm + "'  must have 3 parameters but " + str(par_nums) + " put in!")
            return False 
        else:
            return True
     
    def Convert_date(date):
        try:
            res = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                res = datetime.strptime(date, '%Y-%m-%d')
            except:
                return NULL

        return res

    def Convert_dates(start, finish, delta):
          
        st_date = Convert_date(start)
        if st_date == NULL:
           print("Wrong start date: '" + str(start), end = "")
           return NULL

        fin_date = Convert_date(finish)
        if fin_date == NULL:
           print("Wrong finish date: '" + str(finish), end = "")
           return NULL

        if st_date >= fin_date:
            print("Finish date must be > start date!")
            return NULL

        match delta:
            case "all":
                num = (fin_date - st_date).days * 24 * 3600 + (fin_date - st_date).seconds + 1
                return (st_date, fin_date, num)
            case "week":
                 return (st_date, fin_date, 3600 * 24 * 7)
            case "mouth":
                return (st_date, fin_date, 3600 * 24 * 30)
            case "year":
                return (st_date, fin_date, 3600 * 24 * 365)
   
        try:
                num = int(delta[2:len(delta)])   
        except:
            print("Expected int number in 'delta' from position 2!")
            return NULL

        match delta[0]:
            case 's':
                num *= 1
            case 'm':
                num *= 60
            case 'h':
                num *= (60 * 60)
            case 'd':
                num *= (60 * 60 * 24)
            case _:
                print("Expected someone of ['s', 'm', 'h', 'd'] at 'delta'!")
                return NULL
             
        return (st_date, fin_date, num)           

    def Comm_interp(comm,  file, base, reports):

         if Empty_comm(comm) == True:
             return 1

         comm = comm.strip()
         if comm.find("(") >= comm.find(")"):
            print(f"Command expected to be like that: <comm_name>(<args>)!")
            return -1

         text_end = comm.find("(")
         comm_text = comm[0 : text_end].strip()

         comm_params = list()
         past = text_end + 1
        
         i = past
         i2 = 0

         while True:
            i2 += 1

            if i2 == 40:
                return -1

            while comm[i] != ',' and comm[i] != ')':
                i += 1

            comm_params.append(comm[past: i].strip())
            if comm[i] == ')':
                break

            i += 1
            past = i
         
         if comm_text == "end":
            return 0
         
         if comm_text == "read":
             filename = comm_params[0].strip()
             filename.replace("\t", " ")
             filename =  "Commands\\" + filename 

             if os.path.exists(filename) == False:
                 print(f"File '{filename}' not exist!")
                 return -1
             
             f = open(filename, "r")

             file_data = f.read()
             file_data = file_data.replace("\n", "")
             file_data = file_data.replace("\r", "")

             comms = file_data.split(";")

             for command in comms:
                 command = command + ";"
                 ans = Comm_interp(command, file, base, reports)

                 if ans == -1:
                     print(f"Error in '{command}'!")
                 if ans == -1 or ans == 0:
                     return ans

         elif comm_text == "info":
             f = open("log\info.txt", "r", encoding='utf-8')
             print(f.read())
         else:
             res = Convert_dates(comm_params[0], comm_params[1], comm_params[2])
             if res == NULL:
                 print("' in command '" + comm_text + "'!")
                 return -1

             par_num = len(comm_params)
             match comm_text:

                case "new_users":
                    if Check_par_num(par_num, comm_text, 3) == False:
                        return -1

                    reports.new_users(file, base, res[0], res[1], res[2])

                case "orders":
                    if Check_par_num(par_num, comm_text, 4) == False:
                        return -1
                    if comm_params[3] in ["start", "finish", "deal", "all"]:
                        reports.orders(file, base, res[0], res[1], res[2], comm_params[3])
                    else:
                        print("Command 'orders' must have 'start', 'finish', 'deal', 'all' at 4 arg!")
                        return -1                                      

                case "select_top":
                    if Check_par_num(par_num, comm_text, 7) == False:
                        return -1
                
                    if comm_params[3] in ["experts", "clients"]:
                        if comm_params[5] not in ["compls", "ord_num", "ord_cost", "ord_mid"]:
                            print(f"Command 'select_top' has '{comm_params[3]}' at 4 arg but one of ['compls',  'ord_num', 'ord_cost', 'ord_mid']"
                                     " expected at 6!")
                            return -1  
                    elif comm_params[3] == "orders":
                         if comm_params[5] != "price":
                            print(f"Command 'select_top' has '{comm_params[3]}' at 4 arg but one of ['price']  expected at 6!")
                            return -1 
                    else:
                        print("Command 'select_top' must have one of ['experts', 'clients', 'orders'] at 4!")                          
                        return -1  

                    try:
                        num = int(comm_params[4])
                    except:
                        print("Command 'select_top' must have int number > 0 at 5!")                          
                        return -1

                    if num < 1:
                        print("Command 'select_top' must have int number > 0 at 5!")                          
                        return -1

                    if comm_params[6] not in ["up", "down"]:
                        print("Command 'select_top' must have 'up' or 'down' at 7!")                          
                        return -1
                
                    reports.select_top(file, base, res[0], res[1], res[2], comm_params[3], num, comm_params[5], comm_params[6])

                case "complaints":
                    if Check_par_num(par_num, comm_text, 4) == False:
                        return -1

                    if comm_params[3] in ["list", "num"]:
                        reports.complaints(file, base, res[0], res[1], res[2], comm_params[3])
                    else:
                        print("Command 'complaints' must have 'list' or 'num' at 4 arg!")
                        return -1
                
                case _:
                    print("Wrong command '" + comm_text + "'!")
                    return -1

             file.New_lines(1)
         
         i += 1
         if i == len(comm):
            return 0
         elif comm[i] != ';':
           print("Unexpected char '" + comm[i] + "' in command '" + comm + "' at " + str(i) + "!")
           return -1
       
         return 1

    while True:
        comm = input(">> ")
        ans = Comm_interp(comm, file, base, reports)

        if ans == -1:
            print(f"Error in '{comm}'!")
            time.sleep(2)
        if ans != 1:
            break
    
    file.Save_docx()



        
