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

###########################
###########################
###########################

if filename_input:
    filename = input("filename? ")

if angle_input:
    flex_rads = math.radians(int(input("flex angle (degrees)? ")))


## Don't touch past here unless you know what you're doing #############################################3

# remove cube
# bpy.ops.object.select_all(action='DESELECT')
# bpy.data.objects["Cube"].select_set(True)
bpy.ops.object.delete()

#import
filepath = os.path.join("data", "objs", filename)
bpy.ops.import_scene.obj(filepath=filepath)

print(bpy.data.objects)

# bpy.ops.object.select_all(action='SELECT')

obj = bpy.context.selected_objects[0]
print(obj)

# do flex

flex_mod = obj.modifiers.new("flex", 'SIMPLE_DEFORM')
flex_mod.deform_method = 'BEND'
flex_mod.angle = flex_rads

# do rotate
# obj.rotation_euler =   (-math.pi/4, # x rotation
#                         0,       # y rotation
#                         0)       # z rotation

#export
bpy.ops.export_scene.obj(filepath=filepath + str(math.ceil(math.degrees(flex_rads) - 1)) + ".obj", use_materials=False)