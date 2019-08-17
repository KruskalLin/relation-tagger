import pymysql
import json
f = open('tags', 'r', encoding='utf8')
lines = f.readlines()
conn = pymysql.connect(user='root', password='123456', database='tagger', charset='utf8')
cursor = conn.cursor()
sql = 'insert into tags(tag) values(%s);'
lines_replica = []
for line in lines:
    k = json.loads(line)
    text = k['sentText']
    texts = set()
    temp = []
    for i in k['entityMentions']:
        if i['text'] not in texts:
            texts.add(i['text'])
            pos = text.find(i['text'])
            i['start'] = pos
            i['end'] = pos + len(i['text'])
            temp.extend([i])
    k['entityMentions'] = temp
    lines_replica.extend([json.dumps(k)])
try:
    # 执行sql语句
    cursor.executemany(sql, lines_replica)    #使用executemany做批量处理
    conn.commit()   #把修改提交到数据库
except Exception as e :
    print(e)
    conn.rollback()
cursor.close()
conn.close()