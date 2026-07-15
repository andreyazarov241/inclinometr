from math import sin, cos, sqrt, atan2, radians

from .excel_reader import ExcelReader


class Mathematics:

    def __init__(self, dialog):
        self.dialog = dialog
        self.excel = ExcelReader(dialog)

    def loadInclinometry(self):

        filename = self.excel.open_file()

        if filename is None:
            return

        data = self.excel.read_inclinometry(filename)

        print("Прочитано:")
        print(data)