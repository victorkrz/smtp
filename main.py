from PyQt5.QtWidgets import *
from PyQt5 import uic
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

'''
WARNING! if you're using gmail, follow this guide before login:
https://support.google.com/accounts/answer/6010255?hl=en

for more info on the code, look for documentation on Python modules:
https://docs.python.org/3/library/email.html
https://docs.python.org/3/library/smtplib.html
'''


class MyGUI(QMainWindow):

	def __init__(self):
		super(MyGUI, self).__init__()
		uic.loadUi("GUI.ui", self)
		self.show()

		self.pushButton_login.clicked.connect(self.login)
		self.pushButton_attach.clicked.connect(self.attach_sth)
		self.pushButton_send_email.clicked.connect(self.send_mail)

	def login(self):
		try:
			self.server = smtplib.SMTP(self.lineEdit_smtp.text(), self.lineEdit_port.text())
			self.server.ehlo()
			self.server.starttls()
			self.server.ehlo()
			self.server.login(self.lineEdit_email.text(), self.lineEdit_password.text())

			self.lineEdit_email.setEnabled(False)
			self.lineEdit_password.setEnabled(False)
			self.lineEdit_smtp.setEnabled(False)
			self.lineEdit_port.setEnabled(False)
			self.pushButton_login.setEnabled(False)

			self.lineEdit_to.setEnabled(True)
			self.lineEdit_subject.setEnabled(True)
			self.textEdit.setEnabled(True)
			self.pushButton_attach.setEnabled(True)
			self.pushButton_send_email.setEnabled(True)

			self.msg = MIMEMultipart()

		except smtplib.SMTPAuthenticationError:
			message_box = QMessageBox()
			message_box.setText("Invalid login info.")
			message_box.exec()

		except:
			message_box = QMessageBox()
			message_box.setText("Login failed.")
			message_box.exec()

	def attach_sth(self):
		options = QFileDialog.Options()
		filenames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "All Files (*.*)", options=options)
		
		if filenames != []:
			for filename in filenames:
				attachment = open(filename, "rb")
				filename = filename[filename.rfind("/") + 1:]

				p = MIMEBase("application", "octet-stream")
				p.set_payload(attachment.read())
				encoders.encode_base64(p)
				p.add_header("Content-Disposition", f"attachment; filename={filename}")
				self.msg.attach(p)
				
				if not self.label_8.text().endswith(":"):
					self.label_8.setText(self.label_8.text() + ", ")
				self.label_8.setText(self.label_8.text() + " " + filename)

	def send_mail(self):
		dialog = QMessageBox()
		dialog.setText("Are you sure you want to send this email?")
		dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole)
		dialog.addButton(QPushButton("No"), QMessageBox.NoRole)

		if dialog.exec_() == 0:  # user chose yes
			try:
				self.msg["From"] = self.lineEdit_email.text()
				self.msg["To"] = self.lineEdit_to.text()
				self.msg["Subject"] = self.lineEdit_subject.text()
				self.msg.attach(MIMEText(self.textEdit.toPlainText(), "plain"))
				text = self.msg.as_string()
				self.server.sendmail(self.lineEdit_email.text(), self.lineEdit_to.text(), text)
				message_box = QMessageBox()
				message_box.setText("Mail sent!")
				message_box.exec()
			except:
				message_box = QMessageBox()
				message_box.setText("Sending mail failed!")
				message_box.exec()

app = QApplication([])
window = MyGUI()
app.exec_()
