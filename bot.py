"""Telegram Bot - Расписание занятий преподователя"""
from datetime import datetime

import telegram
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

TOKEN = '<TELEGRAM BOT TOKEN>'
bot = telegram.Bot(token=TOKEN)

URL = '<WEB SERVER URI>'


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    room = db.Column(db.String(4), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    group = db.Column(db.String(10), nullable=False)
    topic = db.Column(db.String(100), nullable=False)

    def repr(self):
        return '<Lessons %r>' % self.subject


def all_lessons():
    """Список всех уроков преподователя

    По умолчанию выводим только первые 5
    """
    lessons_query = db.session.query(Lesson).order_by(Lesson.datetime).limit(5)
    html = ''
    for lesson_item in lessons_query:
        html += """
Предмет - {lesson.subject}
Дата и время - {lesson.datetime}
Место проведения - {lesson.address}
/lesson_{lesson.id}
        """.format(lesson=lesson_item)
    return html


def lesson(lesson_id):
    """Информация о занятии"""
    lesson_query = db.session.query(Lesson).get_or_404(lesson_id)
    html = """
Предмет - {lesson.subject}
Дата и время - {lesson.datetime}
Место проведения - {lesson.address}
Аудитория - {lesson.room}
Группа студентов - {lesson.group}
Тема занятия - {lesson.topic}

Чтобы увидеть все занятия нажмите /all
    """.format(lesson=lesson_query)
    return html


@app.route('/hook', methods=['POST', 'GET'])
def webhook_handler():
    if request.method == 'POST':
        try:
            response = ''
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            chat_id = update.message.chat.id
            text = update.message.text
            if text in ['/start', '/help']:
                response = """
Привет, я помощник в расписании!

Чтобы увидеть все занятия нажмите /all
                """
            elif text == '/all':
                response = all_lessons()
            elif '/lesson_' in text:
                command, lesson_id = text.split('_')
                response = lesson(lesson_id)
            bot.send_message(chat_id=chat_id, text=response)
        except Exception as err:
            pass

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    """Установка webhook"""
    result = bot.setWebhook('https://{url}/hook'.format(url=URL))
    if result is True:
        return 'webhook is set'
    return 'webhook is not set'


if __name__ == '__main__':
    app.run()
