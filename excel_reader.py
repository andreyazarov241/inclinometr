from openpyxl import load_workbook
from PyQt5.QtWidgets import QFileDialog
from qgis.PyQt import QtWidgets

class ExcelReader:

    def __init__(self, dialog):
        self.dialog = dialog

    def open_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self.dialog,
            "Выберите файл инклинометрии",
            "",
            "Excel (*.xlsx *.xls)"
        )
        print(filename)
        if not filename:
            return None

        return filename


    def read_inclinometry(self, filename):
        """
        Чтение таблицы инклинометрии.

        A18 -> Глубина по стволу, м
        B18 -> Зенитный угол, град
        C18 -> Азимут GRID, град
        """

        workbook = load_workbook(
            filename,
            data_only=True
        )

        sheet = workbook.active

        self.data = []

        row = 18

        while True:

            depth = sheet[f"A{row}"].value

            # дошли до конца таблицы
            if depth is None:
                break

            zenith = sheet[f"B{row}"].value
            azimuth = sheet[f"C{row}"].value

            self.data.append({
                "depth": float(depth),
                "zenith": float(zenith),
                "azimuth": float(azimuth)
            })

            row += 1

        workbook.close()
        print ("проверка")
        print("Глубина\tЗенит\tАзимут")

        for row in self.data:
            print(
                f"{row['depth']:.2f}\t"
                f"{row['zenith']:.2f}\t"
                f"{row['azimuth']:.2f}"
            )
        return self.data
    
    
    def fill_table(self):
        table = self.dialog.tableInclinometry
        table.setRowCount(0)
        for row_data in self.data:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(
                row,
                0,
                QtWidgets.QTableWidgetItem(
                    f"{row_data['depth']:.2f}"
                )
            )
            table.setItem(
                row,
                1,
                QtWidgets.QTableWidgetItem(
                    f"{row_data['zenith']:.2f}"
                )
            )
            table.setItem(
                row,
                2,
                QtWidgets.QTableWidgetItem(
                    f"{row_data['azimuth']:.2f}"
                )
            )