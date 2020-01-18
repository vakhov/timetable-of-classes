
"""Заполнение таблицы данными о занятиях"""
from datetime import datetime, timedelta
from app import db, Lesson

now = datetime.utcnow()


def td(days=1, hours=0):
    return now + timedelta(days=days, hours=hours)


def init_lessons():
    db.create_all()
    lessons = [
        dict(subject='Физика', datetime=td(1), room='1C', address='Ленина 20а', group='ПР1',
             topic='Теория относительности'),
        dict(subject='Программирование', datetime=td(1, 2), room='2B', address='Ленина 20а', group='ПР1',
             topic='Представление алгоритмов'),
        dict(subject='Физика', datetime=td(2), room='3A', address='Ленина 20а', group='ПР2',
             topic='Траектория'),
        dict(subject='Программирование', datetime=td(2, 2), room='1C', address='Ленина 20а', group='ПР2',
             topic='Типы данных, операции и выражения'),
        dict(subject='Физика', datetime=td(3), room='11D', address='Ленина 20а', group='ПР3',
             topic='Средняя скорость'),
        dict(subject='Программирование', datetime=td(3, 2), room='6C', address='Ленина 20а', group='ПР3',
             topic='Отладка простейших задач'),
        dict(subject='Физика', datetime=td(4), room='1C', address='Ленина 20а', group='ПР4',
             topic='Сообщающиеся сосуды'),
        dict(subject='Программирование', datetime=td(4, 2), room='2C', address='Ленина 20а', group='ПР4',
             topic='Указатели и операции с адресами')
    ]
    for lesson in lessons:
        db.session.add(Lesson(**lesson))
    db.session.commit()


if __name__ == '__main__':
    init_lessons()
