from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'temp123'
app.config['MYSQL_DB'] = 'csc206cars'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/LandingPage")
def landing():
    return render_template("landingPage.html", title="Home")

@app.route("/basetemplete.html")
def base():
    return render_template("basetemplete.html", title="Tim's Cars")
@app.route("/")
def buyacar():
    year_filter = request.args.get('year')
    fuel_filter = request.args.get('fuel')

    cursor = mysql.connection.cursor()

    query = """
        SELECT v.vehicleID, v.vin, v.mileage, v.description, v.model_name, v.model_year, v.fuel_type
        FROM vehicles v
        WHERE 1=1
    """
   # https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
    paramitors = []
    if year_filter:
        query += " AND v.model_year = %s"
        paramitors.append(year_filter)
    if fuel_filter:
        query += " AND v.fuel_type = %s"
        paramitors.append(fuel_filter)
    #https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application, I know it is about sqlalchmy and i used db but the two (accoring to the internet) are very similar 

    cursor.execute(query, paramitors)
    vehicles = cursor.fetchall()

#https://www.tutorialspoint.com/explain-the-use-of-select-distinct-statement-in-mysql-using-python
    cursor.execute("SELECT DISTINCT model_year FROM vehicles ORDER BY model_year")
    all_years = [row['model_year'] for row in cursor.fetchall()]

#https://www.tutorialspoint.com/explain-the-use-of-select-distinct-statement-in-mysql-using-python
    cursor.execute("SELECT DISTINCT fuel_type FROM vehicles ORDER BY fuel_type")
    all_fuels = [row['fuel_type'] for row in cursor.fetchall()]

    cursor.close()

    return render_template("buyacar.html", title="Buy a car",vehicles=vehicles, all_years=all_years, all_fuels=all_fuels, selected_year=year_filter,selected_fuel=fuel_filter)

@app.route("/SignIn.html")
def signin():
    return render_template("SignIn.html", title="Sign In")

if __name__ == "__main__":
    app.run(debug=True)
