import os
import sys
import json
from datetime import datetime
from inspect import getsourcefile

from PySide2 import QtWidgets as qtw
from PySide2 import QtGui as qtg
from PySide2 import QtCore as qtc


class CigaretteCounter(qtw.QDialog):

    WINDOW_TITLE = 'Cigarette Counter'
    data_path = "D:/Orkah/learning_PySide2/CigaretteCounter/data.json"
    DATA = dict()

    seuil_moyen_content = 6
    cigarette_number = 0
    seuil_content = 3
    date = ""
    time = ""

    def __init__(self, parent=None):
        super(CigaretteCounter, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ qtc.Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(280, 300)

        self.geometry=None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.retrieve_data()

        self.build_num_cig_string()
        self.build_cig_timer_string()
        
    def create_widgets(self):
        self.label01 = qtw.QLabel()

        self.shame_button = qtw.QPushButton()
        self.shame_button.setIcon(qtg.QIcon("D:/Orkah/learning_PySide2/CigaretteCounter/Logo/logo_content.png"))
        self.shame_button.setIconSize(qtc.QSize(100, 100))

        self.label02 = qtw.QLabel()

    def create_layouts(self):
        count_layout = qtw.QHBoxLayout()
        count_layout.addStretch()
        count_layout.addWidget(self.label01)
        count_layout.addStretch()

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self.shame_button)

        time_layout = qtw.QHBoxLayout()
        time_layout.addStretch()
        time_layout.addWidget(self.label02)
        time_layout.addStretch()

        main_layout = qtw.QVBoxLayout(self)
        main_layout.addLayout(count_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(time_layout)

    def create_connections(self):
        self.shame_button.clicked.connect(self.going_to_smoke)

    def build_num_cig_string(self):
        self.label01.setText(F"You've smoked {self.cigarette_number} cigarettes today")

    def build_cig_timer_string(self):
        self.label02.setText(F"Last smoke was -- {self.day}d - {self.hour}h - {self.minute}m - {self.second}s -- ago")

    def going_to_smoke(self):
        self.cigarette_number += 1
        self.build_num_cig_string()
        self.build_data()
        self.swap_logo()
        self.save_to_json(self.data_path, self.DATA)

    def build_data(self):
        self.year, self.month, self.day, self.hour, self.minute, self.second = self.get_today_date_time()
        self.date = F"{self.month}/{self.day}/{self.year}"
        self.time = F"{self.hour}:{self.minute}:{self.second}"

        if self.date not in self.DATA.keys():
            self.DATA[self.date] = [self.cigarette_number, [self.time]]

        else:
            cig_num, timers = self.DATA[self.date]

            if self.cigarette_number > cig_num: pass 
            else: self.cigarette_number = cig_num

            timers.insert(0, self.time)
            self.DATA[self.date] = [self.cigarette_number, timers]

    def get_today_date_time(self):
        now     = datetime.now()

        day     = now.strftime("%d")
        month   = now.strftime("%m")
        year    = now.strftime("%Y")
        hour    = now.strftime("%H")
        minute  = now.strftime("%M")
        second  = now.strftime("%S")

        return year, month, day, hour, minute, second

    def retrieve_data(self):
        self.data_path = os.path.abspath(getsourcefile(lambda: 0)).replace("CigaretteCounter.py", "data.json")
        self.DATA = self.get_data(self.data_path) or dict()
        self.build_data()
        self.get_time_spent()

    def get_data(self, data_file):
        try:
            with open(data_file, "r") as jsonFile:
                return json.load(jsonFile)
        except:
            print(F"Could not read : {data_file}")
 
    def save_to_json(self, data_file, data):
        with open(data_file, "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
            print(F"Data was successfully written to : {data_file}")

    def get_time_spent(self):
        self.date
        self.time

        

    def swap_logo(self):
        logo_path = "D:/Orkah/learning_PySide2/CigaretteCounter/Logo/"

        if self.cigarette_number <=self.seuil_content:
            self.shame_button.setIcon(qtg.QIcon(F"{logo_path}logo_content.png"))

        elif self.seuil_content < self.cigarette_number <= self.seuil_moyen_content:
            self.shame_button.setIcon(qtg.QIcon(F"{logo_path}logo_moyen content.png"))

        elif self.cigarette_number > self.seuil_moyen_content:
            self.shame_button.setIcon(qtg.QIcon(F"{logo_path}logo_pas_content.png"))

    def showEvent(self, e):
        super(CigaretteCounter, self).showEvent(e)
        if self.geometry:
            self.restoreGeometry(self.geometry)
   
    def closeEvent(self, e):
        if isinstance(self, CigaretteCounter):
            super(CigaretteCounter, self).closeEvent(e)
            self.geometry = self.saveGeometry()


if __name__ == '__main__':
    # Create the Qt Application
    app = qtw.QApplication(sys.argv)
    # Create and show the form
    ranApp = CigaretteCounter()
    ranApp.show()

    # Run the main Qt loop
    sys.exit(app.exec_())