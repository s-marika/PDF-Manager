from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *


class MergeTab(QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        # 画面サイズを取得 (a.desktop()は QtWidgets.QDesktopWidget )
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


class SplitTab(QWidget):
    def __init__(self):
        super().__init__()


class ExtractorTab(QWidget):
    def __init__(self):
        super().__init__()
