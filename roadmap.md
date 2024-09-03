# Road map
The only current objective is the alpha release.

Expected features:
- loading and viewing a map
- reading, editing, writing dvd sections MISC BGND MOVE SGHT MASK BOND MAT LIFT BUIL and JUMP
- friendly GUI for editing
- writing empty SCRP, SCB, and animation-only ELEM, for mission tests
- changing map DVM



## Todo list
This table lists the main tasks to be carried out for the alpha release, roughly sorted by importance.

| Topic                                    | Description                                                                                                                                                                   |
|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Replace Qt geometry by shapely in model  | Replace QPolygonF, QLineF and QPoint by shapely object in model.<br/>Adapt pathfinder with new object.<br/>Remove monkey patch.                                               |
| Allow Drag and Drop in tree presentation | Implement D&D item in tree presentation.<br/>Add color for allowed/disallowed movement.<br/>Link item movement to model                                                       |
| Refactor adding item to the scene        | Change the strategy for adding elements to the scene:<br/> - add a shape of the element rather than the element itself<br/> - then add the element only on visibility request |
| Allow optional subinspector              | Not all objects always have all properties set.<br/>Optional SI allow to unset a property without invalid state.                                                              |
| BGND integration                         | Use BGND map filename to load DVM.<br/>Build minimap generation gui.                                                                                                          |
| Allow SGHT edition                       | Build vline dynamic graphic object (for sight, jump_area, rect ...)                                                                                                           |
| Allow multicolor geometric graphic       | Useful for SGHT, JUMP ...                                                                                                                                                     |
| Allow MASK edition                       | Build specific dynamic graphic object for mask edition                                                                                                                        |
| MAT integration                          | MAT section integration, model and gui.                                                                                                                                       |
| Refactor BUIL                            | Differentiating between building doors and special doors                                                                                                                      |
