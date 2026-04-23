"""
Application-wide context for ODVpy.

``AppContext`` is a module-level singleton that holds references to the
main runtime objects. It is populated by ``QWindow.set_widget()`` each
time a level is loaded or unloaded, and consumed by any widget that needs
cross-section access without explicit parameter threading.

Usage::

    from app_context import AppContext

    # write (QWindow)
    AppContext.level   = level
    AppContext.scene   = scene
    AppContext.tool_bar = tool_bar
    AppContext.control  = control

    # read (anywhere)
    section = AppContext.level.data["MOVE"]
    AppContext.scene.move_to(x, y)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal, QObject

if TYPE_CHECKING:
    from odv.level import Level
    from qt.scene import QScene
    from qt.scene_tool_bar import QSceneToolBar
    from qt.control.main_control import QControl


class _AppContext(QObject):
    """Singleton — access via the module-level ``AppContext`` instance."""

    level_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._level:    "Level | None"          = None
        self._scene:    "QScene | None"         = None
        self._tool_bar: "QSceneToolBar | None"  = None
        self._control:  "QControl | None"       = None

    # ------------------------------------------------------------------
    # properties
    # ------------------------------------------------------------------

    @property
    def level(self) -> "Level | None":
        # assert self._level is not None, "AppContext.level accessed before assignment"
        return self._level

    @level.setter
    def level(self, level: "Level | None") -> None:
        self._level = level
        self.level_changed.emit()
        print("[AppContext] Whole Level is set")

    @property
    def scene(self) -> "QScene":
        assert self._scene is not None, "AppContext.scene accessed before assignment"
        return self._scene

    # @scene.setter
    # def scene(self, scene: "QScene | None") -> None:
    #     self._scene = scene

    @property
    def tool_bar(self) -> "QSceneToolBar":
        assert self._tool_bar is not None, "AppContext.tool_bar accessed before assignment"
        return self._tool_bar

    # @tool_bar.setter
    # def tool_bar(self, tool_bar: "QSceneToolBar | None") -> None:
    #     self._tool_bar = tool_bar

    @property
    def control(self) -> "QControl":
        assert self._control is not None, "AppContext.control accessed before assignment"
        return self._control

    # @control.setter
    # def control(self, control: "QControl | None") -> None:
    #     self._control = control

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def set_ui(self, *, scene, tool_bar, control) -> None:
        """Assign all ui context objects at once)."""
        self._scene    = scene
        self._tool_bar = tool_bar
        self._control  = control



# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

AppContext = _AppContext()
