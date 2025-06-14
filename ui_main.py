import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton, QTextBrowser,
    QProgressBar, QTabWidget, QFileDialog, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from gemini_engine import generate_learning_plan, generate_chat_response
import markdown
import logging

class WorkerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args

    def run(self):
        result = self.fn(*self.args)
        self.finished.emit(result or "Error: no response")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SkillBuilder AI')
        self.resize(1200, 800)

        tabs = QTabWidget()
        tabs.addTab(self.build_learning_tab(), "Learning Plan")
        tabs.addTab(self.build_chat_tab(), "AI Coach")
        self.setCentralWidget(tabs)

    def build_learning_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)

        title = QLabel('📘 SkillBuilder AI')
        title.setFont(QFont('Segoe UI', 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form = QHBoxLayout()
        self.topic_input = QLineEdit(); self.topic_input.setPlaceholderText('Enter a topic')
        self.level_input = QComboBox(); self.level_input.addItems(['Beginner','Intermediate','Advanced'])
        self.weeks_input = QSpinBox(); self.weeks_input.setRange(1,52); self.weeks_input.setValue(6)
        self.lang_input = QComboBox(); self.lang_input.addItems(['English','Spanish','Urdu','Turkish'])
        gen_btn = QPushButton('🚀 Generate Plan'); gen_btn.clicked.connect(self.start_plan)

        form.addWidget(self.topic_input)
        form.addWidget(self.level_input)
        form.addWidget(self.weeks_input)
        form.addWidget(self.lang_input)
        form.addWidget(gen_btn)
        layout.addLayout(form)

        self.progress = QProgressBar(); self.progress.setRange(0,0); self.progress.hide()
        layout.addWidget(self.progress)

        self.plan_output = QTextBrowser()
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(self.plan_output)
        layout.addWidget(scroll)

        btn_layout = QHBoxLayout()
        copy_btn = QPushButton('📋 Copy'); copy_btn.clicked.connect(self.copy_plan)
        pdf_btn = QPushButton('📥 Save as PDF'); pdf_btn.clicked.connect(self.save_pdf)
        btn_layout.addWidget(copy_btn); btn_layout.addWidget(pdf_btn)
        layout.addLayout(btn_layout)

        return container

    def build_chat_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)

        self.chat_history = QTextBrowser()
        layout.addWidget(self.chat_history)

        box = QHBoxLayout()
        self.chat_input = QLineEdit(); self.chat_input.setPlaceholderText('Ask me anything...')
        send = QPushButton('Send'); send.clicked.connect(self.send_chat)
        box.addWidget(self.chat_input); box.addWidget(send)
        layout.addLayout(box)

        return container

    def start_plan(self):
        topic = self.topic_input.text().strip()
        if not topic:
            QMessageBox.warning(self, 'Input error', 'Please enter a topic.')
            return
        weeks = self.weeks_input.value()
        self.progress.show()
        self.thread = WorkerThread(
            generate_learning_plan,
            topic,
            self.level_input.currentText(),
            weeks,
            self.lang_input.currentText()
        )
        self.thread.finished.connect(lambda raw: self.show_plan(raw, weeks))
        self.thread.start()

    def show_plan(self, raw_text, weeks):
        self.progress.hide()
        # flow diagram
        flow = ' ➔ '.join(f'Week {i}' for i in range(1, weeks+1))
        flow_html = f'<div class="flow-diagram"><strong>Roadmap Flow:</strong> {flow}</div><hr>'
        # convert markdown to HTML
        md = markdown.Markdown(extensions=['extra'])
        plan_html = md.convert(raw_text)
        self.plan_output.setHtml(flow_html + plan_html)

    def copy_plan(self):
        QApplication.clipboard().setText(self.plan_output.toPlainText())
        QMessageBox.information(self, 'Copied', 'Learning plan copied to clipboard!')

    def save_pdf(self):
        fname, _ = QFileDialog.getSaveFileName(self, 'Save PDF', '', 'PDF Files (*.pdf)')
        if fname:
            from PyQt5.QtPrintSupport import QPrinter
            from PyQt5.QtGui import QTextDocument
            printer = QPrinter(); printer.setOutputFormat(QPrinter.PdfFormat); printer.setOutputFileName(fname)
            doc = QTextDocument(); doc.setHtml(self.plan_output.toHtml())
            doc.print_(printer)
            QMessageBox.information(self, 'Saved', f'Saved to {fname}')

    def send_chat(self):
        msg = self.chat_input.text().strip()
        if not msg:
            return
        self.chat_input.clear()
        self.chat_history.append(f'<span class="user"><b>You:</b> {msg}</span>')
        resp = generate_chat_response(msg, self.lang_input.currentText())
        self.chat_history.append(f'<span class="coach"><b>Coach:</b> {resp}</span>')