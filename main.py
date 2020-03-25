import sys

from Runner import *
from Supermarket import *

def main():

    app = QApplication(sys.argv)
    a = Runner()
    #a.start_experiment()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
