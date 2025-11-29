from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import login_user, UserMixin, current_user
from flask_mysqldb import MySQL
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')

#https://www.geeksforgeeks.org/python/how-to-add-authentication-to-your-app-with-flask-login/
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
#https://www.geeksforgeeks.org/python/how-to-add-authentication-to-your-app-with-flask-login/
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT userID, first_name, role FROM users WHERE userID = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    if user_data:
        return User(user_data['userID'], user_data['first_name'], user_data['role'])
    return None






app.config['SECRET_KEY'] = 'ActiveUser'



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'HollowKnight1!'
app.config['MYSQL_DB'] = 'csc206cars'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def landing():
    return render_template("landingPage.html", title="Home")


@app.route("/basetemplete.html")
def base():
    return render_template("basetemplete.html", title="Tim's Cars")

@app.route("/buyacar.html")
def buyacar():
    mileage_filter = request.args.get('mileage')
    description_filter = request.args.get('description')
    model_filter = request.args.get('model')
    year_filter = request.args.get('year')
    fuel_filter = request.args.get('fuel')

    cursor = mysql.connection.cursor()

    query = """
        SELECT v.vehicleID, v.vin, v.mileage, v.description, v.model_name, v.model_year, v.fuel_type
        FROM vehicles v
        WHERE 1=1
    """
   # https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
    paramiters = []
    if mileage_filter:
        query += " AND v.mileage = %s"
        paramiters.append(mileage_filter)
     # https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application  
    if description_filter:
        query += " AND v.description = %s"
        paramiters.append(description_filter)
    if model_filter:
        query += " AND v.model_name = %s"
        paramiters.append(model_filter)
    if year_filter:
        query += " AND v.model_year = %s"
        paramiters.append(year_filter)
    if fuel_filter:
        query += " AND v.fuel_type = %s"
        paramiters.append(fuel_filter)



    cursor.execute(query, paramiters)
    vehicles = cursor.fetchall()

    cursor.execute("SELECT DISTINCT mileage FROM vehicles ORDER BY mileage")
    all_mileage = [row['mileage'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT description FROM vehicles ORDER BY description")
    all_descriptions = [row['description'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT model_name FROM vehicles ORDER BY model_name")
    all_models = [row['model_name'] for row in cursor.fetchall()]


#https://www.tutorialspoint.com/explain-the-use-of-select-distinct-statement-in-mysql-using-python
    cursor.execute("SELECT DISTINCT model_year FROM vehicles ORDER BY model_year")
    all_years = [row['model_year'] for row in cursor.fetchall()]

#https://www.tutorialspoint.com/explain-the-use-of-select-distinct-statement-in-mysql-using-python
    cursor.execute("SELECT DISTINCT fuel_type FROM vehicles ORDER BY fuel_type")
    all_fuels = [row['fuel_type'] for row in cursor.fetchall()]
 
    cursor.close()

   
    return render_template("buyacar.html", title="Buy a car", vehicles=vehicles, all_mileage= all_mileage, all_descriptions=all_descriptions, all_models=all_models, all_years=all_years,all_fuels=all_fuels, selected_year=year_filter, selected_fuel=fuel_filter, selected_mileage=mileage_filter, selected_description=description_filter, selected_model=model_filter)


class User(UserMixin):
    def __init__(self, user_id, first_name, role):
        self.user_id = user_id
        self.first_name = first_name
        self.role = role

    def get_id(self):
        return str(self.user_id)

#https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/
@app.route('/SignIn.html', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
#https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userID, first_name, password, role FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and user_data['password'] == password:
            user = User(user_data['userID'], user_data['first_name'], user_data['role'])
            login_user(user, remember=True)
            return redirect(url_for('landing'))  
        else:
            flash('Invalid username or password, please try again.')
            return render_template('SignIn.html', title="Sign In")
    return render_template('SignIn.html', title="sign In")



@app.route("/VehicleDetails.html/<string:vin>")
def VehicleDetails(vin):
    cursor = mysql.connection.cursor()

    # get the vehicle row
    cursor.execute("SELECT * FROM vehicles WHERE vin = %s", (vin,))
    v = cursor.fetchone()
    if not v:
        cursor.close()
        return redirect(url_for('buyacar'))

    vehicle_id = v['vehicleID']
    parts_sql = """
        SELECT
            ven.vendor_name,
            ven.phone_number,
            ven.street,
            ven.city,
            ven.state,
            ven.postal_code ,
            p.part_number, 
            p.description, 
            p.quantity, 
            p.cost,
            p.quantity * p.cost AS total_cost,
            p.status,
            c.phone_number,
            c.email_address,
            c.street,c.city,
            c.state,
            c.postal_code,
            c.first_name, 
            c.last_name
        FROM 
            vehicles v
            INNER JOIN partorders po ON v.vehicleID = po.vehicleID
            INNER JOIN parts p ON po.part_orderID = p.part_orderID
            INNER JOIN vendors ven ON po.vendorID = ven.vendorID
            INNER JOIN purchasetransactions pt ON v.vehicleID = pt.vehicleID
            INNER JOIN customers c ON pt.customerID = c.customerID
        WHERE 
            v.vehicleID = %s
    """
    #https://jinja.palletsprojects.com/en/stable/templates/
    #for the %s
    #https://jinja.palletsprojects.com/en/stable/templates/
    cursor.execute(parts_sql, (vehicle_id,))
    parts = cursor.fetchall()

    cursor.close()

    return render_template("VehicleDetails.html", role=current_user.role if current_user.is_authenticated else None, v=v, parts=parts )





if __name__ == "__main__":
    app.run(debug=True)