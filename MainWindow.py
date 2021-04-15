# coding: utf-8

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PdfManager import pdf_merger, pdf_spliter, pdf_extractor


class ExampleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 画面サイズを取得 (a.desktop()は QtWidgets.QDesktopWidget )
        desktop = QApplication.desktop()
        geometry = desktop.screenGeometry()
        self.resize(geometry.width() / 2, geometry.height() / 2)
        # ウインドウサイズ(枠込)を取得
        framesize = self.frameSize()
        # ウインドウの位置を指定
        self.move(geometry.width() / 2 - framesize.width() / 2,
                  geometry.height() / 2 - framesize.height() / 2)
        self.setWindowTitle('pdf manager')
        self.main_layout = QHBoxLayout()
        self.main_layout.addStretch(1)

        # menu checkbox
        self.checkboxes = QVBoxLayout()
        self.checkboxes.addStretch(1)
        self.btngroup = QButtonGroup()
        self.merger = QRadioButton('結合')
        self.spliter = QRadioButton('分割')
        self.extractor = QRadioButton('抽出')
        self.merger.setChecked(True)
        self.btngroup.addButton(self.merger)
        self.btngroup.addButton(self.spliter)
        self.btngroup.addButton(self.extractor)
        self.checkboxes.addWidget(self.merger)
        self.checkboxes.addWidget(self.spliter)
        self.checkboxes.addWidget(self.extractor)
        self.checkboxes.addStretch(1)
        self.main_layout.addLayout(self.checkboxes)
        self.main_layout.addStretch(1)

        # file getter
        self.file_getter = QVBoxLayout()
        self.file_get_button = QPushButton('読み込み')
        self.file_get_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.file_get_button.clicked.connect(self.validFileGet)
        self.file_getter.addWidget(self.file_get_button)

        # values
        self.texts = QGridLayout()
        self.sp_start_l = QLabel('分割するページ\n(指定したページから2個目が始まる)')
        self.sp_start = QLineEdit(self)
        self.sp_start.setValidator(QIntValidator())

        self.ex_start_l = QLabel('抽出するページ(スタート)')
        self.ex_start = QLineEdit(self)
        self.ex_start.setValidator(QIntValidator())
        self.ex_end_l = QLabel('抽出するページ(エンド)(文書に含まれます)')
        self.ex_end = QLineEdit(self)
        self.ex_end.setValidator(QIntValidator())

        self.texts.addWidget(self.sp_start_l, 0, 0)
        self.texts.addWidget(self.sp_start, 0, 1)
        self.texts.addWidget(self.ex_start_l, 1, 0)
        self.texts.addWidget(self.ex_start, 1, 1)
        self.texts.addWidget(self.ex_end_l, 2, 0)
        self.texts.addWidget(self.ex_end, 2, 1)
        self.file_getter.addLayout(self.texts)

        self.main_layout.addLayout(self.file_getter)

        # 表示
        self.setLayout(self.main_layout)
        self.show()

    def validFileGet(self):
        if self.merger.isChecked():
            filenames = self.openFileNamesDialog()
            savepath = self.saveFileDialog()
            pdf_merger(filenames, savepath)
        else:
            filename = self.openFileNameDialog()
            savepath = self.saveFileDialog()
            if self.spliter.isChecked():
                pdf_spliter(filename, int(self.sp_start.text()), savepath)
            else:
                pdf_extractor(filename, int(self.ex_start.text()),
                              int(self.ex_end.text()), savepath)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "Pdf file (*.pdf);;All Files (*)")
        if fileName:
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            self, "QFileDialog.getOpenFileNames()", "", "Pdf file (*.pdf);;All Files (*)")
        if files:
            return files

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "Pdf file (*.pdf);;All Files (*)")
        if fileName:
            return fileName


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ew = ExampleWidget()
    sys.exit(app.exec_())
