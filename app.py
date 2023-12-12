from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = "mySecretKey"
#app.permanent_session_lifetime = timedelta(days=1)


### DATABASE SETUP
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Co!!ege3oard2",
    "database": "community_shelf",
    }

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to MySQL")
except mysql.connector.Error as err:
    print(f"Error: {err}")

editing = -1

def getEdit():
    global editing
    x = editing
    return x

def setEdit(n):
    global editing
    editing = n
    return

def getUserId(username):
    curs = connection.cursor()
    args = (username, (0, "CHAR"))
    result = curs.callproc("GetUserIdByUsername", args)
    userid = result[1]
    curs.close()
    connection.commit()
    return userid

def checkUsernameValid(username):
    #check if username is in database of usernames
    #if it is valid, return the corresponding password
    # if not valid, return None
    
    username_check = "SELECT password FROM users WHERE name = %s"
    
    pcursor = connection.cursor(prepared=True)  #PREPARED STATEMENT

    pcursor.execute(username_check, (username,))
    
    pword = [pw for pw in pcursor]
    if len(pword) == 0:
        pcursor.close()
        return None
    else:
        pcursor.close()
        return pword[0][0]
 

@app.route('/')
def hello():
        return render_template("login.html")


@app.route('/login/', methods = ["POST", "GET"])
def login():
    if request.method == "POST": 
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = connection.cursor()
        print(username, password)

        password_ = checkUsernameValid(username) 
        #print(password_)
        if (password_ == None) or (password != password_):
            return render_template('login.html', l_error='Invalid username or password')
        
        #session.permament = True
        session["user"] = username
        return redirect(url_for("userhome"))
    else:
        if "user" in session:
            return redirect(url_for("userhome"))
        return render_template("login.html")


@app.route('/adduser', methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password2 =  request.form.get('password2')
        zipcode =  request.form.get('zipcode')
        email =  request.form.get('email')
        phone =  request.form.get('phone')
        address = request.form.get('address')

        if password1 == password2:
            args = (username, email, phone, address, zipcode, password)        
            
            results = cursor.callproc('CreateUser', args)
            #should check results for valid signup attempt
            
            #session.permament = True
            session["user"] = username
            cursor.close()
            connection.commit()
            return redirect(url_for("userhome"))

        return render_template('login.html', s_error='Invalid signup attempt')

    else:
        if "user" in session:
            return redirect(url_for("userhome"))
        return render_template("login.html")


@app.route('/userhome', methods=["POST", "GET"])
def userhome():
    if "user" in session:
        user = session["user"]
    pcursor = connection.cursor(prepared=True)
    sstmt = "select itemId, name, category, retail_cost, description from items join categories cat on items.category_id = cat.categoryId where ownerId = %s"
    pcursor.execute(sstmt, (getUserId(user),))
    
    itemss = []
    for iid, name, cat, price, descr in pcursor:
        itemss.append([iid, name, cat, price, descr])
   
    pcursor.close()
    connection.commit()
    return render_template("userhome.html", uname = user, item_list = itemss)

@app.route('/additem', methods=["POST"])
def additem():
    if request.method=="POST":    
        #get categories
        cursor = connection.cursor(prepared=True)
        getcats = cursor.execute("select category from categories")
        cats = [item for item in cursor]
        cursor.close()
        connection.commit()
        print(cats)
        return render_template("additem.html", categories = cats)
    else:
        if "user" in session:
            return redirect(url_for("userhome"))
        return render_template("login.html")

@app.route('/adding', methods=["POST"])
def adding():
    if request.method=="POST":
        name = request.form.get("nm") # getting words, name, category, price, description
        category = request.form.get("category")
        price = request.form.get("price")
        description = request.form.get("description")
        
        pcursor = connection.cursor(prepared=True)
        userid = getUserId(session["user"])

        print(category)
        #print("category", category[2:-3])
        
        print(getEdit())
        if getEdit() == -1:
            pcursor.execute("select categoryId from categories where category = %s", (category[2:-3],))
            
            result = pcursor.fetchone()

            #cats = [thing for thing in pcursor]
            cat = result[0]
            print("cats", cat)
            
            pcursor.close()
            pcursor = connection.cursor(prepared=True)
            
            addstmt = "INSERT INTO items (ownerId, name, category_id, retail_cost, description) VALUES (%s, %s, %s, %s, %s)"
            
            pcursor.execute(addstmt, (userid, name, cat, price, description))
    
        else:   
            #edit item with id currently_editing with data in form
            print("editing item ", getEdit())
            pcursor.execute("select categoryId from categories where category = %s", (category[2:-3],))
            
            result = pcursor.fetchone()

            #cats = [thing for thing in pcursor]
            cat = result[0]
            #print("cats", cat)
            
            editstmt = "UPDATE items SET ownerId = %s, name = %s, category_id = %s, retail_cost = %s, description = %s WHERE itemId = %s"
            pcursor.execute(editstmt, (userid, name, cat, price, description, getEdit()))

        setEdit(-1)

        pcursor.close()
        connection.commit()
        #reroute to userhome
        return redirect(url_for("userhome"))
    else:
        if "user" in session:
            return redirect(url_for("userhome"))
        return render_template("login.html")


@app.route('/deleting', methods=["POST"])
def deleteitem():
    if request.method=="POST":    
        itemid = request.form.get("deleteid")
        #deletion statement
        #TODO: write, executre statement to delete item with this id
        pcursor = connection.cursor(prepared=True)
        
        dstmt = "delete from items where itemId = %s"
        pcursor.execute(dstmt, (itemid,))
        pcursor.close()
        connection.commit()
        #return render_template("additem.html")
        return redirect(url_for("userhome"))
    else:
        if "user" in session:
            return redirect(url_for("userhome"))
        return render_template("login.html")


@app.route('/edititem', methods=["POST"])
def edititem():
    if request.method=="POST":
        itemid = request.form.get("editid")
        print("itemid", itemid)
        print(getEdit())
        setEdit(itemid)
        print("set", getEdit())

        cursor = connection.cursor()
        args = (itemid, (0, "CHAR"), (0, "CHAR"), (0, "CHAR"), (0, "CHAR"))
        result = cursor.callproc("GetItemDetails", args)
        pname = result[1]
        #pcat = result[2]
        pprice = result[3]
        pdescription = result[4]

        connection.commit()
        cursor.close()

        cursor = connection.cursor(prepared=True)
        getcats = cursor.execute("select category from categories")
        cats = [item for item in cursor]
        cursor.close()
        connection.commit()
        print(cats)

        return render_template("additem.html", name=pname, categories=cats, price=pprice, description=pdescription)
    else:
        if "user" in session:
            return redirect(url_for("userhome"))
        return render_template("login.html")


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    username=None
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)


