import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
import requests


CREATE_TABLE = (
    "CREATE TABLE IF NOT EXISTS questions ("
    "id integer PRIMARY KEY, "
    "question_text TEXT, "
    "answer_text TEXT, "
    "created_at TIMESTAMP);"
)

INSERT_QUESTION = (
    "INSERT INTO questions (id, question_text, answer_text, created_at) VALUES (%s, %s, %s, %s);"
)

CHECK_DUPLICATE = (
    "SELECT * FROM questions WHERE id = %s"
)

load_dotenv()

app = Flask(__name__)
connection = psycopg2.connect(
    host='db',
    port='5432',
    database=os.getenv('DB'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),

)

BASE_URL = 'https://jservice.io/api/random?count='


@app.post('/api/questions')
def random_question():
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname= 'public' AND tablename = 'questions')")
    if not cursor.fetchone():
        print('no table')
        cursor.execute(CREATE_TABLE)
    data = request.get_json()
    url = BASE_URL + str(data['questions_num'])
    response = get_questions(url)
    questions = list()

    for question in response:
        replacer = check_duplicate(question)
        if replacer == question:
            questions.append(question)
        else:
            questions.append(replacer)

    with connection:
        with connection.cursor() as cursor:
            for question in questions:
                cursor.execute(INSERT_QUESTION,
                               (question['id'],
                                question['question'],
                                question['answer'],
                                question['created_at']))
    return questions


@app.route('/hello')
def hello():
    return 'hello'


@app.route('/show')
def show():
    rows = list()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM questions LIMIT 10')
            for row in cursor:
                rows.append(row)
    return rows


def get_questions(url):
    response = requests.get(url).json()
    return response


def check_duplicate(question):
    unique = False
    while not unique:
        with connection.cursor() as cursor:
            cursor.execute(CHECK_DUPLICATE, (question['id'], ))
            if not cursor.fetchone():
                unique = True
            else:
                replacer = get_questions(BASE_URL + '1')
                return replacer[0]
    return question


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
