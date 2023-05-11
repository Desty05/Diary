from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime


connection_string = 'mongodb://Desty05:Desty05@ac-innzuuj-shard-00-00.61f0sp5.mongodb.net:27017,ac-innzuuj-shard-00-01.61f0sp5.mongodb.net:27017,ac-innzuuj-shard-00-02.61f0sp5.mongodb.net:27017/?ssl=true&replicaSet=atlas-10mesw-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
   # sample_receive = request.args.get('sample_give')
   # print(sample_receive)
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
   # sample_receive = request.form['sample_give']
   # print(sample_receive)
    title_recieve = request.form.get('title_give')
    content_recieve = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d %H-%M-%S")

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_recieve,
        'content': content_recieve,
        'time': time,
    }

    db.diary.insert_one(doc)
    return jsonify({'msg': 'data was saved!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
