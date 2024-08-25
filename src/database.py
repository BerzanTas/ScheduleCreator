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
        

        
