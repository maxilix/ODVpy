# Source - https://stackoverflow.com/a/65987818
# Posted by musicamante
# Retrieved 2026-04-09, License - CC BY-SA 4.0
from PyQt6.QtCore import QTimer, QSize, QRect, Qt, QEvent
from PyQt6.QtGui import QAction, QCursor, QPainter, QRegion, QPalette
from PyQt6.QtWidgets import QWidget, QMenu, QStyleOptionMenuItem, QStyleOptionFrame, QStyle, QApplication


class ScrollableMenu(QMenu):
    deltaY = 0
    dirty = True
    ignoreAutoScroll = False
    def __init__(self, *args, **kwargs):
        maxItemCount = kwargs.pop('maxItemCount', 0)
        super().__init__(*args, **kwargs)
        self._maximumHeight = self.maximumHeight()
        self._actionRects = []

        self.scrollTimer = QTimer(self, interval=50, singleShot=True, timeout=self.checkScroll)
        self.scrollTimer.setProperty('defaultInterval', 50)
        self.delayTimer = QTimer(self, interval=100, singleShot=True)

        self.setMaxItemCount(maxItemCount)

    @property
    def actionRects(self):
        if self.dirty or not self._actionRects:
            self._actionRects.clear()
            offset = self.offset()
            for action in self.actions():
                geo = super().actionGeometry(action)
                if offset:
                    geo.moveTop(geo.y() - offset)
                self._actionRects.append(geo)
            self.dirty = False
        return self._actionRects

    def iterActionRects(self):
        for action, rect in zip(self.actions(), self.actionRects):
            yield action, rect

    def setMaxItemCount(self, count):
        style = self.style()
        opt = QStyleOptionMenuItem()
        opt.initFrom(self)

        a = QAction('fake action', self)
        self.initStyleOption(opt, a)
        size = QSize()
        fm = self.fontMetrics()
        qfm = opt.fontMetrics
        size.setWidth(fm.boundingRect(QRect(), Qt.TextFlag.TextSingleLine, a.text()).width())
        size.setHeight(max(fm.height(), qfm.height()))
        self.defaultItemHeight = style.sizeFromContents(style.ContentsType.CT_MenuItem, opt, size, self).height()

        if not count:
            self.setMaximumHeight(self._maximumHeight)
        else:
            fw = style.pixelMetric(style.PixelMetric.PM_MenuPanelWidth, None, self)
            vmargin = style.pixelMetric(style.PixelMetric.PM_MenuHMargin, opt, self)
            scrollHeight = self.scrollHeight(style)
            self.setMaximumHeight(
                self.defaultItemHeight * count + (fw + vmargin + scrollHeight) * 2)
        self.dirty = True

    def scrollHeight(self, style):
        return style.pixelMetric(style.PixelMetric.PM_MenuScrollerHeight, None, self) * 2

    def isScrollable(self):
        return self.height() < super().sizeHint().height()

    def checkScroll(self):
        pos = self.mapFromGlobal(QCursor.pos())
        delta = max(2, int(self.defaultItemHeight * .25))
        if pos in self.scrollUpRect:
            delta *= -1
        elif pos not in self.scrollDownRect:
            return
        if self.scrollBy(delta):
            self.scrollTimer.start(self.scrollTimer.property('defaultInterval'))

    def offset(self):
        if self.isScrollable():
            return self.deltaY - self.scrollHeight(self.style())
        return 0

    def translatedActionGeometry(self, action):
        return self.actionRects[self.actions().index(action)]

    def ensureVisible(self, action):
        style = self.style()
        fw = style.pixelMetric(style.PixelMetric.PM_MenuPanelWidth, None, self)
        hmargin = style.pixelMetric(style.PixelMetric.PM_MenuHMargin, None, self)
        vmargin = style.pixelMetric(style.PixelMetric.PM_MenuVMargin, None, self)
        scrollHeight = self.scrollHeight(style)
        extent = fw + hmargin + vmargin + scrollHeight
        r = self.rect().adjusted(0, extent, 0, -extent)
        geo = self.translatedActionGeometry(action)
        if geo.top() < r.top():
            self.scrollBy(-(r.top() - geo.top()))
        elif geo.bottom() > r.bottom():
            self.scrollBy(geo.bottom() - r.bottom())

    def scrollBy(self, step):
        if step < 0:
            newDelta = max(0, self.deltaY + step)
            if newDelta == self.deltaY:
                return False
        elif step > 0:
            newDelta = self.deltaY + step
            style = self.style()
            scrollHeight = self.scrollHeight(style)
            bottom = self.height() - scrollHeight

            for lastAction in reversed(self.actions()):
                if lastAction.isVisible():
                    break
            lastBottom = self.actionGeometry(lastAction).bottom() - newDelta + scrollHeight
            if lastBottom < bottom:
                newDelta -= bottom - lastBottom
            if newDelta == self.deltaY:
                return False

        self.deltaY = newDelta
        self.dirty = True
        self.update()
        return True

    def actionAt(self, pos):
        for action, rect in self.iterActionRects():
            if pos in rect:
                return action

    # class methods reimplementation

    def sizeHint(self):
        hint = super().sizeHint()
        if hint.height() > self.maximumHeight():
            hint.setHeight(self.maximumHeight())
        return hint

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Show:
            if self.isScrollable() and self.deltaY:
                action = source.menuAction()
                self.ensureVisible(action)
                rect = self.translatedActionGeometry(action)
                delta = rect.topLeft() - self.actionGeometry(action).topLeft()
                source.move(source.pos() + delta)
            return False
        return super().eventFilter(source, event)

    def event(self, event):
        if not self.isScrollable():
            return super().event(event)
        if event.type() == QEvent.Type.KeyPress and event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down):
            res = super().event(event)
            action = self.activeAction()
            if action:
                self.ensureVisible(action)
                self.update()
            return res
        elif event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonDblClick):
            pos = event.pos()
            if pos in self.scrollUpRect or pos in self.scrollDownRect:
                if event.button() == Qt.MouseButton.LeftButton:
                    step = max(2, int(self.defaultItemHeight * .25))
                    if pos in self.scrollUpRect:
                        step *= -1
                    self.scrollBy(step)
                    self.scrollTimer.start(200)
                    self.ignoreAutoScroll = True
                return True
        elif event.type() == QEvent.Type.MouseButtonRelease:
            pos = event.pos()
            self.scrollTimer.stop()
            if not (pos in self.scrollUpRect or pos in self.scrollDownRect):
                action = self.actionAt(event.pos())
                if action:
                    action.trigger()
                    self.close()
            return True
        return super().event(event)

    def timerEvent(self, event):
        if not self.isScrollable():
            # ignore internal timer event for reopening popups
            super().timerEvent(event)

    def mouseMoveEvent(self, event):
        if not self.isScrollable():
            super().mouseMoveEvent(event)
            return

        pos = event.pos()
        if pos.y() < self.scrollUpRect.bottom() or pos.y() > self.scrollDownRect.top():
            if not self.ignoreAutoScroll and not self.scrollTimer.isActive():
                self.scrollTimer.start(200)
            return
        self.ignoreAutoScroll = False

        oldAction = self.activeAction()
        if not pos in self.rect():
            action = None
        else:
            y = event.pos().y()
            for action, rect in self.iterActionRects():
                if rect.y() <= y <= rect.y() + rect.height():
                    break
            else:
                action = None

        self.setActiveAction(action)
        if action and not action.isSeparator():
            def ensureVisible():
                self.delayTimer.timeout.disconnect()
                self.ensureVisible(action)
            try:
                self.delayTimer.disconnect()
            except:
                pass
            self.delayTimer.timeout.connect(ensureVisible)
            self.delayTimer.start(150)
        elif oldAction and oldAction.menu() and oldAction.menu().isVisible():
            def closeMenu():
                self.delayTimer.timeout.disconnect()
                oldAction.menu().hide()
            self.delayTimer.timeout.connect(closeMenu)
            self.delayTimer.start(50)
        self.update()

    def wheelEvent(self, event):
        if not self.isScrollable():
            return
        self.delayTimer.stop()
        if event.angleDelta().y() < 0:
            self.scrollBy(self.defaultItemHeight)
        else:
            self.scrollBy(-self.defaultItemHeight)

    def showEvent(self, event):
        if self.isScrollable():
            self.deltaY = 0
            self.dirty = True
            for action in self.actions():
                if action.menu():
                    action.menu().installEventFilter(self)
            self.ignoreAutoScroll = False
        super().showEvent(event)

    def hideEvent(self, event):
        for action in self.actions():
            if action.menu():
                action.menu().removeEventFilter(self)
        super().hideEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        style = self.style()
        # l, t, r, b = self.contentsMargins()
        m = self.contentsMargins()
        l = m.left()
        t = m.top()
        r = m.right()
        b = m.bottom()
        fw = style.pixelMetric(style.PixelMetric.PM_MenuPanelWidth, None, self)
        hmargin = style.pixelMetric(style.PixelMetric.PM_MenuHMargin, None, self)
        vmargin = style.pixelMetric(style.PixelMetric.PM_MenuVMargin, None, self)
        leftMargin = fw + hmargin + l
        topMargin = fw + vmargin + t
        bottomMargin = fw + vmargin + b
        contentWidth = self.width() - (fw + hmargin) * 2 - l - r

        scrollHeight = self.scrollHeight(style)
        self.scrollUpRect = QRect(leftMargin, topMargin, contentWidth, scrollHeight)
        self.scrollDownRect = QRect(leftMargin, self.height() - scrollHeight - bottomMargin,
            contentWidth, scrollHeight)

    def paintEvent(self, event):
        if not self.isScrollable():
            super().paintEvent(event)
            return

        style = self.style()
        qp = QPainter(self)
        rect = self.rect()
        emptyArea = QRegion(rect)

        menuOpt = QStyleOptionMenuItem()
        menuOpt.initFrom(self)
        menuOpt.state = style.StateFlag.State_None
        menuOpt.maxIconWidth = 0
        menuOpt.tabWidth = 0
        style.drawPrimitive(style.PrimitiveElement.PE_PanelMenu, menuOpt, qp, self)

        fw = style.pixelMetric(style.PixelMetric.PM_MenuPanelWidth, None, self)

        topEdge = self.scrollUpRect.bottom()
        bottomEdge = self.scrollDownRect.top()

        offset = self.offset()
        qp.save()
        qp.translate(0, -offset)
        # offset translation is required in order to allow correct fade animations
        for action, actionRect in self.iterActionRects():
            actionRect = self.translatedActionGeometry(action)
            if actionRect.bottom() < topEdge:
                continue
            if actionRect.top() > bottomEdge:
                continue

            visible = QRect(actionRect)
            if actionRect.bottom() > bottomEdge:
                visible.setBottom(bottomEdge)
            elif actionRect.top() < topEdge:
                visible.setTop(topEdge)
            visible = QRegion(visible.translated(0, offset))
            qp.setClipRegion(visible)
            emptyArea -= visible.translated(0, -offset)

            opt = QStyleOptionMenuItem()
            self.initStyleOption(opt, action)
            opt.rect = actionRect.translated(0, offset)
            style.drawControl(style.ControlElement.CE_MenuItem, opt, qp, self)
        qp.restore()

        cursor = self.mapFromGlobal(QCursor.pos())
        upData = (
            False, self.deltaY > 0, self.scrollUpRect
        )
        downData = (
            True, actionRect.bottom() - 2 > bottomEdge, self.scrollDownRect
        )

        for isDown, enabled, scrollRect in upData, downData:
            qp.setClipRect(scrollRect)

            scrollOpt = QStyleOptionMenuItem()
            scrollOpt.initFrom(self)
            scrollOpt.state = style.StateFlag.State_None
            scrollOpt.checkType = scrollOpt.checkType.NotCheckable
            scrollOpt.maxIconWidth = scrollOpt.tabWidth = 0
            scrollOpt.rect = scrollRect
            scrollOpt.menuItemType = scrollOpt.menuItemType.Scroller
            if enabled:
                if cursor in scrollRect:
                    frame = QStyleOptionMenuItem()
                    frame.initFrom(self)
                    frame.rect = scrollRect
                    frame.state |= style.StateFlag.State_Selected | style.StateFlag.State_Enabled
                    style.drawControl(style.ControlElement.CE_MenuItem, frame, qp, self)

                scrollOpt.state |= style.StateFlag.State_Enabled
                scrollOpt.palette.setCurrentColorGroup(QPalette.ColorGroup.Active)
            else:
                scrollOpt.palette.setCurrentColorGroup(QPalette.ColorGroup.Disabled)
            if isDown:
                scrollOpt.state |= style.StateFlag.State_DownArrow
            style.drawControl(style.ControlElement.CE_MenuScroller, scrollOpt, qp, self)

        if fw:
            borderReg = QRegion()
            borderReg |= QRegion(QRect(0, 0, fw, self.height()))
            borderReg |= QRegion(QRect(self.width() - fw, 0, fw, self.height()))
            borderReg |= QRegion(QRect(0, 0, self.width(), fw))
            borderReg |= QRegion(QRect(0, self.height() - fw, self.width(), fw))
            qp.setClipRegion(borderReg)
            emptyArea -= borderReg
            frame = QStyleOptionFrame()
            frame.rect = rect
            frame.palette = self.palette()
            frame.state = QStyle.StateFlag.State_None
            frame.lineWidth = style.pixelMetric(style.PixelMetric.PM_MenuPanelWidth)
            frame.midLineWidth = 0
            style.drawPrimitive(style.PrimitiveElement.PE_FrameMenu, frame, qp, self)

        qp.setClipRegion(emptyArea)
        menuOpt.state = style.StateFlag.State_None
        menuOpt.menuItemType = menuOpt.MenuItemType.EmptyArea
        menuOpt.checkType = menuOpt.CheckType.NotCheckable
        menuOpt.rect = menuOpt.menuRect = rect
        style.drawControl(style.ControlElement.CE_MenuEmptyArea, menuOpt, qp, self)


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.menu = ScrollableMenu(maxItemCount=5)
        self.menu.addAction('test action')
        for i in range(10):
            self.menu.addAction('Action {}'.format(i + 1))
            if i & 1:
                self.menu.addSeparator()
        subMenu = self.menu.addMenu('very long sub menu')
        subMenu.addAction('goodbye')

        self.menu.triggered.connect(self.menuTriggered)

    def menuTriggered(self, action):
        print(action.text())

    def contextMenuEvent(self, event):
        self.menu.exec(event.globalPos())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    test = Test()
    test.show()
    sys.exit(app.exec())
