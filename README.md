# shoeprint-analysis

> NAS Engineering Project (Semester 1 Final)

This program can analyze the prints made by 3D shoeprint models across different flex angles.
It can help determine the model of a shoe in a deformed print at an angle.

## Installation

1. install [pychrono](https://api.projectchrono.org/development/pychrono_installation.html).

2. clone this repository onto your computer

## Usage

1. Store cleaned prints in `data/objs`

### flexing

2. Change information in `flexer.py` to your desire

3. Run `python flexer.py` for each of your desired files and angles

    - It generates a .obj file named after the degrees in `/data/objs`

### simulating

4. Change the information in `test.py` to your desire

6. Run `python test.py` to run the simulation

    - The generated .csv file will appear in `/data/csvs/`

---

### visualizing (optional)

1. Install and open [ParaView](https://www.paraview.org/download/)

2. Open the .csv file with file > open

3. Press "apply"

4. Right-click the csv file on the left and select `add filter > alphabetical > Table To Points`

5. Select the TableToPoints1 node, change the x, y, and z columns to the proper ones, and press apply
    - if it didn't show up, you have to press the little eye icon next to the node

6. if you want to make a pretty elevation view, continue.

7. add a filter to TableToPoints called delaunay 2d

8. change projection plane mode to "best fit" and press apply

9. add a filter to delaunay2D1 called "elevation" and select "y axis", then press apply.

10. use the top bar to select the icon that says "-Y"