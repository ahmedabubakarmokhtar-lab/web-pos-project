<<<<<<< HEAD
from flask import Flask, render_template_string, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

conn = sqlite3.connect("geedi_web.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE,
price REAL,
quantity INTEGER)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
product TEXT,
price REAL,
qty INTEGER,
total REAL,
date TEXT)
""")
conn.commit()

HTML="""
<!DOCTYPE html>
<html>
<head>
<title>Geedi Supermarket POS</title>
<style>
body {font-family: Arial; background:#f4f6f9;}
header {background:#0d6efd;color:white;padding:15px;font-size:24px;}
.container{display:flex;padding:20px;}
table{border-collapse:collapse;width:100%;}
th,td{border:1px solid #ddd;padding:8px;text-align:center;}
th{background:#0d6efd;color:white;}
button{padding:8px 12px;background:#198754;color:white;border:none;cursor:pointer;}
input{padding:5px;margin:5px;}
</style>
</head>
<body>
<header>GEEDI SUPERMARKET POS</header>

<div style="padding:20px;">
<h3>Add Product</h3>
<form method="POST" action="/add">
<input name="name" placeholder="Name" required>
<input name="price" placeholder="Price" required>
<input name="qty" placeholder="Qty" required>
<button>Add</button>
</form>

<h3>Products</h3>
<table>
<tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th><th>Sell</th></tr>
{% for p in products %}
<tr>
<td>{{p[0]}}</td>
<td>{{p[1]}}</td>
<td>${{p[2]}}</td>
<td>{{p[3]}}</td>
<td><a href="/sell/{{p[0]}}"><button>Sell</button></a></td>
</tr>
{% endfor %}
</table>

<h3>Total Revenue: ${{revenue}}</h3>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    cursor.execute("SELECT * FROM products")
    products=cursor.fetchall()

    cursor.execute("SELECT SUM(total) FROM sales")
    revenue=cursor.fetchone()[0]
    if revenue is None: revenue=0

    return render_template_string(HTML,products=products,revenue=revenue)

@app.route("/add",methods=["POST"])
def add():
    name=request.form["name"]
    price=float(request.form["price"])
    qty=int(request.form["qty"])

    cursor.execute("SELECT id,quantity FROM products WHERE name=?",(name,))
    existing=cursor.fetchone()

    if existing:
        cursor.execute("UPDATE products SET quantity=? WHERE id=?",
                       (existing[1]+qty,existing[0]))
    else:
        cursor.execute("INSERT INTO products(name,price,quantity) VALUES(?,?,?)",
                       (name,price,qty))
    conn.commit()
    return redirect("/")

@app.route("/sell/<int:id>")
def sell(id):
    cursor.execute("SELECT name,price,quantity FROM products WHERE id=?",(id,))
    p=cursor.fetchone()
    if p and p[2]>0:
        cursor.execute("UPDATE products SET quantity=quantity-1 WHERE id=?",(id,))
        cursor.execute("INSERT INTO sales VALUES(?,?,?,?,?)",
                       (p[0],p[1],1,p[1],
                        datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
    return redirect("/")

=======
from flask import Flask, render_template_string, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

conn = sqlite3.connect("geedi_web.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE,
price REAL,
quantity INTEGER)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
product TEXT,
price REAL,
qty INTEGER,
total REAL,
date TEXT)
""")
conn.commit()

HTML="""
<!DOCTYPE html>
<html>
<head>
<title>Geedi Supermarket POS</title>
<style>
body {font-family: Arial; background:#f4f6f9;}
header {background:#0d6efd;color:white;padding:15px;font-size:24px;}
.container{display:flex;padding:20px;}
table{border-collapse:collapse;width:100%;}
th,td{border:1px solid #ddd;padding:8px;text-align:center;}
th{background:#0d6efd;color:white;}
button{padding:8px 12px;background:#198754;color:white;border:none;cursor:pointer;}
input{padding:5px;margin:5px;}
</style>
</head>
<body>
<header>GEEDI SUPERMARKET POS</header>

<div style="padding:20px;">
<h3>Add Product</h3>
<form method="POST" action="/add">
<input name="name" placeholder="Name" required>
<input name="price" placeholder="Price" required>
<input name="qty" placeholder="Qty" required>
<button>Add</button>
</form>

<h3>Products</h3>
<table>
<tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th><th>Sell</th></tr>
{% for p in products %}
<tr>
<td>{{p[0]}}</td>
<td>{{p[1]}}</td>
<td>${{p[2]}}</td>
<td>{{p[3]}}</td>
<td><a href="/sell/{{p[0]}}"><button>Sell</button></a></td>
</tr>
{% endfor %}
</table>

<h3>Total Revenue: ${{revenue}}</h3>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    cursor.execute("SELECT * FROM products")
    products=cursor.fetchall()

    cursor.execute("SELECT SUM(total) FROM sales")
    revenue=cursor.fetchone()[0]
    if revenue is None: revenue=0

    return render_template_string(HTML,products=products,revenue=revenue)

@app.route("/add",methods=["POST"])
def add():
    name=request.form["name"]
    price=float(request.form["price"])
    qty=int(request.form["qty"])

    cursor.execute("SELECT id,quantity FROM products WHERE name=?",(name,))
    existing=cursor.fetchone()

    if existing:
        cursor.execute("UPDATE products SET quantity=? WHERE id=?",
                       (existing[1]+qty,existing[0]))
    else:
        cursor.execute("INSERT INTO products(name,price,quantity) VALUES(?,?,?)",
                       (name,price,qty))
    conn.commit()
    return redirect("/")

@app.route("/sell/<int:id>")
def sell(id):
    cursor.execute("SELECT name,price,quantity FROM products WHERE id=?",(id,))
    p=cursor.fetchone()
    if p and p[2]>0:
        cursor.execute("UPDATE products SET quantity=quantity-1 WHERE id=?",(id,))
        cursor.execute("INSERT INTO sales VALUES(?,?,?,?,?)",
                       (p[0],p[1],1,p[1],
                        datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
    return redirect("/")

>>>>>>> 61582baf7b4a49b5c5fcd3c5006e0c4cddf8a009
app.run(debug=True)