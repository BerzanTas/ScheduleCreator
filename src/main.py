from excelReader import Reader

class App:
    def __init__(self) -> None:
        path = "schedule.xlsx"
        self.reader = Reader(path)

    def run(self):
        self.reader.main()


if __name__ == "__main__":
    app = App()
    app.run()