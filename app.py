from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key= "kahsdfwi8askdflaksdfjasdfjljksdfl"

userpass = "mysql+pymysql://root:@"
basedir = '127.0.0.1'
dbname="/company"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    def __init__(self, name, designation, address, phone):
        self.name = name
        self.designation = designation
        self.address = address
        self.phone = phone
    
    

@app.route("/")
def index():
    data_employe = db.session.query(Employes)
    return render_template("index.html", data=data_employe)

@app.route("/input", methods=['GET','POST'])
def input_data():
    if request.method=="POST":
        name = request.form['name']
        designation = request.form['designation']
        address = request.form['address']
        phone = request.form['phone']

        add_data = Employes(name,designation, address, phone)

        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('index'))

    return render_template("input.html")

@app.route("/edit/<int:id>")
def edit_data(id):
    employee_data = Employes.query.get(id)
    return render_template('edit.html', data = employee_data)

@app.route("/process_edit", methods=['GET', 'POST'])
def process_edit():
    employee_data = Employes.query.get(request.form.get('id'))

    employee_data.name = request.form['name']
    employee_data.designation = request.form['designation']
    employee_data.address = request.form['address']
    employee_data.phone = request.form['phone']

    db.session.commit()

    flash('Successfully data updated!')

    return redirect(url_for('index'))


@app.route("/delete/<int:id>")
def delete_data(id):
    employee_data = Employes.query.get(id)
    db.session.delete(employee_data)
    db.session.commit()

    flash('Data is successfuly deleted!')

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)
