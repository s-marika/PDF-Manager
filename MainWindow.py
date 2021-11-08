# coding: utf-8
import os
import random
import string

import PyQt5
from PyQt5.QtCore import QFile, QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PdfManager import pdf_merger, pdf_spliter, pdf_extractor

# TODO: ファイルの読み込みを実行前で泣く，別処理として移行．読み込んだファイルのパスを表示する
# TODO: 各機能をタブ分けする


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        if os.name == 'nt':
            self.savepath = os.path.join(
                os.environ['USERPROFILE'], 'Downloads')
        elif os.name == 'posix':
            self.savepath = os.path.join(
                os.environ['USERPROFILE'], 'Downloads')
        self.mode = 0
        self.filename = ""
        self.filenames = ""
        self.initUI()

    def initUI(self):
        # ----- setup window -----
        # 画面サイズを取得 (a.desktop()は QtWidgets.QDesktopWidget )
        desktop = QApplication.desktop()
        geometry = desktop.screenGeometry()
        self.resize(int(geometry.width() / 2), int(geometry.height() / 2))
        # ウインドウサイズ(枠込)を取得
        framesize = self.frameSize()
        # ウインドウの位置を指定
        self.move(int(geometry.width() / 2 - framesize.width() / 2),
                  int(geometry.height() / 2 - framesize.height() / 2))
        self.setWindowTitle('PDF Manager')
        self.main_layout = QGridLayout(self)

        # ----- mode select -----
        self.checkboxes = QHBoxLayout()
        self.btngroup = QButtonGroup()
        self.merger = QRadioButton('結合')
        self.spliter = QRadioButton('分割')
        self.extractor = QRadioButton('抽出')
        
        self.btngroup.addButton(self.merger)
        self.btngroup.addButton(self.spliter)
        self.btngroup.addButton(self.extractor)

        self.checkboxes.addStretch(1)
        self.checkboxes.addWidget(self.merger)
        self.checkboxes.addStretch(1)
        self.checkboxes.addWidget(self.spliter)
        self.checkboxes.addStretch(1)
        self.checkboxes.addWidget(self.extractor)
        self.checkboxes.addStretch(2)

        self.main_layout.addLayout(self.checkboxes, 0, 0, 1, 4)
        # self.main_layout.addStretch(1)
        
        # ----- file select button -----
        self.select_file_frame = QFrame()
        # self.select_file_frame.setFrameStyle(1)
        self.select_file_layout = QGridLayout()
        self.file_get_button = QPushButton('ファイル読み込み')
        self.file_get_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.file_get_button.clicked.connect(self.validFileGet)

        self.file_delete_button = QPushButton('削除')
        self.file_delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.file_delete_button.clicked.connect(self.deleteFileItems)

        self.selected_file_box = QLineEdit("", self)
        self.selected_file_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.selected_file_box.setReadOnly(True)

        self.select_file_layout.addWidget(self.file_get_button, 0, 0, 1, 1)
        self.select_file_layout.addWidget(self.file_delete_button, 0, 1, 1, 1)
        self.select_file_layout.addWidget(self.selected_file_box, 1, 0, 1, 2)
        self.select_file_frame.setLayout(self.select_file_layout)
        self.main_layout.addWidget(self.select_file_frame, 1, 0, 1, 3)

        # ----- mode tab -----
        self.tabs_frame = QFrame()
        self.tabs = QVBoxLayout()

        # ----- merge tab -----
        self.tab_merge = QFrame()
        self.merge_frame = QGridLayout()
                
        self.file_list = QListWidget(self)
        self.file_list.setFrameStyle(1)
        # self.file_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragEnabled(True)
        self.file_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        
        self.merge_frame.setColumnStretch(0, 1)
        self.merge_frame.addWidget(self.file_list, 0, 0, 3, 3)
        self.merge_frame.setColumnStretch(4, 1)
        self.tab_merge.setLayout(self.merge_frame)
        
        self.tabs.addWidget(self.tab_merge)
        
        # ----- split tab -----
        self.tab_split = QFrame(self)
        self.split_frame = QGridLayout()
        
        self.s_texts = QHBoxLayout()
        self.sp_start_l = QLabel('分割後開始ページ')
        self.sp_start_l.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sp_start_l.setWhatsThis('指定したページが、2個目のファイルの開始ページになります')
        self.sp_start = QLineEdit(self)
        self.sp_start.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sp_start.setValidator(QIntValidator())
        self.s_texts.addWidget(self.sp_start_l)
        self.s_texts.addWidget(self.sp_start)
        self.split_frame.addLayout(self.s_texts, 0, 0, 1, 1)
        self.split_frame.setColumnStretch(1, 3)
        self.tab_split.setLayout(self.split_frame)

        self.tabs.addWidget(self.tab_split)

        # ----- extract tab -----
        self.tab_extract = QFrame(self)
        self.extract_frame = QGridLayout()
        
        self.e_texts = QGridLayout()
        self.ex_start_l = QLabel('開始ページ')
        self.ex_start = QLineEdit(self)
        self.ex_start.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ex_start.setValidator(QIntValidator())
        self.ex_end_l = QLabel('終了ページ(文書に含まれます)')
        self.ex_end = QLineEdit(self)
        self.ex_end.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ex_end.setValidator(QIntValidator())

        self.e_texts.addWidget(self.ex_start_l, 0, 0)
        self.e_texts.addWidget(self.ex_start, 0, 1)
        self.e_texts.addWidget(self.ex_end_l, 1, 0)
        self.e_texts.addWidget(self.ex_end, 1, 1)
        self.extract_frame.addLayout(self.e_texts, 0, 0, 1, 1)
        self.extract_frame.setColumnStretch(1, 3)
        self.tab_extract.setLayout(self.extract_frame)

        self.tabs.addWidget(self.tab_extract)
        
        # ----- hide split or extract tab -----
        self.tab_split.hide()
        self.tab_split.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.tab_extract.hide()
        self.tab_extract.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.tabs_frame.setLayout(self.tabs)
        self.tabs_frame.setFrameStyle(1)
        self.main_layout.addWidget(self.tabs_frame, 2, 0, 2, 5)

        # ----- save path -----
        self.save_path_wid = QGridLayout()
        savepath_label = QLabel("保存先: ")
        savepath_label.setAlignment(Qt.AlignRight)
        self.savepath_text = QLineEdit(f"{self.savepath}", self)
        self.savepath_text.setReadOnly(True)
        self.savepath_change_button = QPushButton("参照...", self)
        self.savepath_change_button.clicked.connect(self.saveFileDialog)
        self.save_path_wid.addWidget(savepath_label, 0, 0, 1, 1)
        self.save_path_wid.addWidget(self.savepath_text, 0, 1, 1, 2)
        self.save_path_wid.addWidget(self.savepath_change_button, 0, 3, 1, 1)
        self.main_layout.addLayout(self.save_path_wid, 4, 0, 1, 5)

        self.start_button = QPushButton('処理開始', self)
        self.start_button.clicked.connect(self.execFileEdit)
        self.start_button.setStyleSheet("font-weight: bold;")
        self.main_layout.addWidget(self.start_button, 5, 4, 1, 1)

        self.merger.toggled.connect(lambda: self.change_mode(0))
        self.spliter.toggled.connect(lambda: self.change_mode(1))
        self.extractor.toggled.connect(lambda: self.change_mode(2))

        self.merger.setChecked(True)

        # ----- display -----
        self.setLayout(self.main_layout)
        self.show()

    def validFileGet(self):
        if self.merger.isChecked():
            filenames = self.openFileNamesDialog()
            self.filenames = filenames if filenames else None
            self.filename = None
            self.addFileItems(filenames)
        else:
            filename = self.openFileNameDialog()
            self.filename = filename if filename else None
            self.filenames = None
            self.selected_file_box.setText(filename) if filename else None
    
    def execFileEdit(self):
        if self.merger.isChecked():
                savepath = os.path.join(self.savepath, ''.join(
                random.choices(string.ascii_letters + string.digits, k=8)) + '.pdf')
                self.filenames = [self.file_list.item(row).text() for row in range(self.file_list.count())]
                if self.filenames:
                    pdf_merger(self.filenames, savepath)
        else:
            savepath = os.path.join(self.savepath, ''.join(
                random.choices(string.ascii_letters + string.digits, k=8)))
            if self.filename:
                if self.spliter.isChecked():
                    pdf_spliter(self.filename, int(self.sp_start.text()), savepath)
                else:
                    pdf_extractor(self.filename, int(self.ex_start.text()),
                                  int(self.ex_end.text()), savepath + '.pdf')
                    
    def addFileItems(self, filenames):
        for file in filenames:
            item = QListWidgetItem()
            item.setText(file)
            self.file_list.addItem(item)
                    
    def deleteFileItems(self):
        selected = self.file_list.selectedItems()
        for file in selected:
            row = self.file_list.row(file)
            tfile = self.file_list.takeItem(row)
            # self.file_list.removeItemWidget(tfile)
            del tfile

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
        # fileName, _ = QFileDialog.getSaveFileName(
        #     self, "QFileDialog.getSaveFileName()", "", "Pdf file (*.pdf);;All Files (*)")
        dirname = QFileDialog.getExistingDirectory(
            self, "保存先フォルダを選択", self.savepath)
        if dirname:
            self.savepath = dirname
            self.savepath_text.setText(dirname)

    def change_mode(self, mode):
        if mode == 0:
            self.mode = 0
            self.tab_merge.show()
            self.tab_merge.setSizePolicy(
                QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.tab_split.hide()
            self.tab_split.setSizePolicy(
                QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.tab_extract.hide()
            self.tab_extract.setSizePolicy(
                QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.selected_file_box.hide()
            self.file_delete_button.show()
            self.file_delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        elif mode == 1:
            self.mode = 1
            self.tab_merge.hide()
            self.tab_merge.setSizePolicy(
                QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.tab_split.show()
            self.tab_split.setSizePolicy(
                QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.tab_extract.hide()
            self.tab_extract.setSizePolicy(
                QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.selected_file_box.show()
            self.file_delete_button.hide()
            self.file_delete_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        elif mode == 2:
            self.mode = 2
            self.tab_merge.hide()
            self.tab_merge.setSizePolicy(
                QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.tab_split.hide()
            self.tab_split.setSizePolicy(
                QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.tab_extract.show()
            self.tab_extract.setSizePolicy(
                QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.selected_file_box.show()
            self.file_delete_button.hide()
            self.file_delete_button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        else:
            raise Exception("Error: mode selection has bad value")