from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
import sys
import threading
import cv2

from my_module.K24098.lecture05_camera_image_capture import MyVideoCapture
from src.lecture05_01 import lecture05_01

class MainWindow(QMainWindow):
	def __init__(self):
		# メインウィンドウの作成
		super().__init__()
		self.setWindowTitle("背景加工アプリ")
		self.setGeometry(100, 100, 640, 600)
		central_widget = QWidget(self)
		layout = QVBoxLayout(central_widget)

		# タイトルラベル
		label = QLabel("背景加工アプリ", self)
		label.setAlignment(Qt.AlignCenter)
		layout.addWidget(label)

		# カメラ画像表示用ラベル
		self.image_label = QLabel(self)
		self.image_label.setFixedSize(640, 480)
		self.image_label.setAlignment(Qt.AlignCenter)
		layout.addWidget(self.image_label)

		# ボタン追加
		self.btn_camera = QPushButton("カメラ起動", self)
		self.btn_capture = QPushButton("画像撮影", self)
		self.btn_show_processed = QPushButton("加工後画像表示", self)

    # ボタンレイアウト
		layout.addWidget(self.btn_camera)
		layout.addWidget(self.btn_capture)
		layout.addWidget(self.btn_show_processed)

		self.setCentralWidget(central_widget)

		# ボタンのクリックイベント
		self.btn_camera.clicked.connect(self.camera_start)
		self.btn_capture.clicked.connect(self.capture_image)
		self.btn_show_processed.clicked.connect(self.show_image)

    # カメラのインスタンスを生成（Noneは未起動）
		self.camera = None
		# QTimerで周期的に呼び出す
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_frame)
		
  # カメラを起動する
	def camera_start(self):
		print("カメラ起動ボタンが押されました")
		if self.camera is None:
			self.camera = MyVideoCapture()
		self.timer.start(30)  # 30msごとにフレーム更新
		
  # 画像を撮影する
	def capture_image(self):
		print("画像撮影ボタンが押されました")
		if self.camera:
			self.camera.capture_image()
			self.timer.stop()

  # フレームを更新する
	def update_frame(self):
		if self.camera:
			ret, frame = self.camera.cap.read()
			if ret:
				# 加工（ターゲットマーク描画、左右反転）
				img = frame.copy()
				rows, cols, _ = img.shape
				center = (int(cols / 2), int(rows / 2))
				img = cv2.circle(img, center, 30, (0, 0, 255), 3)
				img = cv2.circle(img, center, 60, (0, 0, 255), 3)
				img = cv2.line(img, (center[0], center[1] - 80), (center[0], center[1] + 80), (0, 0, 255), 3)
				img = cv2.line(img, (center[0] - 80, center[1]), (center[0] + 80, center[1]), (0, 0, 255), 3)
				img = cv2.flip(img, flipCode=1)
				# OpenCV画像(numpy)→QImage→QPixmap
				rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
				h, w, ch = rgb_img.shape
				bytes_per_line = ch * w
				qt_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
				pixmap = QPixmap.fromImage(qt_img)
				self.image_label.setPixmap(pixmap)
	
  # 加工後の画像を表示する
	def show_image(self):
		print("加工後画像表示ボタンが押されました。")
		# 画像を加工する
		lecture05_01() 
		# 新規ウィンドウ(QDialog)で画像を表示
		img = cv2.imread('output_images/lecture05_01_k24098.png')
		if img is not None:
			rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			h, w, ch = rgb_img.shape
			bytes_per_line = ch * w
			qt_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
			pixmap = QPixmap.fromImage(qt_img)

			from PySide6.QtWidgets import QDialog, QVBoxLayout
			dialog = QDialog(self)
			dialog.setWindowTitle("加工後画像表示")
			dialog.resize(w, h)
			layout = QVBoxLayout(dialog)
			label = QLabel(dialog)
			label.setPixmap(pixmap)
			label.setAlignment(Qt.AlignCenter)
			layout.addWidget(label)
			dialog.exec()
		else:
			print("画像の読み込みに失敗しました。")

def app():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())