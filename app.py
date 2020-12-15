#!/usr/bin/python
# vim: set fileencoding=<encoding name> :
import os, sys
from flask import Flask, render_template, request, make_response, jsonify, session, redirect, url_for, escape, flash
import array
from flaskext.mysql import MySQL
import os
from werkzeug.utils import secure_filename            #for upload purpuse


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
mysql = MySQL()

# app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mytest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = 'gtyfDGFRdfijfjiG783bbf7s8bhgmnxsrcv^&*#nfrBBF23778477#@@$%&^BFBFJ@@#%&FSDSUFUFfnf%^3839'

mysql.init_app(app)


@app.route('/kkkkk')
def index():
    return jsonify("payload")

@app.route('/home')
def ddd():
   return render_template('yy.html', page='aa')

@app.route('/imageupload')
def imgUpload():
   cursor = mysql.connect().cursor()
   cursor.execute('select * from uploadfile')
   dataa = cursor.fetchall()
   return render_template('imageupload.html', page='imageupload', allimg=dataa)

# Allowd file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/imageuploadaction', methods=['GET', 'POST'])
def imgUploadaction():
    if request.method == 'POST':
           userid = session['userID']
           file = request.files['file']
           if file.filename == '':
                  return redirect(request.url)
           if file and allowed_file(file.filename):
                  filename = secure_filename(file.filename)
                  file.save(os.path.join('static/uploads', filename))
                  
                  conn = mysql.connect()
                  cursor = conn.cursor()
                  
                  sql_insert_query = "INSERT INTO uploadfile (pic, up_u_id) VALUES (%s,%s)"
                  cursor.execute(sql_insert_query, (filename, userid))
                  conn.commit()
                  insert = conn.insert_id()
                  conn.close()
                  if insert is not None:
                     return redirect(url_for('fetchAllUser'))
           
   # return render_template('imageupload.html', page='imageupload')



@app.route('/normal')
def normal():
   return render_template('normal.html', page='normal')

@app.route('/test/<u_id>')
def testing(u_id):
   u_id = u_id
   cursor = mysql.connect().cursor()
   cursor.execute("select * from user where aid='"+ u_id +"'")
   data = cursor.fetchone()
   return render_template('tc.html', hh=u_id, values=data)

@app.route('/edituseraction', methods=['GET', 'POST'])
def editaction():
   if request.method == 'POST':
          name = request.form['name']
          email = request.form['email']
          userage = request.form['age']
          userid = request.form['uid']
          conn = mysql.connect()
          cursor = conn.cursor()
          sql_insert_query = "update user set name=%s, email=%s, age=%s where aid='"+ userid +"'"
          cursor.execute(sql_insert_query, (name, email, userage))
          conn.commit()
          insert = conn.insert_id()
          conn.close()
          if insert is not None:
                 return redirect(url_for('fetchAllUser'))
          else:
                 return redirect(url_for('fetchAllUser'))

# view login page
@app.route('/')
def lo():
   return render_template('login.html')

# all login functionality 
@app.route('/loginaction', methods=['GET', 'POST'])
def authenticate():
   if request.method == 'POST':
          email = request.form['email']
          password = request.form['password']
          cursor = mysql.connect().cursor()
         #  payload = []
         #  content = {}
          cursor.execute("SELECT * from user where email='" +
                       email + "' and password='" + password + "'")
          data = cursor.fetchone()
   #        content = {'id': data[0], 'name': data[1]}
   #        payload.append(content)
   #        content = {}
   # return jsonify(payload)
          if data is None:
               return redirect(url_for('lo'))
               # return render_template('register.html')
          else:
               # save user details into the session
               session['userID'] = data[0]
               session['userName'] = data[1]
               session['email'] = data[2]
               return redirect(url_for('ddd'))
               
               # return render_template('yy.html')
               # return redirect(url_for('testing', u_id=data[0]))
          
   # return jsonify('id': data[0], 'name': data[1])     
     
# view register page
@app.route('/register')
def loki():
   return render_template('register.html')

# create new user
@app.route('/registeraction', methods=['GET', 'POST'])
def regaction():
       if request.method == 'POST':
            fname = request.form['name']
            email = request.form['email']
            password = request.form['password']
            age = request.form['age']
            # return jsonify(password+"||"+age)
            conn = mysql.connect()
            cursor = conn.cursor()
            sql_insert_query = "INSERT INTO user (name, email, password, age) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql_insert_query, (fname, email, password, age))
            conn.commit()
            insert = conn.insert_id()
            conn.close()
            if insert is not None:
                   return redirect(url_for('ddd'))
            else:
                   return redirect(url_for('loki'))

# fetching example
@app.route('/alluser')
def fetchAllUser():
    cursor = mysql.connect().cursor()
    cursor.execute('select * from user')
    dataa = cursor.fetchall()
    return render_template("alluser.html", alluser=dataa, page='alluser')
 
 # delete user example
@app.route('/deleteUser/<u_id>', methods=['GET', 'POST'])
def deleteSingleUser(u_id):
    if request.method == 'POST':   
         u_id = u_id
         conn = mysql.connect()
         cursor = conn.cursor()
         cursor.execute("DELETE FROM user WHERE aid = '"+ u_id +"'")
         conn.commit()
         return redirect(url_for('fetchAllUser'))
 
# logout session destroy
@app.route('/logout')
def fus():
      session.clear()
      return redirect(url_for('lo'))
	
if __name__ == "__main__":
    app.run()