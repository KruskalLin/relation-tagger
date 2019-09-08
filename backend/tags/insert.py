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
    start_end = []
    temp = []
    for i in k['entityMentions']:
        if i['text'] not in texts:
            pos = text.find(i['text'])
            i['start'] = pos
            for j in start_end:
                if j[0] <= pos <= j[1]:
                    pos = text.find(i['text'], j[1])
                    i['start'] = pos
            if pos == -1:
                continue
            i['end'] = pos + len(i['text'])
            start_end.extend([(i['start'], i['end'])])
            start_end.sort(key=lambda x: x[1])
            texts.add(i['text'])
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