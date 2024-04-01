from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QTreeWidget, QMainWindow, QScrollArea, QWidget, QVBoxLayout, \
    QLabel, QTreeWidgetItem, QSizePolicy

data = {"top1": ["child1", "child2", "child3", "child4", "child5", "child6", "child7", "child8", "child9"],
        "top2": ["child1", "child2", "child3", "child4", "child5", "child6", "child7", "child8", "child9"],
        "top3": ["child1", "child2", "child3", "child4", "child5", "child6", "child7", "child8", "child9"]}


class QResizableTree(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setMinimumHeight(0)
        # self.setMaximumHeight(0)
        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)

        self.title = QLabel(f"Label")
        self.layout.addWidget(self.title)

        self.tree = QTreeWidget(self)

        items = []
        for parent_item in data:
            item = QTreeWidgetItem([parent_item])
            for child_item in data[parent_item]:
                child = QTreeWidgetItem([child_item])
                item.addChild(child)
            items.append(item)
        self.tree.insertTopLevelItems(0, items)

        self.tree.itemExpanded.connect(self.up)
        self.tree.itemCollapsed.connect(self.up)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # self.tree.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        # self.setSizeAdjustPolicy(self.SizeAdjustPolicy.AdjustToContents)
        # self.tree.setSizeAdjustPolicy(self.tree.SizeAdjustPolicy.AdjustToContents)
        # self.tree.scroll
        # print(self.tree.sizeAdjustPolicy())

        self.layout.addWidget(self.tree)

        self.layout.addStretch()

        self.setWidgetResizable(True)

        self.setWidget(self.content)

        self.up()

    def up(self):
        m = self.tree.viewportSizeHint()
        m += QSize(2, 2)
        self.tree.resize(m)
        # self.tree.adjustSize()
        # self.adjustSize()
        pass
        # print(m)


class QWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Resizable tree')
        self.setGeometry(100, 100, 400, 200)

        self.setCentralWidget(QResizableTree(self))


if __name__ == '__main__':
    app = QApplication([])
    window = QWindow()
    window.show()
    app.exec()
