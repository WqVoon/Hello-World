from flask import Flask,request,render_template
import sqlite3
import string
from random import sample
app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if(request.form.get('content')):
        content=request.form['content']
        con=sqlite3.connect('database/data.db')
        cur=con.cursor()
        keyword=''.join(sample(string.ascii_letters+string.digits,10))
        total=cur.execute('select id from test;').fetchall()
        while(keyword in total):
            keyword=''.join(sample(string.ascii_letters+string.digits,10))
        cur.execute('insert into test values(?,?);',(keyword,content))
        con.commit()
        cur.close()
        con.close()
        return render_template('index.html',de=keyword)
    elif(request.form.get('keyword')):
        keyword=request.form['keyword'].strip()
        con=sqlite3.connect('database/data.db')
        cur=con.cursor()
        info=''
        temp=cur.execute('select * from test;').fetchall()
        for row in temp:
            if(row[0]==keyword):
                info=row[1]
                cur.execute('delete from test where id=="'+keyword+'";')
                break
        con.commit()
        cur.close()
        con.close()
        return render_template('index.html',content=info)
    else:return render_template('index.html')

if __name__ == "__main__":
    app.run()
