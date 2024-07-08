import pandas as pd

class Reader:
    def __init__(self, path) -> None:
        self.path = path
    
    def _read(self):
        file = pd.read_excel(self.path, "Arkusz1")
        return file

    def main(self):
        file = self._read()

        print(file.head(5))