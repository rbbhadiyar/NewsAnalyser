from flask import Flask, render_template, request,jsonify,send_from_directory
import psycopg2
import nltk
import json
from nltk import word_tokenize
from nltk import sent_tokenize
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from nltk.corpus import stopwords
nltk.download('all')
from werkzeug.urls import url_quote



app = Flask(__name__,static_folder='static')
# Making connection to database
conn = psycopg2.connect(database="news_native",user = 'postgres', password ='Ram@0916', host='localhost')
cur = conn.cursor()

#Making Connections with Different Webpages
@app.route("/",methods=['GET', 'POST'])
def portal():
    return render_template("Main page.html")
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/Main page')
def Main():
    return render_template('Main page.html')
@app.route('/index')
def index():
    return render_template('index.html')

# Extracting data and playing with it  
@app.route("/words",methods=['POST'])
def words():
    if request.method == 'POST':
        text_input = request.form['news-url']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        page = requests.get(text_input, headers=headers)
        project = BeautifulSoup(page.content,'html.parser')

        #Headings of Article
        heading = []
        head = project.find_all('h1')
        s_head1 = project.find_all('h2')
        for h1 in head:
            clean_text = re.sub(r'<.*?>', '', str(h1))
            heading.append(clean_text)
        for h2 in s_head1:
            clean_text = re.sub(r'<.*?>', '', str(h2))
            heading.append(clean_text)
        Remove = ["Also Read","Best Deals","Create free account and unlock exciting features like"]
        for i in Remove:
            if i in heading:
                heading.remove(i)
        heading = str(heading)

        #for paragraphs
        para = []
        paragraph= project.find_all('p')
        for p in paragraph:
            clean_text = re.sub(r'<.*?>', '', str(p))
            para.append(clean_text)
        para.pop(0)


        #for links
        link_list = []
        for links in project.find_all('a'):
            href = links.get('href')
            # Checking for valid links/href
            if href and urlparse(href).scheme:
                link_list.append(href)
        len_links = len(link_list)
        link_list = str(link_list)
        
        word = 0
        sent = 0
        Pos_dict = {}
        p=[]
        stop_words = set(stopwords.words('english'))
        for w in para:
            word_list = word_tokenize(w)
            word += len(word_list)
            sent += 1
            x = nltk.pos_tag(word_list, tagset='universal')
            for i in x:
                if i[1] not in Pos_dict:
                    Pos_dict[i[1]] = 1
                else:
                    Pos_dict[i[1]] += 1
            for w in word_list:
                if w not in stop_words:
                    p.append(w)
            p.append('\n')

        num_stop_words = word - len(p)
        para2 = ' '.join(p)

        with open('Pos_dict.json','w'):
        #using json.dump() to write the dictionary to file
            a = json.dumps(Pos_dict)

        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Data \
                (id serial primary key,
                Words INT,
                Sentences INT,
                POS_Tags Varchar,
                Paragraphs Varchar,
                links varchar,
                heading varchar,
                url varchar,
                Num_links INT,
                num_stop_words INT);''')
        
        email_id = users[-1][1]
        name = users[-1][0]
        cur.execute(
            '''INSERT INTO Data (Words ,Sentences,POS_Tags,Paragraphs,links,heading,url,numlinks,num_stop_words,name,email_id) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                (word,sent,a,para2,link_list,heading,text_input,len_links,num_stop_words,name,email_id))
        cur.execute('''SELECT Words ,Sentences,POS_Tags,Paragraphs,heading,numlinks,num_stop_words FROM Data ORDER BY ID DESC LIMIT 1''')
        data = cur.fetchall()
    
        cur.close()
        conn.commit()
        return render_template('result.html',data = data)
    
users = []
@app.route("/signin", methods=["GET","POST"])
def signin():
    if request.method == "POST":
        data = request.json  
        email = data.get('email')
        name = data.get('name')

        users.append([name,email])
        return jsonify({"message": "User signed in successfully"}), 200

#For Admin History
@app.route("/admin",methods = ["GET","POST"])
def admin():
    return render_template('admin.html')
@app.route("/check",methods = ["POST","GET"])
def check():
    pin = 'Rambhanwar@newsnative.admin'
    password = request.form["password"]
    if pin == password:
        cur = conn.cursor()
        cur.execute('''SELECT ID, URL,email_id FROM Data ''')
        urls = cur.fetchall()

        conn.commit()
        cur.close()

        return render_template("history.html",urls = urls)
    else:
        return render_template('admin.html')

   
@app.route("/view/<id>",methods = ["GET","POST"])
def view(id):
    cur = conn.cursor()
    cur.execute('''SELECT Words ,Sentences,POS_Tags,Paragraphs,heading, numlinks,num_stop_words FROM Data where id = %s ''',(id,))
    data = cur.fetchall()

    conn.commit()
    cur.close()

    return render_template('result.html',data = data)

#For User History
@app.route("/viewhistory",methods = ["GET","POST"])
def history():
    cur = conn.cursor()
    cur.execute('''SELECT ID, URL,email_id FROM Data where email_id=%s ''',(users[-1][1],))
    urls = cur.fetchall()

    conn.commit()
    cur.close()

    return render_template("user_history.html",urls = urls)

@app.route("/viewhistory2/<id>",methods = ["GET","POST"])
def viewhistory2(id):
    cur = conn.cursor()
    cur.execute('''SELECT Words ,Sentences,POS_Tags,Paragraphs,heading, numlinks,num_stop_words FROM Data where email_id = %s and id =%s''',(users[-1][1],id,))
    data = cur.fetchall()
    
    conn.commit()
    cur.close()

    return render_template('result.html',data = data)

    
if __name__=='__main__':
    app.run(debug=True, port=8000)
    conn.close()
