from flask import Flask , request , render_template , redirect
from tinydb import TinyDB , Query


app = Flask(__name__)
app.env = "development"

db = TinyDB("data.json")
Todo = Query()



@app.route("/")
def home():
  visitor_ip = visitor_ip
  check_ip = db.contains(Todo.ip==visitor_ip)
  
  if check_ip:
    works = [i.get("work") for i in db.search(Todo.ip==visitor_ip) ]
    show_works=True
    
  else:
    show_works=False
    works=[None]
    
  return render_template("index.html",show_works=show_works,works=works,ip=visitor_ip)



@app.route("/add",methods=["POST"])
def add():
  work = request.values["work"]
  
  if len(work) < 2 or "<" in work: return redirect("/")
  
  visitor_ip=request.remote_addr
  data = {
    "ip":visitor_ip,
    "work":work
  }
  db.insert(data)
  return redirect("/")
  
  

@app.route("/delete")
def delete():
  visitor_ip=request.remote_addr
  work = request.values["work"]
  checker = db.contains((Todo.ip==visitor_ip)&(Todo.work==work))
  
  if checker:
    visitor_ip=request.remote_addr
    db.remove((Todo.ip==visitor_ip)&(Todo.work==work))
  
  return redirect("/")


app.run(debug=True)