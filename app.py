import json
import sys
from pathlib import Path
from urllib import request

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton,
    QSplitter, QTextEdit, QToolBar, QVBoxLayout, QWidget
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "resources"
CONFIG = ROOT / "config.json"


def load_resources():
    items = []
    if not DATA.exists():
        return items
    for path in sorted(DATA.rglob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            item["_path"] = str(path)
            items.append(item)
        except Exception:
            pass
    return items


class AIDialog(QDialog):
    def __init__(self, parent, context=""):
        super().__init__(parent)
        self.setWindowTitle("Asistente IA")
        self.resize(760, 560)
        self.context = context
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Consulta"))
        self.prompt = QTextEdit()
        self.prompt.setPlaceholderText("Escribe qué quieres hacer con este recurso…")
        layout.addWidget(self.prompt)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        row = QHBoxLayout()
        self.key = QLineEdit()
        self.key.setPlaceholderText("API key de OpenAI (opcional: también puede guardarse en config.json)")
        self.key.setEchoMode(QLineEdit.Password)
        row.addWidget(self.key)
        go = QPushButton("Consultar")
        go.clicked.connect(self.ask)
        row.addWidget(go)
        layout.addLayout(row)

    def ask(self):
        key = self.key.text().strip()
        if not key:
            try:
                key = json.loads(CONFIG.read_text(encoding="utf-8")).get("api_key", "")
            except Exception:
                key = ""
        if not key:
            QMessageBox.warning(self, "Falta la API key", "Introduce una API key o configúrala en config.json.")
            return
        question = self.prompt.toPlainText().strip()
        if not question:
            return
        body = json.dumps({
            "model": "gpt-5.1",
            "input": [{"role": "user", "content": question + "\n\nRECURSO:\n" + self.context}],
        }).encode()
        req = request.Request(
            "https://api.openai.com/v1/responses",
            data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            with request.urlopen(req, timeout=90) as response:
                data = json.loads(response.read().decode("utf-8"))
            text = data.get("output_text", "")
            self.output.setPlainText(text or json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as exc:
            self.output.setPlainText(f"Error al consultar la IA:\n{exc}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IA Library")
        self.resize(1200, 760)
        self.resources = load_resources()
        self.filtered = self.resources[:]
        self.build_ui()
        self.refresh()

    def build_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        copy_action = QAction("Copiar", self)
        copy_action.triggered.connect(self.copy_content)
        toolbar.addAction(copy_action)
        ai_action = QAction("IA", self)
        ai_action.triggered.connect(self.open_ai)
        toolbar.addAction(ai_action)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar recursos…")
        self.search.textChanged.connect(self.refresh)
        layout.addWidget(self.search)
        split = QSplitter(Qt.Horizontal)
        layout.addWidget(split)

        self.list = QListWidget()
        self.list.currentItemChanged.connect(self.show_item)
        split.addWidget(self.list)

        right = QWidget()
        rlayout = QVBoxLayout(right)
        self.title = QLabel("Selecciona un recurso")
        self.title.setObjectName("title")
        rlayout.addWidget(self.title)
        self.editor = QTextEdit()
        rlayout.addWidget(self.editor)
        row = QHBoxLayout()
        save = QPushButton("Guardar cambios")
        save.clicked.connect(self.save_item)
        row.addWidget(save)
        ai = QPushButton("Trabajar con IA")
        ai.clicked.connect(self.open_ai)
        row.addWidget(ai)
        rlayout.addLayout(row)
        split.addWidget(right)
        split.setSizes([300, 900])

    def refresh(self):
        term = self.search.text().lower().strip()
        self.filtered = [r for r in self.resources if not term or term in json.dumps(r, ensure_ascii=False).lower()]
        self.list.clear()
        for resource in self.filtered:
            item = QListWidgetItem(resource.get("title", "Sin título"))
            item.setData(Qt.UserRole, resource)
            self.list.addItem(item)

    def show_item(self, current, previous=None):
        if not current:
            return
        r = current.data(Qt.UserRole)
        self.title.setText(r.get("title", "Sin título"))
        self.editor.setPlainText(r.get("content", ""))

    def save_item(self):
        item = self.list.currentItem()
        if not item:
            return
        r = item.data(Qt.UserRole)
        path = Path(r["_path"])
        r["content"] = self.editor.toPlainText()
        clean = {k: v for k, v in r.items() if not k.startswith("_")}
        path.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
        QMessageBox.information(self, "Guardado", "Recurso actualizado.")

    def copy_content(self):
        QApplication.clipboard().setText(self.editor.toPlainText())

    def open_ai(self):
        if not self.list.currentItem():
            context = self.editor.toPlainText()
        else:
            context = self.editor.toPlainText()
        AIDialog(self, context).exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget { font-size: 14px; }
        QMainWindow { background: #f5f6f8; }
        #title { font-size: 24px; font-weight: 600; padding: 8px 2px; }
        QLineEdit, QTextEdit, QListWidget { border: 1px solid #d5d9df; border-radius: 8px; padding: 7px; background: white; }
        QPushButton { padding: 8px 14px; border-radius: 7px; }
        QListWidget::item { padding: 9px; }
        QListWidget::item:selected { background: #e7edf7; color: #111; }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
