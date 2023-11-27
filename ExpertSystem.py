from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMessageBox
import DialogWindowES_ver2
import sys
import sqlite3 as sql

class Data:
    def get_initial_data(self):
        with sql.connect("Concept.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT name, find FROM concepts1 WHERE find != ?", ("None", ))
            data1, data2, data3 = self.change_type_data(cur.fetchall())
            return data1, data2, data3

    def get_final_predicts(self, hard_concept):
        recomends = []
        with sql.connect("Concept.db") as con:
            cur = con.cursor()
            for i in range(len(hard_concept)):
                cur.execute("SELECT annotation FROM concepts1 WHERE name = ? AND final = 1", (hard_concept[i],))
                temp = cur.fetchone()
                if temp != None:
                    recomends.append(temp)
            return recomends

    def change_type_data(self, data):
        """Функция для преобразования данных из БД в формат словаря"""
        simple_consepts = {} # Здесь будут хранится факты, в которых нет условия ИЛИ
        consepts = {} # Здесь будут хранится факты, в которых есть ИЛИ
        linked_consepts = {}
        for elem in data:
            if "or" not in elem[1] and ")" not in elem[1]:
               simple_consepts[elem[0]] = elem[1].split(", ")
            elif "or" in elem[1] and ")" not in elem[1]:
                consepts[elem[0]] = [elem.split(",") for elem in elem[1].split("or")]
            elif ")" in elem[1]:
                linked_consepts[elem[0]] = elem[1].split(",")
        return simple_consepts, consepts, linked_consepts


class ExpertSystem:
    def __init__(self, concepts):
        data = Data()
        self.concepts = concepts
        self.data1, self.data2, self.data3 = data.get_initial_data()
        self.find_concepts(self.data1, self.data2, self.data3)
        self.recomends = data.get_final_predicts(self.hard_concept)
        self.answer = self.get_answer(self.recomends)

    def find_concepts(self, data1, data2, data3):
        self.hard_concept = []
        i = 0
        temp = None
        while temp != len(self.hard_concept):
            temp = len(self.hard_concept)
            for key, value in data1.items():
                if all(elem in self.hard_concept or elem in self.concepts for elem in value) and key not in self.hard_concept:
                    self.hard_concept.append(key)
            for key, value in data2.items():
                for i in value:
                    if any(elem in self.hard_concept or elem in self.concepts for elem in i) and key not in self.hard_concept:
                        self.hard_concept.append(key)
            for key, value in data3.items():
                temp_list = self.hard_concept + self.concepts
                if all(any(temp in elem for temp in temp_list) for elem in value) and key not in self.hard_concept:
                    self.hard_concept.append(key)




    def get_answer(self, recomends):
        if len(recomends) != 0:
            print_string = "\n"
            for elem in recomends:
                print_string = print_string + elem[0] + "\n"
            return f"На основе ваших предпочтений мы подобрали вам произведения: {print_string}"
        else:
            return "На основе ваших предпочтений мы не смогли подобрать вам произведения"

    def return_result(self):
        return self.answer

class MainWindow(QtWidgets.QMainWindow, DialogWindowES_ver2.Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.concepts = []
        self.get_result.clicked.connect(self.get_final_result)


    def __get_answers(self):
        if self.answer1.isChecked():
            self.concepts.append("ХЛ")
        if self.negative_answer1.isChecked():
            self.concepts.append("!ХЛ")

        if self.answer2.isChecked():
            self.concepts.append("С")

        if self.negative_answer2.isChecked():
            self.concepts.append("!С")

        if self.answer3.isChecked():
            self.concepts.append("РК")
        if self.negative_answer3.isChecked():
            self.concepts.append("!РК")

        if self.answer4.isChecked():
            self.concepts.append("НЛ")
        if self.negative_answer4.isChecked():
            self.concepts.append("!НЛ")

        if self.answer5.isChecked():
            self.concepts.append("ИоЛ")
        if self.negative_answer5.isChecked():
            self.concepts.append("!ИоЛ")

        if self.answer6.isChecked():
            self.concepts.append("ОВ")
        if self.negative_answer6.isChecked():
            self.concepts.append("!ОВ")

        if self.answer7.isChecked():
            self.concepts.append("ЗП")
        if self.negative_answer7.isChecked():
            self.concepts.append("!ЗП")

        if self.answer8.isChecked():
            self.concepts.append("ОП")

        if self.negative_answer8.isChecked():
            self.concepts.append("!ОП")

        if self.answer9.isChecked():
            self.concepts.append("Л19В")
        if self.negative_answer9.isChecked():
            self.concepts.append("!Л19В")


    def get_final_result(self):
        self.__get_answers()
        ExpSystem = ExpertSystem(self.concepts)
        self.print_result.setText(ExpSystem.return_result())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())