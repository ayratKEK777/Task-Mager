import datetime
import sqlite3
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QListWidget, QTextEdit, QInputDialog


# TODO: переписать класс до нг переделать Qlabel до нг,


class TimeToNewYear():
    def to_new_year():
        now = datetime.datetime.now()
        NY = datetime.datetime(2024, 1, 1)
        d = NY - now

        mm, ss = divmod(d.seconds, 60)
        hh, mm = divmod(mm, 60)
        return "{0} д, {1} ч, {2} мин, {3} сек.".format(d.days, hh, mm, ss)


class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список задач")
        self.resize(300, 400)

        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()
        self.hbox6 = QHBoxLayout()

        self.task_list = QListWidget()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_Qlabel_time_to_new_year)
        self.timer.start(1000)

        self.setWindowIcon(QIcon("17463067.png"))

        self.time_to_new_year_Qlabel = QLabel(TimeToNewYear.to_new_year(), self)
        self.active_tasks_Qlabel = QLabel("Задачи:", self)
        self.completed_tasks_Qlabel = QLabel("Выполненные задачи:", self)

        self.active_tasks_QListWidget = QListWidget()
        self.active_tasks_QListWidget.itemDoubleClicked.connect(self.delete_task_in_list_completed_tasks)
        self.completed_tasks_QListWidget = QListWidget()
        self.completed_tasks_QListWidget.itemDoubleClicked.connect(self.delete_task_in_completed_list)

        self.btn_add_task = QPushButton("Добaвление задачи", self)
        self.btn_add_task.clicked.connect(self.add_task_into_db)

        self.text_task_discription = QTextEdit()

        self.init_ui()

    def init_ui(self):
        self.set_structure()
        self.create_db()
        self.update_list_with_active_tasks()
        self.update_list_with_completed_tasks()
        self.show()

    def update_Qlabel_time_to_new_year(self):
        self.time_to_new_year_Qlabel.setText(TimeToNewYear.to_new_year())
        self.time_to_new_year_Qlabel.update()

    def create_db(self):
        try:
            self.conn = sqlite3.connect("Task_List.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""CREATE TABLE IF NOT EXISTS tasks
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT,
            status_task INTEGER DEFAULT 1 );""")
            self.conn.commit()
        except:
            print("Не удалось Создать ДБ")

    def add_task_into_db(self):
        text, ok = QInputDialog.getText(self, 'Добавление Задачи',
                                        "Введите задачу")
        if ok:
            self.cur.execute("""INSERT INTO tasks(task_name) VALUES (?);""", (text,))
            self.conn.commit()
            self.active_tasks_QListWidget.clear()
            self.update_list_with_active_tasks()

    def update_list_with_active_tasks(self):
        self.active_tasks_QListWidget.clear()
        list_active_tasks = list(self.cur.execute("SELECT task_name FROM tasks where status_task = 1"))
        self.conn.commit()
        list_active_tasks = [x[0] for x in list_active_tasks]
        for task in list_active_tasks:
            self.active_tasks_QListWidget.addItem(i)

    def update_list_with_completed_tasks(self):
        self.completed_tasks_QListWidget.clear()
        list_completed_tsk = list(self.cur.execute("SELECT task_name FROM tasks where status_task = 0"))
        self.conn.commit()
        list_completed_tsk = [x[0] for x in list_completed_tsk]
        for i in list_completed_tsk:
            self.completed_tasks_QListWidget.addItem(i)

    def delete_task_in_list_completed_tasks(self):
        task = self.active_tasks_QListWidget.currentItem().text()
        self.cur.execute("UPDATE tasks SET status_task = 0 WHERE task_name = (?)", (task,))
        self.conn.commit()
        self.update_list_with_active_tasks()
        self.update_list_with_completed_tasks()

    def delete_task_in_completed_list(self):
        task = self.completed_tasks_QListWidget.currentItem().text()
        self.cur.execute("DELETE FROM tasks WHERE task_name = (?)", (task,))
        self.conn.commit()
        self.update_list_with_completed_tasks()

    def set_structure(self):
        self.hbox1.addWidget(self.time_to_new_year_Qlabel)
        self.vbox.addLayout(self.hbox1)

        self.hbox2.addWidget(self.btn_add_task)
        self.vbox.addLayout(self.hbox2)

        self.hbox3.addWidget(self.active_tasks_Qlabel)
        self.vbox.addLayout(self.hbox3)

        self.hbox4.addWidget(self.active_tasks_QListWidget)
        self.vbox.addLayout(self.hbox4)

        self.hbox5.addWidget(self.completed_tasks_Qlabel)
        self.vbox.addLayout(self.hbox5)

        self.hbox6.addWidget(self.completed_tasks_QListWidget)
        self.vbox.addLayout(self.hbox6)

        self.setLayout(self.vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = ToDoList()
    sys.exit(app.exec_())
