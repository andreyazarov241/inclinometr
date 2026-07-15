from openpyxl import load_workbook
from PyQt5.QtWidgets import QFileDialog


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

        data = []

        row = 18

        while True:

            depth = sheet[f"A{row}"].value

            # дошли до конца таблицы
            if depth is None:
                break

            zenith = sheet[f"B{row}"].value
            azimuth = sheet[f"C{row}"].value

            data.append({
                "depth": float(depth),
                "zenith": float(zenith),
                "azimuth": float(azimuth)
            })

            row += 1

        workbook.close()
        print ("проверка")
        print("Глубина\tЗенит\tАзимут")

        for row in data:
            print(
                f"{row['depth']:.2f}\t"
                f"{row['zenith']:.2f}\t"
                f"{row['azimuth']:.2f}"
            )
        return data