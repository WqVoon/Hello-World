from flask import Flask,request,render_template
import sqlite3

app=Flask(__name__)

item_type={'1':'攻击','2':'法术','3':'防御','4':'移动','5':'打野','7':'辅助'}
hero_type={'1':'战士','2':'法师','3':'坦克','4':'刺客','5':'射手','6':'辅助','None':''}

@app.route('/',methods=['POST','GET'])
def index():
    try:
        if(request.method=='POST'):
            cont=request.form['content'].strip()
            if(request.form['de']=='1'):
                con=sqlite3.connect('database/hero.db')
                cur=con.cursor()
                re=[]
                hero=cur.execute('select * from type where name=="'+cont+'";').fetchone()
                if(not hero):
                        return render_template('index.html',de=1,no='没有找到该英雄，请重新输入')
                heros=[hero_type[hero[1]],hero_type[hero[2]]]
                for i in range(1,6):
                    table='s'+str(i)
                    result = cur.execute('select * from '+table+' where name=="'+cont+'";').fetchone()
                    temp={'name':result[1],'cd':result[2],'con':result[3],'des':result[4],'tip':result[5]}
                    if(temp['name']!='None'):
                        re.append(temp)
                cur.close()
                con.close()
                return render_template('index.html',de=1,hero_name=cont,hero_cls=heros,info=re)
            
            elif(request.form['de']=='2'):
                con=sqlite3.connect('database/item.db')
                cur=con.cursor()
                result = cur.execute('select * from test where name=="'+cont+'";').fetchone()
                if(not result):
                    return render_template('index.html',de=2,no='没有找到该装备，请重新输入')
                item=item_type[str(result[1])]
                re={'name':result[0],'pri':result[2],'total':result[3],'de1':result[4][3:-4].split('<br>'),'de2':result[5][3:-4].split('<br>') if result[5] else ''}
                cur.close()
                con.close()
                return render_template('index.html',de=2,item_cls=item,info=re)
            
        else:return render_template('index.html',de=1)
    except Exception as er:
        return(er)
app.run()
                
                
            
