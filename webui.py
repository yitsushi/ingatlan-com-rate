from bottle import Bottle, run, request, static_file
from database import Database

app = Bottle()

db = Database()

@app.route('/')
def hello():
    return '''<html>
<head><title>ingatlan.com rate</title></head>
<body>
<div class='container'>Content...</div>
<script src="/static/app.js"></script>
<link rel="stylesheet" type="text/css" href="/static/app.css" />
</body>
</html>'''

@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@app.route('/properties')
def properties():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return 'fek ye!'
    return {"properties": db.fetch_all("properties", order="order by decided desc,predicted desc, price/area asc")}

@app.route('/decide/<property_id>/<decision>')
def decide(property_id, decision):
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return 'fek ye!'
    item = db.update_decision("properties", "id", property_id, int(float(decision)))
    if item == None or item[13] != int(float(decision)):
        return {"success": False}

    return {"success": True, "prop": item}


run(app, host='0.0.0.0', port=8080)

