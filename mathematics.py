from math import sin, cos, sqrt, atan2, radians, acos, asin, tan

from .excel_reader import ExcelReader
from qgis.PyQt import QtWidgets



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
        data = self.excel.read_inclinometry(filename)
        self.excel.fill_table()
        
    def calculateInclinometry(self):
        """
        Расчет траектории методом минимальной кривизны.
        Формулы используются согласно методическому пособию.
        """
    
        # Таблица инклинометрии
        data = self.excel.data
    
        # Если таблица пустая — ничего не считаем
        if len(data) == 0:
            return
        # Таблица результатов
        table = self.dialog.tableInclinometry
        # ==========================================================
        # Координаты устья из интерфейса
        # ==========================================================
        
        north = float(self.dialog.txtWellHeadNorth.text())
        east = float(self.dialog.txtWellHeadEast.text())
    
        # Начальная вертикальная отметка
        tvd = 0.0
    
        # ==========================================================
        # Результирующая таблица
        # ==========================================================
    
        result = []
    
        # ==========================================================
        # Первая точка
        # ==========================================================
    
        first = {}
    
        first["depth"] = data[0]["depth"]
        first["zenith"] = data[0]["zenith"]
        first["azimuth"] = data[0]["azimuth"]
    
        first["north"] = north
        first["east"] = east
        first["tvd"] = tvd
    
        result.append(first)
        
        # Записываем первую строку в таблицу
        table.setItem(
            0,
            3,
            QtWidgets.QTableWidgetItem(f"{north:.3f}")
        )
        
        table.setItem(
            0,
            4,
            QtWidgets.QTableWidgetItem(f"{east:.3f}")
        )
        
        table.setItem(
            0,
            5,
            QtWidgets.QTableWidgetItem(f"{tvd:.3f}")
        )
        # ==========================================================
        # Расчет остальных точек
        # ==========================================================
    
        for i in range(1, len(data)):
    
            # -------------------------------
            # Верхняя точка интервала
            # -------------------------------
    
            p1 = data[i - 1]
    
            # -------------------------------
            # Нижняя точка интервала
            # -------------------------------
    
            p2 = data[i]
    
            # -------------------------------
            # Длина интервала
            # -------------------------------
    
            dMD = p2["depth"] - p1["depth"]
    
            # -------------------------------
            # Углы переводим в радианы
            # -------------------------------
    
            I1 = radians(p1["zenith"])
            I2 = radians(p2["zenith"])
    
            A1 = radians(p1["azimuth"])
            A2 = radians(p2["azimuth"])
    
            # =====================================================
            # Угол β между двумя измерениями
            # =====================================================
    
            cos_beta = cos(I2-I1) - sin(I1) * sin(I2) * (1-cos(A2-A1))

    
            # Из-за ошибок округления значение может выйти
            # немного больше 1 или меньше -1.
            cos_beta = max(-1.0, min(1.0, cos_beta))
    
            beta = acos(cos_beta)
    
            # =====================================================
            # Условие если угол β = 0 (радиус кривизны бесконечен) то используется метод средних углов
            # Иначе используется метод наименьшей кривизны
            # =====================================================
            if abs(beta) < 1e-10:
                # =====================================================
                # Приращения координат методом средних углов
                # =====================================================
                dNorth = dMD * sin((I1+I2) /2) * cos((A1+A2) /2)
                dEast = dMD * sin((I1+I2) /2) * sin((A1+A2) /2)
                dTVD = dMD * cos((I1+I2) /2)
            else:
                RF = (2 / beta) * tan(beta / 2)
    
                # =====================================================
                # Приращения координат методом наименьшей кривизны
                # =====================================================
        
                dNorth = (dMD / 2) * (sin(I1) * cos(A1)+ sin(I2) * cos(A2)) * RF
                dEast = (dMD / 2) * (sin(I1) * sin(A1)+ sin(I2) * sin(A2)) * RF
                dTVD = (dMD / 2 * (cos(I1) + cos(I2)) * RF )
    
            # =====================================================
            # Новые координаты
            # =====================================================
    
            north += dNorth
            east += dEast
            tvd += dTVD
    
            # =====================================================
            # Запись строки результата
            # =====================================================
    
            newRow = {}
    
            newRow["depth"] = p2["depth"]
            newRow["zenith"] = p2["zenith"]
            newRow["azimuth"] = p2["azimuth"]
    
            newRow["north"] = north
            newRow["east"] = east
            newRow["tvd"] = tvd
    
            result.append(newRow)

            # Записываем рассчитанные координаты в таблицу
            table.setItem(
                i,
                3,
                QtWidgets.QTableWidgetItem(f"{north:.3f}")
            )
            
            table.setItem(
                i,
                4,
                QtWidgets.QTableWidgetItem(f"{east:.3f}")
            )
            
            table.setItem(
                i,
                5,
                QtWidgets.QTableWidgetItem(f"{tvd:.3f}")
            )
        # ==========================================================
        # Вывод результата
        # ==========================================================
    
        print()
    
        print(
            "Depth\tZenith\tAzimuth\tNorth\tEast\tTVD"
        )
    
        for row in result:
    
            print(
                f"{row['depth']:8.2f}\t"
                f"{row['zenith']:7.2f}\t"
                f"{row['azimuth']:8.2f}\t"
                f"{row['north']:12.3f}\t"
                f"{row['east']:12.3f}\t"
                f"{row['tvd']:12.3f}"
            )


    # def calculationDeviation(self):
    #     """
    #     Подготовка таблицы расчета отклонений.
    #     """

    #     sourceTable = self.dialog.tableTargets
    #     resultTable = self.dialog.tableCalculationDeviation

    #     # Очистить старые результаты
    #     resultTable.setRowCount(0)

    #     # Количество целей
    #     rows = sourceTable.rowCount()

    #     for row in range(rows):

    #         # Добавляем новую строку
    #         resultTable.insertRow(row)

    #         # ID цели (0 столбец таблицы целей)
    #         idItem = sourceTable.item(row, 0)

    #         # TVD (3 столбец таблицы целей)
    #         tvdItem = sourceTable.item(row, 3)

    #         if tvdItem:
    #             resultTable.setItem(
    #                 row,
    #                 0,
    #                 QtWidgets.QTableWidgetItem(tvdItem.text())
    #             )

    #         if idItem:
    #             resultTable.setItem(
    #                 row,
    #                 1,
    #                 QtWidgets.QTableWidgetItem(idItem.text())
    #             )


    def calculationDeviation(self):
        """
        Расчет координат траектории на глубине целей.
        """

        sourceTable = self.dialog.tableTargets
        resultTable = self.dialog.tableCalculationDeviation

        # Очистить старые результаты
        resultTable.setRowCount(0)

        # Количество целей
        rows = sourceTable.rowCount()

        for row in range(rows):

            # Добавляем новую строку
            resultTable.insertRow(row)

            # ID цели (0 столбец таблицы целей)
            idItem = sourceTable.item(row, 0)

            # TVD (3 столбец таблицы целей)
            tvdItem = sourceTable.item(row, 3)

            if tvdItem:
                resultTable.setItem(
                    row,
                    0,
                    QtWidgets.QTableWidgetItem(tvdItem.text())
                )

            if idItem:
                resultTable.setItem(
                    row,
                    1,
                    QtWidgets.QTableWidgetItem(idItem.text())
                )

        # первые строки таблицы записаны , начинаем расчет координат и отклонений

        tableTargets = self.dialog.tableCalculationDeviation
        tableInclin = self.dialog.tableInclinometry

        # Проходим по всем целям
        for rowTarget in range(tableTargets.rowCount()):

            # Глубина цели
            targetTVD = float(
                tableTargets.item(rowTarget, 0).text()
            )

            # ----------------------------------------
            # Ищем две соседние строки
            # ----------------------------------------

            for row in range(tableInclin.rowCount() - 1):

                tvd1 = float(tableInclin.item(row, 5).text())
                tvd2 = float(tableInclin.item(row + 1, 5).text())

                if tvd1 <= targetTVD <= tvd2:

                    north1 = float(tableInclin.item(row, 3).text())
                    east1  = float(tableInclin.item(row, 4).text())

                    north2 = float(tableInclin.item(row + 1, 3).text())
                    east2  = float(tableInclin.item(row + 1, 4).text())

                    # ----------------------------------------
                    # Коэффициент интерполяции
                    # ----------------------------------------

                    k = (targetTVD - tvd1) / (tvd2 - tvd1)

                    # ----------------------------------------
                    # Интерполяция координат
                    # ----------------------------------------

                    north = north1 + k * (north2 - north1)
                    east  = east1 + k * (east2 - east1)

                    # ----------------------------------------
                    # Запись в таблицу
                    # ----------------------------------------

                    tableTargets.setItem(
                        rowTarget,
                        3,
                        QtWidgets.QTableWidgetItem(f"{north:.3f}")
                    )

                    tableTargets.setItem(
                        rowTarget,
                        4,
                        QtWidgets.QTableWidgetItem(f"{east:.3f}")
                    )

                    break