# DocAutofillApp
## Приложение для автоматического заполнения определённых документов (договоров) 
Разработанное приложение распознаёт фотографии (сканы) паспорта РФ и/или свидетельства о регистрации 
транспортного средства (СТС) и далее заполняет данными бланк договора формата word. Кроме этого, после процедур 
распознавания и автоматической вставки данных можно сразу проверить заполненный бланк договора и, 
в случае обнаружения неточностей, сделать корректировки. После чего можно внести договор в 
базу данных. Также предусмотрен отбор по параметрам (см.ниже) заполненных документов из БД.

### Описание работы приложения
У приложения есть примитивный графический интерфейс (GUI), реализованный с помощью python библиотеки Tkinter.
При нажатии на кнопку "Загрузить" открывается проводник, где пользователь может выбрать фотографию документа. 
После загрузки фото документа нужно подождать некоторое время, т.к. сразу происходит распознавание данных, 
после чего появляется зеленая галочка. Путём нажатия на кнопку "Заполнить договор" распознанные данные вносятся 
в договор, автоматически создается дата заполнения документа. 
Пример незаполненного бланка договора находится в папке проекта, файл GNZ.docx.
Заполнение договора доступно, даже если пользователь загрузил только один документ - паспорт или СТС.
Нажав на кнопку "Внести договор в БД", заполненный договор вносится в базу данных, в качестве СУБД выбрана SQLite.
По нажатию на кнопку "Отбор договоров" открывается новое окно, в данном окне 2 поля для ввода: "ФИО" и "Дата создания". 
Напротив каждого поля для ввода есть кнопка "Отбор", после нажатия которой производится поиск в БД документов по 
заданным параметрам. В случае обнаружения в БД искомых документов, файлы в формате word заносятся в 
папку selected_doc_db. 

### Запуск приложения
1. Установить необходимые зависимости
   ``` commandline
   pip install -r requirements.txt
   ```
2. Запустить файл main.py