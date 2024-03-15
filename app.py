from flask import Flask,render_template,request,redirect

from models import db,Emp
import random
import date
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db.init_app(app)



@app.before_request
def create():
    db.create_all()

@app.route("/create",methods=["POST","GET"])
def index():
    if request.method=="POST":
        emp_id=request.form["emp_id"]
        name=request.form["name"]
        age=request.form["age"]
        position=request.form["position"]

        employee=Emp(emp_id=emp_id,name=name,age=age,position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect("/view")


    return render_template("register.html")


@app.route("/view")
def view():
    Employee=Emp.query.all()
    return render_template("view.html",Employee=Employee)
    



@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    employee = Emp.query.get_or_404(id)

    if request.method == "POST":
        employee.emp_id = request.form["emp_id"]
        employee.name = request.form["name"]
        employee.age = request.form["age"]
        employee.position = request.form["position"]

        db.session.commit()
        return redirect("/view")

    return render_template("update.html", employee=employee)

@app.route("/delete/<int:id>", methods=["POST","GET"])
def delete(id):
    employee = Emp.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(employee)
        db.session.commit()
        return redirect("/view")
    return render_template("delete.html",employee=employee)



if __name__=="__main__":
    app.run(debug=True)
