# Site_test
Это программа создает отчеты в docx-файлах по данным из учебной БД.
Отчеты состоят из таблиц, графиков и рассчетов, которые создаются на основе имитатора базы данных сайта.
Структура проекта:
1. Concole.py - это код для работы консоли, куда вводят команды для создания отчета
2. Data_base.py - здесь находится класс, при помощи методов которого можно делать запросы к базе
3. Docx_operands.py - данный элемент позволяет создавать файлы, писать текст, вставлять таблицы и изображения.
4. Graph_operands.py - здесь функции и методы для создания графиков и их сохранения.
5. Reports.py - класс, создающий отчеты по указанным командам. Использует функционал трех вышеуказанных элементов.
6. Site_test.py - файл, который запускает базу данных и консоль.
7. Site_base.db - это файл, в котором расписано устройство БД (sqllite3).
