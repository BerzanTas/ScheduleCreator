from scheduleCreator import ScheduleCreator
import database

# main application
class App:
    def __init__(self) -> None:
        self.db = database.EmployeeDB()
        self.schedule_creator = ScheduleCreator(self.db)

    # main method
    def run(self):
        self.db.main()
        # call main method of ScheduleCreater class
        self.schedule_creator.main()


if __name__ == "__main__":
    app = App()
    app.run()