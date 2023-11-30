# Space_Engine
Simple space dynamic engine

This is an early alpha version, in future I will add more parameters and functions.

### How to add body to simulation
Due to the fact that this is not yet a finished program, most of the parameters are changed by changing the code or save files.

In order to get into the save file, you need to go to the "Saves" folder, then select the required file, or create your own. IMPORTANT, the file must be in the extension of JSON.

To add a planet, you must follow this syntax (you can copy and change it to the parameters you need).
<code>
    {"Position": [0, 0],
    "Vector": [0, 0],
    "Mass": 10000000000,
    "type": "star",
    "size": 10,
    "ID": "001"}
<code>