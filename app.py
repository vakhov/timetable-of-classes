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
    lessons = db.session.query(Lesson).order_by(Lesson.datetime).limit(5)
    html = ''
    for lesson in lessons:
        html += """
        <p>
        Предмет - {l.subject}<br/>
        Дата и время - {l.datetime}<br/>
        Место проведения - {l.address}<br/>
        <a href="/lesson/{l.id}">Подробнее</a>
        </p>
        """.format(l=lesson)
    return html


@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    """Информация о занятии"""
    lesson = db.session.query(Lesson).get_or_404(lesson_id)
    html = """
    <p>
    Предмет - {l.subject}<br/>
    Дата и время - {l.datetime}<br/>
    Место проведения - {l.address}<br/>
    Аудитория - {l.room}<br/>
    Группа студентов - {l.group}<br/>
    Тема занятия - {l.topic}
    </p>
    """.format(l=lesson)
    return html


if __name__ == '__main__':
    app.run()
