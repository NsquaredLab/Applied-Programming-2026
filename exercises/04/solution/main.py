import sys

from PySide6.QtWidgets import QApplication

from views.mainView import MainView
from viewmodels.mainViewModel import MainViewModel

def main():
    app = QApplication(sys.argv)

    view_model = MainViewModel()
    view = MainView(view_model)
    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
