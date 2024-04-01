import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.tree1 = QTreeWidget()
        self.tree1.setHeaderHidden(True)
        self.populateTree(self.tree1, {"top1": ["child1", "child2", "child3", "child4", "child5", "child6", "child7", "child8", "child9"]})

        self.tree2 = QTreeWidget()
        self.tree2.setHeaderHidden(True)
        self.populateTree(self.tree2, {"top2": ["child1", "child2", "child3", "child4", "child5", "child6", "child7", "child8", "child9"]})

        self.layout.addWidget(self.tree1)
        self.layout.addWidget(self.tree2)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Redimensionner la fenêtre en fonction de la taille des arbres
        self.tree1.itemExpanded.connect(self.updateWindowSize)
        self.tree1.itemCollapsed.connect(self.updateWindowSize)
        self.tree2.itemExpanded.connect(self.updateWindowSize)
        self.tree2.itemCollapsed.connect(self.updateWindowSize)

        self.updateWindowSize()

    def populateTree(self, tree, data):
        for top, children in data.items():
            top_item = QTreeWidgetItem(tree, [top])
            for child in children:
                child_item = QTreeWidgetItem(top_item, [child])

    def updateWindowSize(self):
        # Calculer la taille minimale nécessaire pour chaque arbre
        tree1Size = self.tree1.sizeHintForColumn(0) + self.tree1.verticalScrollBar().sizeHint().width()
        tree2Size = self.tree2.sizeHintForColumn(0) + self.tree2.verticalScrollBar().sizeHint().width()

        # Redimensionner la fenêtre en fonction de la taille des arbres
        self.setMinimumHeight(max(tree1Size, tree2Size))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
