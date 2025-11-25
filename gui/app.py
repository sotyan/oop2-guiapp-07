from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
	def __init__(self):
		# メインウィンドウの作成
		super().__init__()
		self.setWindowTitle("背景加工アプリ")
		self.setGeometry(100, 100, 300, 200)
		central_widget = QWidget(self)
		layout = QVBoxLayout(central_widget)

		# タイトルラベル
		label = QLabel("背景加工アプリ", self)
		label.setAlignment(Qt.AlignCenter)
		layout.addWidget(label)

		# ボタン追加
		# ボタンを押すと、画像撮影プログラムが呼び出される。（未実装）
		self.btn_camera = QPushButton("カメラ起動", self)
		self.btn_capture = QPushButton("画像撮影", self)
		self.btn_show_processed = QPushButton("加工後画像表示", self)

    # ボタンレイアウト
		layout.addWidget(self.btn_camera)
		layout.addWidget(self.btn_capture)
		layout.addWidget(self.btn_show_processed)

		self.setCentralWidget(central_widget)

def app():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())