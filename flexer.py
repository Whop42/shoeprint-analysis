import bpy
import os
import math

# remove cube
# bpy.ops.object.select_all(action='DESELECT')
# bpy.data.objects["Cube"].select_set(True)
bpy.ops.object.delete()

#import
filepath = os.path.join("data", "objs", input("filename? "))
bpy.ops.import_scene.obj(filepath=filepath)

print(bpy.data.objects)

# bpy.ops.object.select_all(action='SELECT')

obj = bpy.context.selected_objects[0]
print(obj)

flex_rads = -math.pi/3

# do flex

flex_mod = obj.modifiers.new("flex", 'SIMPLE_DEFORM')
flex_mod.deform_method = 'BEND'
flex_mod.angle = flex_rads

# do rotate

obj.rotation_euler = (-flex_rads + math.pi/2, 0, 0)

#export
bpy.ops.export_scene.obj(filepath=filepath + str(math.ceil(math.degrees(flex_rads) - 1)) + ".obj", )