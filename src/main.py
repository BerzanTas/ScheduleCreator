from scheduleCreator import ScheduleCreator
from PySide6.QtWidgets import QApplication
from gui import WindowControl
import database, sys

# main application
class App:
    def __init__(self) -> None:
        self.db = database.EmployeeData()
        self.gui_app = QApplication(sys.argv)
        self.window_controller = WindowControl()

    # main method
    def run(self):
        self.window_controller.show()
        self.gui_app.exec()
        self.window_controller.main_program.generate_button.clicked.connect(self._generate_schedule)
        #self.db.main()
        # call main method of ScheduleCreater class
        #self.schedule_creator.main()

    def _generate_schedule(self):
        user_mail = self.window_controller.email
        availability_path = self.window_controller.main_program.av_file_path
        rpt_path = self.window_controller.main_program.rpt_file_path
        self.schedule_creator = ScheduleCreator(user_mail, availability_path, rpt_path, self.db)

if __name__ == "__main__":
    app = App()
    app.run()