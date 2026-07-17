from math import sin, cos, sqrt, atan2, radians, acos, asin, tan

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
    
            cos_beta = cos(I2-I1) - sin(I1)*sin(I2)*(1-cos(A2-A1))

    
            # Из-за ошибок округления значение может выйти
            # немного больше 1 или меньше -1.
            cos_beta = max(-1.0, min(1.0, cos_beta))
    
            beta = acos(cos_beta)
    
            # =====================================================
            # Коэффициент RF
            # =====================================================
    
            if abs(beta) < 1e-10:
                RF = 1.0
            else:
                RF = (2 / beta) * tan(beta / 2)
    
            # =====================================================
            # Приращения координат
            # =====================================================
    
            dNorth = (dMD / 2) * (sin(I1) * cos(A1)+ sin(I2) * cos(A2))* RF
    
            dEast = (dMD / 2) * (sin(I1) * sin(A1)+ sin(I2) * sin(A2))* RF
    
            dTVD = (dMD / 2 * (cos(I1)+ cos(I2))* RF )
    
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