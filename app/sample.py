from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import json
import redis

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] +
                          '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get(
    "REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))

collection = db.games


@application.route('/')
def index():
    query = collection.find_one()

    body = '<h1>Alphabet Guessing Game</h1>'
    body += '<hr>'
    body += 'Please Choose A or B or C or D to add the character to the question.'
    body += '<br>'
    body += '<br>'

    if query != None:
        question_display = ' '.join(query['question'])
        body += f'<h2>Question: {question_display}</h2>'
        body += '<br>'
        body += '<br>'
        body += 'Choose:  <a href="/setA"><button>A</button></a>'
        body += '<a href="/setB"><button>B</button></a>'
        body += '<a href="/setC"><button>C</button></a>'
        body += '<a href="/setD"><button>D</button></a>'

        if query['count'] == 4:
            body += 'Choose:  <a href="/guessingA"><button>A</button></a>'
            body += '<a href="/guessingB"><button>B</button></a>'
            body += '<a href="/guessingC"><button>C</button></a>'
            body += '<a href="/guessingD"><button>D</button></a>'

            collection.update_one({}, {"$set": {"count": 0}})

            return start()
    else:
        body += f'<h2>Question: _ _ _ _</h2>'
        body += '<br>'
        body += '<br>'
        body += 'Choose:  <a href="/setA"><button>A</button></a>'
        body += '<a href="/setB"><button>B</button></a>'
        body += '<a href="/setC"><button>C</button></a>'
        body += '<a href="/setD"><button>D</button></a>'

        data = {
            "question": ["_", "_", "_", "_"],
            "guessing": ["*", "*", "*", "*"],
            "answer": [],
            "fail": 0,
            "count": 0
        }

        collection.insert_one(data)

    return body


@application.route('/start')
def start():
    query = collection.find_one()
    question = query['question']
    answer = query['answer']

    if answer != question:
        body = '<h1>Alphabet Guessing Game</h1>'
        body += '<hr>'
        body += "Please Choose A or B or C or D to guess the character."
        body += '<br>'
        body += '<br>'
        ans = ' '.join(query['answer'])
        body += f'<h2>Answer: {ans}</h2>'
        body += '<br>'
        body += '<br>'
        guess = ' '.join(query['guessing'])
        body += f'Character(s) remaining: {guess}'
        body += '<br>'
        body += '<br>'
        body += f'<tt style="color:red;">Fail(s): {str(query["fail"])}</tt>'
        body += '<br>'
        body += '<br>'
        body += '<br>'
        body += 'Choose:  <a href="/guessingA"><button>A</button></a>'
        body += '<a href="/guessingB"><button>B</button></a>'
        body += '<a href="/guessingC"><button>C</button></a>'
        body += '<a href="/guessingD"><button>D</button></a>'

        return body

    if answer == question:
        return stop()


def stop():
    query = collection.find_one()
    num_fails = query["fail"]

    body = '<h1>Alphabet Guessing Game</h1>'
    body += '<hr>'
    body += '<br>'
    body += '<br>'
    body += '<h2 style="color:green;">You win!!!</h2>'
    body += '<br>'
    body += f'<b style="color:red;">You guessed it {num_fails} wrong time(s).</b>'
    body += '<br>'
    body += '<br>'
    body += '<br>'
    body += '<a href="/restart"><button>Play Again?</button></a>'

    return body


@application.route('/restart')
def restart():
    data = {
        "question": ["_", "_", "_", "_"],
        "guessing": ["*", "*", "*", "*"],
        "answer": [],
        "fail": 0,
        "count": 0
    }

    collection.update_one({}, {"$set": data})

    return index()


@application.route('/setA')
def set_question_A():
    set_question('A')
    return index()


@application.route('/setB')
def set_question_B():
    set_question('B')
    return index()


@application.route('/setC')
def set_question_C():
    set_question('C')
    return index()


@application.route('/setD')
def set_question_D():
    set_question('D')
    return index()


@application.route('/guessingA')
def guessing_A():
    guessing('A')
    return start()


@application.route('/guessingB')
def guessing_B():
    guessing('B')
    return start()


@application.route('/guessingC')
def guessing_C():
    guessing('C')
    return start()


@application.route('/guessingD')
def guessing_D():
    guessing('D')
    return start()


def set_question(alphabet):
    query = collection.find_one()
    pos = query["count"]

    new_data = {"$set": {f"question.{pos}": f'{alphabet}', "count": pos + 1}}

    collection.update_one({}, new_data)


def guessing(alphabet):
    query = collection.find_one()
    question = query['question']
    pos = query["count"]
    num_fails = query["fail"]

    if f'{alphabet}' != question[pos]:
        collection.update_one({}, {"$set": {"fail": num_fails + 1}})

    if f'{alphabet}' == question[pos]:
        new_data = {"$set": {f"guessing.{pos}": "X",
                             f"answer.{pos}": f'{alphabet}', "count": pos + 1}}

        collection.update_one({}, new_data)


@application.route('/sample')
def sample():
    doc = db.test.find_one()
    # return jsonify(doc)
    body = '<div style="text-align:center;">'
    body += '<h1>Python</h1>'
    body += '<p>'
    body += '<a target="_blank" href="https://flask.palletsprojects.com/en/1.1.x/quickstart/">Flask v1.1.x Quickstart</a>'
    body += ' | '
    body += '<a target="_blank" href="https://pymongo.readthedocs.io/en/stable/tutorial.html">PyMongo v3.11.2 Tutorial</a>'
    body += ' | '
    body += '<a target="_blank" href="https://github.com/andymccurdy/redis-py">redis-py v3.5.3 Git</a>'
    body += '</p>'
    body += '</div>'
    body += '<h1>MongoDB</h1>'
    body += '<pre>'
    body += json.dumps(doc, indent=4)
    body += '</pre>'
    res = redisClient.set('Hello', 'World')
    if res == True:
        # Display MongoDB & Redis message.
        body += '<h1>Redis</h1>'
        body += 'Get Hello => '+redisClient.get('Hello').decode("utf-8")
    return body


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT,
                    debug=ENVIRONMENT_DEBUG)
