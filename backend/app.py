import os, sys, json, time
import pymysql
from flask import Flask, flash, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/getTagsNum', methods=['GET'])
def get_tags_num():
    conn = pymysql.connect(user='root', password='123456', database='tagger', charset='utf8')
    cursor = conn.cursor()
    query = 'select count(*) from tags'
    ret = cursor.execute(query)
    cursor.close()
    conn.close()
    return json.dumps({'code': 200, 'num': cursor.fetchone()[0]})


@app.route('/getTags', methods=['GET'])
def get_tags():
    num = request.args.get('num')
    conn = pymysql.connect(user='root', password='123456', database='tagger', charset='utf8')
    cursor = conn.cursor()
    query = "select tag from tags where id = %s" % num
    ret = cursor.execute(query)
    tag = cursor.fetchone()
    cursor.close()
    conn.close()
    return json.dumps({'code': 200, 'tag': tag})


@app.route('/saveTags', methods=['POST'])
def save_tags():
    post_json = request.get_data()
    data = json.loads(post_json)
    id = data['id']
    tag = data['tag']
    tag = json.dumps(tag)
    conn = pymysql.connect(user='root', password='123456', database='tagger', charset='utf8')
    cursor = conn.cursor()
    sql = "update tags set tag = %s where id = %s"
    try:
        cursor.execute(sql, (tag, id))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    cursor.close()
    conn.close()
    return json.dumps({'code': 200})


@app.route('/export', methods=['GET'])
def export():
    conn = pymysql.connect(user='root', password='123456', database='tagger', charset='utf8')
    cursor = conn.cursor()
    query = 'select * from tags'
    ret = cursor.execute(query)
    temp = cursor.fetchall()
    tags = ''
    for i in temp:
        tags += (i[1] + '\n')
    cursor.close()
    conn.close()
    return json.dumps({'code': 200, 'tag': tags})


if __name__ == '__main__':
    app.run(host='127.0.0.1')
