import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QScrollArea, \
    QTreeWidgetItemIterator, QSizePolicy


class MainWidget(QScrollArea):
    def __init__(self):
        super().__init__()
        # self.setGeometry(0, 0, 300, 300)
        # self.layout = QVBoxLayout()
        self.content = QWidget(self)
        self.layout = QVBoxLayout(self.content)
        # self.content_area.setWidgetResizable(True)

        # self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # content_layout.setSpacing(0)

        self.trees = []
        for i in range(2):
            self.trees.append(QTreeWidget())
            self.trees[-1].setHeaderHidden(True)
            for j in range(3):
                top_item = QTreeWidgetItem(self.trees[-1], [f"top{j}"])
                for k in range(10):
                    child_item = QTreeWidgetItem(top_item, [f"child{k}"])

        for tree in self.trees:
            tree.itemExpanded.connect(self.updateWindowSize)
            tree.itemCollapsed.connect(self.updateWindowSize)
            tree.setMinimumHeight(50)
            self.layout.addWidget(tree)
        # content_layout.addStretch()

        self.layout.addStretch()
        self.setWidgetResizable(True)
        self.setWidget(self.content)

        self.updateWindowSize()

    def updateWindowSize(self):
        # Calculer la taille minimale nécessaire pour chaque arbre
        for tree in self.trees:
            # treeSize = tree.viewportSizeHint()

            c = self.count_items(tree)
            w = tree.viewport().size().width()
            print(tree.sizeHintForRow(0))
            h = c * 18+2
            tree.setMinimumHeight(h)
            tree.setMaximumHeight(h)
            # tree.resize(w, h)



        # Redimensionner la fenêtre en fonction de la taille des arbres
        # self.setMinimumHeight(max(tree1Size, tree2Size))

    @staticmethod
    def count_items(tree):
        count = 0
        iterator = QTreeWidgetItemIterator(tree)
        while iterator.value():
            item = iterator.value()
            if item.parent():
                if item.parent().isExpanded():
                    count += 1
            else:
                count += 1
            iterator += 1
        return count


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWidget()
    mainWindow.show()
    sys.exit(app.exec())
