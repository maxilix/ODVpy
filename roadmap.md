# Road map
The only current objective is the alpha release.

Expected features:
- loading and viewing a map
- reading, editing, writing dvd sections MISC BGND MOVE SGHT MASK BOND MAT LIFT BUIL and JUMP
- friendly GUI for editing
- writing empty SCRP, SCB, and animation-only ELEM, for mission tests
- changing map DVM



## Todo list
- Allow tree reorganization.
  - Implement "move to" action in inspector submenu.
  - Implement Drag'n'Drop item in tree presentation.
    - Add color for allowed/disallowed movement.
    - Link to the "move to" action.
  - Link reorganization to the model.
- Refactor adding item to the scene.
  - Change the strategy for adding elements to the scene.
  - Add a shape of the element rather than the element itself.
  - Then add the element only on visibility request.
- Allow optional subinspector.
  - Not all objects always have all properties set.
  - Optional subinspector allow to unset a property without invalid state.
  - Implement a section-wide invalid state.
- BGND integration.
  - Use BGND map filename to load DVM.
  - Build minimap generation GUI.
- Allow MASK edition
  - Build specific dynamic graphic object for mask edition
- Allow SGHT edition.
  - Build vline dynamic graphic element (for sight, jump_area, rect ...).
  - Allow multicolor geometric graphic (useful for SGHT, JUMP, MASK ...).
- MAT integration
  - MAT section integration, model and GUI.
- Refactor BUIL
  - Differentiating between building doors and special doors



## Long term features

- Replace Qt geometry by shapely in model.
    - Replace QPolygonF, QLineF and QPoint by shapely object in model.
    - Adapt pathfinder with new object.
    - Remove monkey patch.
- Undo/Redo stack
