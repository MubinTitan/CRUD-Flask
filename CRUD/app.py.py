from logging import debug
from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="mycrud"
mysql=MySQL(app)

@app.route('/')
def fetch():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from details")
    data=cursor.fetchall()
    # print(data)
    return render_template("my.html",data=data)

@app.route('/',methods=['GET', 'POST'])
def insert():
    # check methods
    if(request.method=="POST"):
        # getting details from html
        details=request.form
        name=details['name']
        hobby=details['hobby']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO details(name, hobby) VALUES (%s, %s)", (name, hobby))
        mysql.connection.commit()
        cur.close()
        return "Success!"
  
    return render_template('my.html')


@app.route('/delete/<int:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM details WHERE id='%s'"%id)

    print(id)
    mysql.connection.commit()
    cur.close()
    return redirect('/')

@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    cur=mysql.connection.cursor()
    
    if(request.method=="POST"):
       
        # getting details from html
        detailss=request.form
        hobby=detailss['hobby']
        print(hobby)
        cur=mysql.connection.cursor()
        cur.execute("UPDATE `details` SET `hobby`=%s WHERE `id`=%s",(hobby, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template("new.html",id=id)
    
    
    
if __name__=='__main__':
    app.run(debug=True)

      