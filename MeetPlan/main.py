from flask import *

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetplan.sqlite3'

@app.route("/oobe", methods = ['POST', 'GET'])
def oobe():
    if (request.method == 'POST'):
        try:
            
    return render_template("oobe.html")


def dbinit():
    from meetplan import db
    db.init_app(app)

@app.route("/", methods = ['POST', 'GET'])
def dashboard():
    classname = request.values.get('class')
    print(classname)
    if classname != None:
        return render_template("dashboard.html", name="Mitja", classes=["1b", "2b", "3a"],
        mon=["", "DKE", "KEM", ""],
        tue=[],
        wed=[],
        thu=[],
        fri=[],
        sat=[]
        )
    else:
        return render_template("dashboard.html", name="Mitja", classes=["1b", "2b", "3a"],
        mon=[], tue=[], wed=[], thu=[], fri=[], sat=[]
        )
