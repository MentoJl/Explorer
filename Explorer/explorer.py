from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QPushButton, QLabel, QLineEdit, QVBoxLayout, QApplication, QTreeView, QFileSystemModel
from PyQt5.QtCore import QSortFilterProxyModel, QFileInfo, QFile, QDir, Qt
import os, sys, shutil


class Ui_MainWindow(object):

    model = QFileSystemModel()
    cut = False
    sorting_name = False
    path = os.path.dirname(os.path.abspath(__file__))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 581)
        MainWindow.setMinimumSize(QtCore.QSize(800, 581))
        MainWindow.setMaximumSize(QtCore.QSize(800, 581))
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.delete = QtWidgets.QPushButton(self.centralwidget)
        self.delete.setGeometry(QtCore.QRect(90, 10, 41, 31))
        self.delete.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.path + "/trash.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.delete.setIcon(icon)
        self.delete.setIconSize(QtCore.QSize(20, 20))
        self.delete.setObjectName("delete")
        self.cut = QtWidgets.QPushButton(self.centralwidget)
        self.cut.setGeometry(QtCore.QRect(240, 10, 61, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.path + "/cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cut.setIcon(icon1)
        self.cut.setIconSize(QtCore.QSize(20, 20))
        self.cut.setObjectName("cut")
        self.create = QtWidgets.QPushButton(self.centralwidget)
        self.create.setGeometry(QtCore.QRect(10, 10, 71, 31))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.path + "/create.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.create.setIcon(icon2)
        self.create.setObjectName("create")
        self.Errors = QtWidgets.QLabel(self.centralwidget)
        self.Errors.setGeometry(QtCore.QRect(530, 10, 261, 31))
        self.Errors.setText("")
        self.Errors.setObjectName("Errors")
        self.explorer = QtWidgets.QTreeView(self.centralwidget)
        self.explorer.setGeometry(QtCore.QRect(10, 50, 781, 511))
        self.explorer.setObjectName("explorer")
        self.paste = QtWidgets.QPushButton(self.centralwidget)
        self.paste.setGeometry(QtCore.QRect(380, 10, 61, 31))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.path + "/paste.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.paste.setIcon(icon3)
        self.paste.setIconSize(QtCore.QSize(20, 20))
        self.paste.setObjectName("paste")
        self.copy = QtWidgets.QPushButton(self.centralwidget)
        self.copy.setGeometry(QtCore.QRect(310, 10, 61, 31))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.path + "/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy.setIcon(icon4)
        self.copy.setIconSize(QtCore.QSize(20, 20))
        self.copy.setObjectName("copy")
        self.rename = QtWidgets.QPushButton(self.centralwidget)
        self.rename.setGeometry(QtCore.QRect(450, 10, 71, 31))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.path + "/rename.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        self.rename.setIcon(icon5)
        self.rename.setObjectName("rename")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.model.setRootPath("")
        self.explorer.setModel(self.model)
        self.explorer.setRootIndex(self.model.index(""))
        self.explorer.show()
        self.header = self.explorer.header()
        self.header.setSortIndicatorShown(True)
        self.header.setSectionsClickable(True)
        self.events()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Explorer"))
        self.cut.setText(_translate("MainWindow", "Cut"))
        self.create.setText(_translate("MainWindow", "Create"))
        self.paste.setText(_translate("MainWindow", "Paste"))
        self.copy.setText(_translate("MainWindow", "Copy"))
        self.rename.setText(_translate("MainWindow", "Rename"))

    def inputText(self, string):
        dialog = QDialog()
        layout = QVBoxLayout()
        label = QLabel(f"Input {string}:")
        line_edit = QLineEdit()
        button = QPushButton("Ok")
        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)
        dialog.setLayout(layout)
        def return_text():
            text = line_edit.text()
            dialog.accept()
            return text
        button.clicked.connect(return_text)
        dialog.exec_()
        return line_edit.text()

    def getCurrentPath(self):
        current_index = self.explorer.currentIndex()
        file_model = self.explorer.model()
        return str(file_model.filePath(current_index))

    def createFile(self):
        file_name = self.inputText("filename")
        file_info = QFileInfo(file_name)
        path = self.getCurrentPath()
        if file_info.suffix():
            with open(path + "/" + file_name, 'w'):
                None
        elif file_name != "":
            os.mkdir(path + "/" + file_name)

    def deleteFile(self, path=""):
        if path == "":
            path = self.getCurrentPath()
        file = QFile(path)
        dir = QDir(path)
        if not file.remove():
            dir.removeRecursively()

    def copyFile(self):
        self.copy_path = self.getCurrentPath()
        self.cut = False

    def cutFile(self):
        self.copy_path = self.getCurrentPath()
        self.cut = True

    def pasteFile(self):
        if os.path.exists(self.copy_path):
            if not self.cut and os.path.isdir(self.copy_path):
                shutil.copytree(self.copy_path, os.path.join(self.getCurrentPath(), os.path.basename(self.copy_path)))
            elif not self.cut:
                shutil.copy(self.copy_path, self.getCurrentPath())
            else:
                shutil.move(self.copy_path, self.getCurrentPath())
                

    def renameFile(self):
        new_file_name = self.inputText("new name")
        if new_file_name != "":
            path = self.getCurrentPath()
            index = self.explorer.currentIndex()
            new_path = QDir(os.path.dirname(path)).absolutePath() + "/" + new_file_name
            os.rename(path, new_path)
            self.model.setData(index, new_file_name)

    def sortAll(self, index):
        print(index)
        self.explorer.sortByColumn(index, Qt.DescendingOrder)

    def openFile(self, index):
        if not index.isValid():
            return
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            os.startfile(file_path)

    def events(self):
        try:
            self.create.clicked.connect(lambda: self.createFile())
            self.delete.clicked.connect(lambda: self.deleteFile())
            self.copy.clicked.connect(lambda: self.copyFile())
            self.cut.clicked.connect(lambda: self.cutFile())
            self.paste.clicked.connect(lambda: self.pasteFile())
            self.rename.clicked.connect(lambda: self.renameFile())
            self.explorer.header().sectionClicked.connect(self.sortAll)
            self.explorer.doubleClicked.connect(self.openFile)
        except Exception as error:
            self.Errors.setText(f"Error: {error}")

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())