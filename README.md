`Учебный проект расписание для преподавателя`

Установка зависимостей:

 - pip install -r requirements.txt
 
Инициализация базы:

 - python init_lessons.py
 
Запуск проекта

 -  python app.py
 
Запуск telegram бота

 - python bot.py

---
Файлы проекта
- `app.py - Проект Расписание в виде web сервиса`
- `bot.py - Проект Расписание в виде telegram бота`
- `database.db - Подготовленная база, с примерами расписаний`
- `init_lessons.py - Инициализация db`
- `requirements.txt - Зависимости проекта.`



http://127.0.0.1:5000/lesson/all - Получение первых пяти уроков

http://127.0.0.1:5000/lesson/{id} - Детальная информация
