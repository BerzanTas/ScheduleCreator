from scheduleCreator import ScheduleCreator

# main application
class App:
    def __init__(self) -> None:
        self.schedule_creator = ScheduleCreator()

    # main method
    def run(self):
        # call main method of ScheduleCreater class
        self.schedule_creator.main()


if __name__ == "__main__":
    app = App()
    app.run()