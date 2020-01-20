"""Расписание занятий преподователя"""
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    room = db.Column(db.String(4), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(10), nullable=False)
    topic = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Lessons %r>' % self.subject


@app.route('/lesson/all')
def all_lessons():
    """Список всех уроков преподователя

    По умолчанию выводим только первые 5
    """
    lessons_query = db.session.query(Lesson).order_by(Lesson.datetime).limit(5)
    html = ''
    for lesson_item in lessons_query:
        html += """
        <p>
        Предмет - {lesson.subject}<br/>
        Дата и время - {lesson.datetime}<br/>
        Место проведения - {lesson.address}<br/>
        <a href="/lesson/{lesson.id}">Подробнее</a>
        </p>
        """.format(lesson=lesson_item)
    return html


@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    """Информация о занятии"""
    lesson_query = db.session.query(Lesson).get_or_404(lesson_id)
    html = """
    <p>
    Предмет - {lesson.subject}<br/>
    Дата и время - {lesson.datetime}<br/>
    Место проведения - {lesson.address}<br/>
    Аудитория - {lesson.room}<br/>
    Группа студентов - {lesson.group}<br/>
    Тема занятия - {lesson.topic}
    </p>
    """.format(lesson=lesson_query)
    return html


if __name__ == '__main__':
    app.run()
