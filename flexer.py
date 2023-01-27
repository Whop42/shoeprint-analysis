import bpy
import os
import math

###########################
###########################
### CHANGE THESE VALUES ###

# flex degree in radians
flex_rads = -math.pi/3

# name of the file (automatically adds /data/objs/) (including .obj)
filename = "1.obj"

# console input for filename?
filename_input = False

# console input for angle (in degrees, will convert to radians)?
angle_input = False

# automatic mode: do all the files, all the angles (files cannot have -scan and must be .obj)
automatic_mode = True

flex_rads_automatic = [
    math.radians(15),
    math.radians(30),
    math.radians(45),
    math.radians(60),
    math.radians(70)
]

###########################
###########################
###########################

if filename_input:
    filename = input("filename? ")

if angle_input:
    flex_rads = math.radians(int(input("flex angle (degrees)? ")))

if not automatic_mode:
    flex_rads_automatic = [flex_rads]

## delicate code, don't break #############################################3

filepaths = [os.path.join("data", "objs", filename)]

if automatic_mode:
    for f in os.listdir(os.path.join("data", "objs")):
        if "scan" not in f and ".obj" in f and "empty" not in f:
            filepaths.append(os.path.join("data", "objs", f))

for filepath in filepaths:
    for flex_rads in flex_rads_automatic:
        print(filepath.replace(".obj", "") + "-" + str(math.ceil(math.degrees(flex_rads))) + ".obj")
        # remove cube
        # bpy.ops.object.select_all(action='DESELECT')
        # bpy.data.objects["Cube"].select_set(True)
        bpy.ops.object.delete()

        #import
        bpy.ops.import_scene.obj(filepath=filepath)

        print(bpy.data.objects)

        # bpy.ops.object.select_all(action='SELECT')

        obj = bpy.context.selected_objects[0]
        print(obj)

        # do flex

        flex_mod = obj.modifiers.new("flex", 'SIMPLE_DEFORM')
        flex_mod.deform_method = 'BEND'
        flex_mod.angle = -flex_rads

        # do rotate
        # obj.rotation_euler =   (-math.pi/4, # x rotation
        #                         0,       # y rotation
        #                         0)       # z rotation

        #export
        bpy.ops.export_scene.obj(filepath=filepath.replace(".obj", "") + "-" + str(math.ceil(math.degrees(flex_rads))) + ".obj", use_materials=False)