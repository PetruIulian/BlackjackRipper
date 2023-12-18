from modules.dialogs import startScreen, ask
from modules.strategyParse import parseStrategy
from modules.ai_model import start_ai
from modules.ui import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    # Start the UI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

