import sqlite3

class EmployeeDB:
    """
        Database for employee information
    """
    def __init__(self, db_name:str = "employee") -> None:
        # creating connection to database (or create if does not exist)
        self.conn = sqlite3.connect(f"data/{db_name}.db")

    def build_table(self, table_name:str = "employees"):
        """
            Creates table in employee database.
            Columns and datatypes are hardcoded
        """
        self.conn.execute(f'''CREATE TABLE {table_name}
                    (ID INT PRIMARY KEY,
                    NAME           TEXT    NOT NULL,
                    WORK_TIME      INT     NOT NULL,
                    STUDENT        BOOLEAN NOT NULL);''')

    def add_record(self, employee_id:int, employee_name:str, work_time:int, student_or_sj:bool, table_name:str = "employees"):
        self.conn.execute(f"INSERT INTO {table_name} (ID, NAME, WORK_TIME, STUDENT) VALUES (?, ?, ?, ?)", [employee_id, employee_name, work_time, student_or_sj])
        self.conn.commit()
    
    def get_data(self, columns:str = "*", table_name:str = "employees", condition:str = None):
        """
            The get_data() method returns list of dictionaries with data from database based on arguments.
            The default values will return everything from 'employees' table.
            Arguments takes string with SQL format, so for example, if you want to get 'id' and 'name'
            of all students or thoose with second job, you should give those arguments:
            get_data(information="id, name", condition="student=1").
        """
        result_list = []

        if condition:
            result = self.conn.execute(f"SELECT {columns} FROM {table_name} WHERE {condition};")
        else:
            result = self.conn.execute(f"SELECT {columns} FROM {table_name};")
        
        if columns == "*":
            columns = "ID, NAME, WORK_TIME, STUDENT"
        
        keys = columns.split(",")
            
        for row in result:
            result_dict = {}
            for i, key in enumerate(keys):
                result_dict[key] = row[i]

            # if there is just one row, then return it as a dictionary
            if len(row) == 1:
                return result_dict
            
            result_list.append(result_dict)

        return result_list
    
    def show_data(self, result:list):
        for i in range(len(result)):
            for key in result[i].keys():
                print(key, "=", result[i][key], end="       ")
            print()

    def main(self):
        try:
            self.build_table()
            self.add_record(10609303, 'Berzan', 80, True)
            self.add_record(10504030, 'Gabriela W.', 120, False)
            self.add_record(10203040, 'Sylwester S.', 120, True)
            self.add_record(10101010, 'Patryk Vege', 40, True)
            self.add_record(10654535, 'Martyna S.', 160, False)
        except:
            pass