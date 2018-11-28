#用来获取英雄信息的爬虫程序（技能信息）
import pickle
import requests
from bs4 import BeautifulSoup as bs
import threading as td
import time
import sqlite3
f = open('hero.pickle','rb')#pickle中存放着解析后的英雄json数据，依靠这个获取ename值
hero = pickle.load(f)
f.close()
L=td.Lock()

heros=[]

def GET(sum):#利用多线程爬取英雄信息，并存放在heros列表里
    total=[]
    url = 'http://pvp.qq.com/web201605/herodetail/'+str(hero[sum]['ename'])+'.shtml'
    r = requests.get(url)
    soup = bs(r.content,'html.parser')
    skills = soup('div',{'class':'skill-show'})[0].contents
    L.acquire()
    for i in range((len(skills)-1)//2):#skills
        temp=[]
        temp.append(hero[sum]['cname'])
        for j in range(3):
            temp.append(skills[i*2+1].contents[1].contents[j].string)#skill_name,consume...
        temp.append(skills[i*2+1].contents[3].string)#describe
        temp.append(skills[i*2+1].contents[5].string)#tip
        total.append(temp)
    heros.append(total)
    print(sum,'has been fetch!')
    L.release()
            
try:
    con=sqlite3.connect('hero.db')
    cur=con.cursor()
    for sum in range(len(hero)):
        td.Thread(target=GET,args=(sum,)).start()
    while td.active_count()!=1:pass
    print('Hero fetch!')#英雄信息爬取完毕
    for sum in heros:
        for num in range(len(sum)):
            table='s'+str(num+1)
            cur.execute('insert into '+table+' values("'+str(sum[num][0])+'",'+'"'+str(sum[num][1])+'","'+str(sum[num][2])+'","'+str(sum[num][3])+'","'
            +str(sum[num][4])+'","'+str(sum[num][5])+'");')
        print(str(sum[0][0]),'has been added!')
    con.commit()#英雄信息储存完毕
    cur.close()
    con.close()
except Exception as er:
    print(er)
