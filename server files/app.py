import bcrypt
from flask import Flask, request, jsonify
import mysql.connector
import os
from mailserver import send_confirmation_email

app = Flask(__name__)

# function to establish connection with the MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME')
        )
        return connection
    except mysql.connector.Error as err:
        # log the error and return None if connection fails
        print(f"Error: {err}")
        return None

# endpoint to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # hash the provided password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    db = connect_to_db()
    if db is None:
        # return error if connection to the database fails
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # insert the new user into the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        db.commit()

        # send a confirmation email upon successful registration
        send_confirmation_email(email)

        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        # handle cases where a duplicate entry is found (username or email already exists)
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            if 'username' in err.msg:
                return jsonify({"message": "Username already exists"}), 409
            elif 'email' in err.msg:
                return jsonify({"message": "Email already exists"}), 409
            else:
                return jsonify({"message": "Duplicate entry error"}), 409
        else:
            # log other database errors
            print(f"Error: {err}")
            return jsonify({"message": "Registration failed due to a database error"}), 500
    finally:
        # close the database cursor and connection
        cursor.close()
        db.close()

# endpoint to check if a username or email is already taken
@app.route('/register/check', methods=['POST'])
def check_availability():
    data = request.json
    field_type = data.get('type')
    value =  data.get('value')

    # validate the field type
    if field_type not in ['username', 'email']:
        return jsonify({"message": "Invalid field type"}), 400

    db = connect_to_db()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # query the database to check if the username or email already exists
        query = f"SELECT 1 FROM users WHERE {field_type} = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchone()

        if result:
            return jsonify({"message": f"{field_type} already exists"}), 409
        else:
            return jsonify({"message": f"{field_type} is available"}), 200
    except mysql.connector.Error as err:
        return jsonify({"message": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        db.close()

# endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = connect_to_db()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # retrieve the hashed password from the database for the given email
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            stored_password_hash = result[0]

            # ensure the password hash is encoded properly
            if isinstance(stored_password_hash, str):
                stored_password_hash = stored_password_hash.encode('utf-8')

            # check if the provided password matches the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                return jsonify({"message": "Login successful!"}), 200
            else:
                return jsonify({"message": "Invalid credentials"}), 401
        else:
            return jsonify({"message": "User not found"}), 404
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"message": "Failed to log in"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"message": "An unexpected error occurred"}), 500
    finally:
        cursor.close()
        db.close()

# endpoint to check if an employee table exists for a user
@app.route('/data/checkemployee', methods=['POST'])
def checkIfEmployeeTableExists():
    data = request.json
    user_email = data.get('user_email')

    db = connect_to_db()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # fetch the user ID using the provided email
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()[0]
    except Exception as e:
        raise e

    try:
        # check if there is an employee table for the given user ID
        query = f"SELECT 1 FROM employee_data WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        if result:
            return jsonify({"message": "Employee table exists"}), 200
        else:
            return jsonify({"message": "User has no employee record"}), 410
    except mysql.connector.Error as err:
        return jsonify({"message": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        db.close()

# endpoint to retrieve employee data for a user
@app.route('/data/get', methods=['POST'])
def getData():
    data = request.json
    user_email = data.get('user_email')

    db = connect_to_db()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # get the user ID from the provided email
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()[0]
    except Exception as e:
        raise e

    try:
        # retrieve all employee data for the given user ID
        query = f"SELECT * FROM employee_data WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        if result:
            return jsonify({"result": result}), 200
        else:
            return jsonify({"message": f"No employee table"}), 409
    except mysql.connector.Error as err:
        return jsonify({"message": f"Database error: {err}"}), 500
    finally:
        cursor.close()
        db.close()

# endpoint to add a new employee record
@app.route('/data/add', methods=['POST'])
def add_employee():
    data = request.json
    user_email = data.get('user_email')
    emp_id = data.get('employee_id')
    emp_name = data.get('employee_name')
    work_time = data.get('work_time')
    student_second_job = data.get('student_or_second_job')

    db = connect_to_db()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # fetch the user ID using the provided email
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()[0]

    except Exception as e:
        raise

    try:
        # insert the new employee record into the employee_data table
        cursor.execute("INSERT INTO employee_data (user_id, employee_id, employee_name, working_time, student_or_second_job) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, emp_id, emp_name, work_time, student_second_job))
        db.commit()

        return jsonify({"message": "Employee added successfully!"}), 201
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

# endpoint to delete an employee record
@app.route('/data/delete', methods=['POST'])
def delete_employee():
    data = request.json
    user_email = data.get('user_email')
    emp_id = data.get('employee_id')

    db = connect_to_db()

    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # fetch the user ID using the provided email
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()[0]
    except Exception as e:
        raise

    try:
        # delete the employee record matching the user ID and employee ID
        cursor.execute("DELETE FROM employee_data WHERE user_id = %s AND employee_id = %s",
                       (user_id, emp_id))
        db.commit()

        return jsonify({"message": "Employee deleted successfully!"}), 201
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

# endpoint to update an employee record
@app.route('/data/update', methods=['POST'])
def update_employee_data():
    data = request.json
    user_email = data.get('user_email')
    old_emp_id = data.get('old_employee_id')
    emp_id = data.get('employee_id')
    emp_name = data.get('employee_name')
    work_time = data.get('work_time')
    student_second_job = data.get('student_or_second_job')

    db = connect_to_db()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = db.cursor()

    try:
        # fetch the user ID using the provided email
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()[0]

    except Exception as e:
        raise

    try:
        # update the employee record with new data
        cursor.execute("UPDATE employee_data SET employee_id = %s, employee_name = %s, working_time = %s, student_or_second_job = %s WHERE user_id = %s AND employee_id = %s",
                       (emp_id, emp_name, work_time, student_second_job, user_id, old_emp_id))
        db.commit()

        return jsonify({"message": "Employee updated successfully!"}), 201
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    # start the Flask application on a specified port
    app.run(host='0.0.0.0', port=1) # I can't expose my port that's why I wrote random port number here
