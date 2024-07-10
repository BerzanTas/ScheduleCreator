import pandas as pd
import re

class ScheduleCreator:
    def __init__(self) -> None:
        self.path = "schedule.xlsx"
        
    # private method for reading excel file
    def _read(self):
        self.df = pd.read_excel(self.path)

    def _beautify(self): # this function formats the dataframe
        self.df.columns = [self.df.columns[0]] + pd.to_datetime(self.df.columns[1:]).strftime('%d-%m').tolist()

    def _build_data(self):
        self.availability = {} # dictionary for availabilty of workers depending on excel file
        workers = self.df.iloc[:,0].tolist() # list of workers

        # add day and workers available that day to dict
        for day in self.df.columns[1:]:
            self.availability[day] = {} # initialize a nested dictionary for each day

            for worker, availability in zip(workers, self.df[day]):
                if availability != "N":
                    start_hour, end_hour = re.split(" |,|-", availability)
                    self.availability[day][worker] = {"From":start_hour, "To":end_hour}
        
        self.availability = sorted(self.availability[day].items(), key=lambda x: (self.availability[x]["From"]))
        for day in self.availability.keys():
            print(day,": ",self.availability[day])

    def build_schedule(self):
        pass
        
    def main(self):
        self._read()
        self._beautify()
        self._build_data()
        self.build_schedule()
        
        #print(self.df)