import sys
from World import *

def main():

    app = QApplication(sys.argv)
    world = World()
    world.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
