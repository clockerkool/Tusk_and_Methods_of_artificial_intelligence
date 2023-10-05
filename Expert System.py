from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMessageBox
import DialogWindowES_ver2
import sys
import sqlite3 as sql

class MainWindow(QtWidgets.QMainWindow, DialogWindowES_ver2.Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        # self.get_data()
        self.concepts = []
        self.final_predict = []
        self.get_result.clicked.connect(self.get_final_result)


    def __get_answers(self):
        if self.answer1.isChecked():
            self.concepts.append("ХЛ")

        if self.answer2.isChecked():
            self.concepts.append("С")

        if self.answer3.isChecked():
            self.concepts.append("РК")

        if self.answer4.isChecked():
            self.concepts.append("НЛ")

        if self.answer5.isChecked():
            self.concepts.append("ИоЛ")

        if self.answer6.isChecked():
            self.concepts.append("ОВ")

        if self.answer7.isChecked():
            self.concepts.append("ЗП")

        if self.answer8.isChecked():
            self.concepts.append("ОП")

        if self.answer9.isChecked():
            self.concepts.append("Л19В")

    def get_final_result(self):
        hard_concept = [] # список для зависимых понятий
        self.__get_answers() # получение понятий из ответов пользователя

        with sql.connect("Concept.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT name, find FROM concepts1 WHERE find != ?", ("None", ))
            data1, data2 = self.change_type_data(cur.fetchall())

            for i in range(10):
                for key, value in data1.items():
                    if all(elem in hard_concept or elem in self.concepts  for elem in value) and key not in hard_concept:
                        hard_concept.append(key)
                for key, value in data2.items():
                    if any([elem in hard_concept or elem in self.concepts  for elem in half] for half in value) and key not in hard_concept:
                        hard_concept.append(key)

            print(hard_concept)




            recomends = []
            for i in range(len(hard_concept)):
                cur.execute("SELECT annotation FROM concepts1 WHERE name = ? AND final = 1", (hard_concept[i],))
                temp = cur.fetchone()
                if temp != None:
                    recomends.append(temp)

            print_string = "\n"
            for elem in recomends:
                print_string = print_string + elem[0] + "\n"

            self.print_result.setText(f"На основе ваших предпочтений мы подобрали вам произведения: {print_string}")
            #self.pesult_out(recomends)


    def change_type_data(self, data):
        """Функция для преобразования данных из БД в формат словаря"""
        print(data)
        simple_consepts = {} # Здесь будут хранится факты, в которых нет условия ИЛИ
        consepts = {} # Здесь будут хранится факты, в которых есть ИЛИ
        for elem in data:
            if "or" not in elem[1]:
               simple_consepts[elem[0]] = elem[1].split(", ")
            else:
                consepts[elem[0]] = [elem.split(",") for elem in elem[1].split("or")]

        return simple_consepts, consepts

    def result_out(self, recomends):
        if len(recomends) != 0:
            print_string = "\n"
            for elem in recomends:
                print_string = print_string + elem[0] + "\n"

            self.print_result.setText(f"На основе ваших предпочтений мы подобрали вам произведения: {print_string}")
        else:
            self.print_result.setText(f"На основе ваших предпочтений мы не смогли подобрать вам произведения")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())