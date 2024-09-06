import requests
import sensitive_data

class Login:
    """User verification using API"""

    def __init__(self):
        self.api_url = sensitive_data.API_URL+'/login'

    # send user information to endpoint
    def connect(self, email, password):
        data = {
            'email': email,
            'password': password
        }

        response = requests.post(self.api_url, json=data)
        print(response.json())
        return(response.status_code)
    

class Register:
    """User registration using API"""

    def __init__(self):
        self.api_url = sensitive_data.API_URL+'/register'

    def register(self, username, email, password):
        data = {
            'username': username,
            'email': email,
            'password': password
        }

        
        response = requests.post(self.api_url, json=data)
        result = response.json()
        print(result)

        return(response.status_code)

    def check_if_exists(self, type, value):
        data = {
            'type':type,
            'value': value
        }

        response = requests.post(self.api_url+'/check', json=data)
        print(response)
        print(response.status_code)
        
        # return True if exists
        if response.status_code == 409:
            return True
        else:
            return False
        
class EmployeeData:
    def __init__(self):
        self.api_url = sensitive_data.API_URL+'/data'

    def checkIfTableExist(self, user_email):
        data = {
            "user_email": user_email
        }
        response = requests.post(self.api_url+'/checkemployee', json=data)
        return response.status_code
    
    def getEmployeeTable(self, user_email):
        data = {
            "user_email": user_email
        }
        employee_data = requests.post(self.api_url+'/get', json=data).json()
        try:
            return employee_data["result"]
        except KeyError:
            return []

    def addEmployee(self, user_email, employee_id, employee_name, working_time, student_or_second_job):
        data = {
            "user_email": user_email,
            "employee_id": employee_id,
            "employee_name": employee_name,
            "work_time": working_time,
            "student_or_second_job": student_or_second_job
        }
        response = requests.post(self.api_url+'/add', json=data)
        print(response)
    
    def deleteEmployee(self, user_email, employee_id):
        data = {
            "user_email": user_email,
            "employee_id": employee_id,
        }
        response = requests.post(self.api_url+'/delete', json=data)
        print(response)

    def updateEmployeeData(self, user_email, old_employee_id, employee_id, employee_name, working_time, student_or_second_job):
        data = {
            "user_email": user_email,
            "old_employee_id": old_employee_id,
            "employee_id": employee_id,
            "employee_name": employee_name,
            "work_time": working_time,
            "student_or_second_job": student_or_second_job
        }
        response = requests.post(self.api_url+'/update', json=data)
        print(response)
        