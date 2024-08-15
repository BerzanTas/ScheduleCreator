import pandas as pd
import numpy as np
import re
from settings import *


class ScheduleCreator:
    def __init__(self, emp_db) -> None:
        self.path = "schedule.xlsx"
        self.emp_db = emp_db
        pd.set_option('future.no_silent_downcasting', True)
        
    # private method for reading excel file
    def _read(self) -> None:
        self.df = pd.read_excel(self.path)

    # private method for formating the dataframe for more human readability
    def _beautify(self) -> None:
        self.df.columns = [self.df.columns[0]] + pd.to_datetime(self.df.columns[1:]).strftime('%d-%m').tolist()

    # private method for creating a dictionary with all the needed information
    def _build_data(self) -> dict:
        # dictionary for availabilty of workers depending on excel file
        availability = {}
        self.employees = self.df.iloc[:,0].tolist() # list of workers by id

        # change id to actual name based on database records
        names = self.emp_db.get_data("id, name")

        for i, employee in enumerate(self.employees):
            self.employees[i] = self.emp_db.get_data("name", condition=f"id={employee}")["name"]

        # add day and workers available that day to dict
        for day in self.df.columns[1:]:
            availability[day] = {} # initialize a nested dictionary for each day

            for employee, av in zip(self.employees, self.df[day]):
                if av != "N": # eliminate records
                    # split given in excel file hours to "FROM" and "TO" using re library
                    start_hour, end_hour = re.split(" |,|-", av)
                    availability[day][employee] = {"From":int(start_hour), "To":int(end_hour)} # add to dictionary as nested dict

        for day in availability:
            # sort dict for every day, so employees available sooner for that day, are listed earlier
            availability[day] = dict(sorted(availability[day].items(), key=lambda item: item[1]["From"]))
        
        return availability
    
    # method for checking and raising errors if an employee has more unavailability than MAX_UNAVAILABILITY
    def _check_unavailability(self) -> None:
        # this method is only for non-student workers and workers without a second job
        employee_list = self.emp_db.get_data("id, name", condition="student=0")

        # creating new dataframe with only non student workers
        df = self.df.loc[self.df[self.df.columns[0]].isin(row["id"] for row in employee_list)]
        df = df.replace('N', np.nan)

        # dataframe with employee ID and number of declared unavailability
        df = pd.concat([df[df.columns[0]], df.isnull().sum(axis=1)], axis=1, keys=["ID", "N"]).reset_index(drop=True)
        # keep only workers with unavailability more than max_unavailability
        df = df[df["N"] > MAX_UNAVAILABILITY]
        
        new_list = df["ID"].to_list()
        
        # if new_list is not None, than print error
        if new_list:
            print(f"Warning!\nFollowing employees have more than {MAX_UNAVAILABILITY} unavailability declared:")
            for emp in new_list:
                print(emp)
    
    # this method is for adding up employee hours in the availability file and checking 
    # whether it is approximately the same as in the employee WORK_TIME record in the database
    def _check_total_hour_amount(self, schedule:dict) -> dict:
        schedule_employee_hour = {}
        db_employee_hour = self.emp_db.get_data("name,WORK_TIME")
        print(db_employee_hour)
        for employee in self.employees:
            schedule_employee_hour[employee] = 0

            for day in schedule:
                for hour in schedule[day]:
                    if employee in schedule[day][hour]:
                        schedule_employee_hour[employee] += 1

        for row in db_employee_hour:
            if schedule_employee_hour[row["name"]] != row["WORK_TIME"]:
                print(f"\nEmployee {row["name"]} has {schedule_employee_hour[row["name"]]} work hours isntead of {row["WORK_TIME"]}!\n")

        return schedule_employee_hour
    
    def _check_hour_per_day(self, schedule:dict, day:str) -> dict:
        schedule_employee_hour = {}

        for employee in self.employees:
            schedule_employee_hour[employee] = 0

            for hour in schedule[day]:
                if employee in schedule[day][hour]:
                    schedule_employee_hour[employee] += 1

        return schedule_employee_hour

    def build_schedule(self, availability: dict) -> dict:
        """
            Builds final schedule dictionary based on availability dictionary
        """
        schedule = dict()
        for day in availability.keys():
            schedule[day] = {} # create nested dict for every day
            self._check_total_hour_amount(schedule)
            for hour in range(OPEN_HOUR, CLOSE_HOUR):
                employee_number = 0 # number of working employee in current hour
                working_employees = [] # list of working employees
                schedule[day][hour] = {} # create nested dict for every hour in every day
                number_of_hours = self._check_hour_per_day(schedule, day)

                for employee in availability[day]:
                    # check if the employee is available to work in current hour
                    if hour in range(availability[day][employee]["From"], availability[day][employee]["To"]) and employee_number <= MAX_WORKERS and number_of_hours[employee] < MAX_HOURS:
                        working_employees.append(employee)
                        employee_number += 1
                # add list of employee to current hour
                schedule[day][hour] = working_employees
            print(day, ": ", schedule[day],"\n")
            
        
    def main(self):
        self._read()
        self._beautify()
        self._check_unavailability()
        av = self._build_data()
        self.build_schedule(av)