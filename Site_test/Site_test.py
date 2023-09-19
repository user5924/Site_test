from Data_base import *
from Console import *
import time

base_name = "Site_base.db"
base = Data_base(base_name)

base.Drop_tables()
base.Create_tables()

start = datetime.strptime( "2023-01-16", '%Y-%m-%d')
finish = datetime.strptime("2023-03-20", '%Y-%m-%d')
delta = 3600 * 24 * 30
base.Fill_base(40, 600, start , finish, 2500)
base.Show_tables("data.txt")      
 
Console(base)

print("Сессия завершена. Консоль закроется через несколько секунд.")
time.sleep(5)
