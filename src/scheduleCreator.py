import pandas as pd
import numpy as np
import re
from settings import *
import database
import random
from dtime import Time


class ScheduleCreator:
    def __init__(self, user_mail, availability_path, rpt_path, emp_db = None) -> None:
        self.user_mail = user_mail
        self.availability_path = availability_path
        self.rpt_path = rpt_path
        self.emp_db = emp_db
        pd.set_option('future.no_silent_downcasting', True)
        self.main()
        
    # reading excel file
    def _read(self) -> None:
        self.df = pd.read_excel(self.availability_path)
        self.rpt_df = pd.read_excel(self.rpt_path)
        

    # Changing %Y-%M-%D %H:%M:%S format to %D-%M format
    def _beautify(self) -> None:
        self.df.columns = [self.df.columns[0]] + pd.to_datetime(self.df.columns[1:]).strftime('%d-%m').tolist()
        self.rpt_df.columns = [self.rpt_df.columns[0]] + pd.to_datetime(self.rpt_df.columns[1:]).strftime('%d-%m').tolist()
        self.rpt_df['Time'] = pd.to_datetime(self.rpt_df['Time'], format='%H:%M:%S').dt.strftime('%H:%M')
        
    
    def _get_from_employee_list(self, column:list) -> list:
        """
        Creates and returns nested list of desired columns from employee database.
        column = [0,1,2,3], where 0 = employee id, 1 = employee name, 2 = working time, 3 = is student/second job.
        """
        employee_list = self.emp_db.getEmployeeTable(self.user_mail)
        # [[user_id, emp_id, name, wt, student]]
        employee_list = [row[1:] for row in employee_list]
        # [[emp_id, name, wt, student]]
        
        # create nested list with desired columns
        result = [[row[i] for i in column] for row in employee_list]
        return result
    
    def build_schedule(self):
        """Creates nested dictionary with employee list as value"""

        working_time = self._get_from_employee_list([0, 2])
        working_time_dict = dict()
        for key, value in working_time:
            working_time_dict[key] = float(value)

        # dictionary for monthly hour limit, if employee has reached limit than turn the value to True
        self.monthly_hour_limit = dict()
        for employee in list(map(str, self.df.iloc[:,0].tolist())):
            self.monthly_hour_limit[employee] = False

        # main schedule dictionary
        schedule = dict()
        for day in self.df.columns[1:]:
            print(f"Day {day}:")
            # create a nested dictionary as a value for every day in dataframe
            schedule[day] = dict()

            # list of employees that are not students and don't have a second job
            non_student_secondjob_employee_list = self._get_from_employee_list([0, 3])
            non_student_secondjob_employee_list = [emp[0] for emp in non_student_secondjob_employee_list if emp[1] == 0]
            # creating weights for random choices
            non_student_weights = [working_time_dict[employee] for employee in non_student_secondjob_employee_list]
            normalized_non_student_weights = [int(weight*4) for weight in non_student_weights]

            # check if any employee reached hour limit
            self._monthly_hour_limit(schedule, working_time_dict)

            for hour in range(OPEN_HOUR.hour, CLOSE_HOUR.hour):
                min_employee = self.rpt_df.loc[self.rpt_df['Time'] == f"{hour}:00", day].values[0]
                emp_number = 0
                hour = Time(hour)

                # create a list for employee names as a value of nested dictionary
                schedule[day][hour] = list()

                # find all employees available at current hour
                available_employees = self.df[self.df[day].apply(lambda x: self._available_employees(x, hour))]
                available_employees_list = available_employees[self.df.columns[0]].tolist()
                available_employees_list = list(map(str, available_employees_list))
                # set weights depending on working time for random choices
                weights = [working_time_dict[employee] for employee in available_employees_list]
                normalized_weights = [int(weight*4) for weight in weights]

                non_student_secondjob_employee_list_copy = non_student_secondjob_employee_list.copy()
                normalized_non_student_weights_copy = normalized_non_student_weights.copy()

                # try adding to list, employees from an hour before, so we can keep continuity
                if hour > OPEN_HOUR:
                    for employee in schedule[day][hour-Time(1,0)]:
                        if emp_number < min_employee or self._daily_hour(schedule, employee) < 4:
                            if (employee in available_employees_list or employee in non_student_secondjob_employee_list) and not self._daily_hour_limit(schedule[day], employee):
                                schedule[day][hour].append(employee)
                                emp_number += 1
                
                # if we are still missing some employees, than choose from our lists of employee
                while emp_number < min_employee:
                    # if lenght of available employees list is equal to 1 and is not already in our schedule list, than add the employee.
                    if len(available_employees_list) <= 1:
                        if  available_employees_list and available_employees_list[0] not in schedule[day][hour] and not self.monthly_hour_limit[available_employees_list[0]]:
                            schedule[day][hour].append(available_employees_list[0])
                            emp_number += 1
                        else:
                            if len(non_student_secondjob_employee_list_copy) == 0:
                                break
                            elif len(non_student_secondjob_employee_list) == 1:
                                if non_student_secondjob_employee_list[0] not in schedule[day][hour] and not self.monthly_hour_limit[non_student_secondjob_employee_list_copy[0]]:
                                    schedule[day][hour].append(non_student_secondjob_employee_list_copy[0])
                                else:
                                    break
                            # if lenght of available employees list is more than 1, than choose random weigthed employee from list
                            else:
                                employee = random.choices(non_student_secondjob_employee_list_copy, weights=normalized_non_student_weights_copy, k=1)[0]
                                if employee not in schedule[day][hour] and not self.monthly_hour_limit[employee]:
                                    schedule[day][hour].append(employee)
                                    emp_number += 1
                                # remove employee from list to avoid endless loop and remove his weight
                                normalized_non_student_weights_copy.pop(non_student_secondjob_employee_list_copy.index(employee))
                                non_student_secondjob_employee_list_copy.remove(employee)

                    else:
                        employee = random.choices(available_employees_list, weights=normalized_weights, k=1)[0]
                        if employee not in schedule[day][hour] and not self.monthly_hour_limit[employee]:
                            schedule[day][hour].append(employee)
                            emp_number += 1
                        normalized_weights.pop(available_employees_list.index(employee))
                        available_employees_list.remove(employee)
                
                
                print(f"{hour}: {schedule[day][hour]}  {len(schedule[day][hour])}/{min_employee}")
            print("\n")
        return schedule
    
    def _available_employees(self, emp_hour, hour) -> list:
        # Sprawdź, czy pracownik jest nieobecny (oznaczone jako "N")
        if emp_hour == 'N':
            return False
        # Jeśli godziny są w formacie "10-16", rozdziel je i sprawdź
        if '-' in emp_hour:
            start_hour, stop_hour = map(Time, map(int, emp_hour.split('-')))
            return start_hour <= hour < stop_hour
        # Jeśli godziny są w formacie "10 21" (bez myślnika), również rozdziel
        elif ' ' in emp_hour:
            start_hour, stop_hour = map(Time, map(int, emp_hour.split(' ')))
            return start_hour <= hour < stop_hour
        return False
    
    def _daily_hour(self, schedule, employee):
        """Return number of hours that employee is been working"""
        hours = 0
        for hour in schedule:
            if employee in schedule[hour]:
                hours += 1
        
        return hours
    
    def _daily_hour_limit(self, schedule, employee):
        """Check if employee reached his daily hour limit"""
        hours = self._daily_hour(schedule, employee)
        
        if hours >= MAX_HOURS:
            return True
        else:
            return False
    
    def _monthly_hour_limit(self, schedule, WorkTime):
        """Controls employees monthly hour limit"""

        for employee in self.monthly_hour_limit.keys():
            if self.monthly_hour_limit[employee] != True:
                hours = 0
                for day in schedule:
                    for hour in schedule[day]:
                        if employee in schedule[day][hour]:
                            hours += 1

                # if employee reached hour limit, than change his value in dictionary
                #WorkTime = WorkTime[employee]
                if hours >= WorkTime[employee]*FULL_TIME:
                    self.monthly_hour_limit[employee] = True

    def _show_monthly_hours(self, schedule):
        employees = self.df.iloc[:,0].tolist()
        employees = list(map(str, employees))
        schedule_employee_hour = {}
        db_employee_hour = self._get_from_employee_list([0,2])
        for employee in employees:
            schedule_employee_hour[employee] = 0

            for day in schedule:
                for hour in schedule[day]:
                    if employee in schedule[day][hour]:
                        schedule_employee_hour[employee] += 1

        for row in db_employee_hour:
            if schedule_employee_hour[row[0]] != float(row[1])*FULL_TIME:
                print(f"\nEmployee {row[0]} has {schedule_employee_hour[row[0]]} work hours instead of {int(float(row[1])*FULL_TIME)}!\n")

    def _file_data_validation(self):
        """Validate uploaded files data to ensure it correctness"""
        pass
            
    def main(self):
        self._read()
        self._beautify()
        schedule = self.build_schedule()
        self._show_monthly_hours(schedule)