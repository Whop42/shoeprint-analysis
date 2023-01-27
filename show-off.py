import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import pychrono.vehicle as veh
# from PIL import Image
# import numpy as np
import os, sys
import math

###########################
###########################
### CHANGE THESE VALUES ###

# name of file in /data/objs/
filename = "5-60.obj"

# change this value until the mesh fits (after rotation)
mesh_scale = 0.17

# change this until the mesh is rotated properly (it's in radians)
mesh_rotation = math.pi

# the frame at which to end (don't give it time to jiggle around)
frame_stop = 105 # set this so it stops once the print solidly hits the terrain

# the degrees to rotate over flipping the print
# (for if you want it to not land in the middle of the print)
flip_extra = .15 * math.pi

# offset the mesh (sometimes you just can't be bothered to edit it again, yk)
offset = [ 0.01, 0, 0 ]

# automatic mode: do an entire folder (as long as they don't have "-scan")
automatic_mode = False

###########################
###########################
###########################

# create a heightmap in CSV form
def terrain_to_heightmap(terrain: veh.SCMDeformableTerrain) -> None:
    mesh: chrono.ChTriangleMeshShape = terrain.GetMesh()
    mesh_mesh: chrono.ChTriangleMeshConnected = mesh.GetMesh()
    vertices: chrono.ChVectorD = mesh_mesh.getCoordsVertices()
    
    csv = open(csv_path, "w")
    csv.flush()
    csv.write("x, y, z\n")
    for v in vertices:
        csv.write(f"{v.x}, {v.y}, {v.z}\n")
    csv.close()
    print(f"saved {csv_path}")

# ----------------------------
# Create the mechanical system
# ----------------------------

sys = chrono.ChSystemSMC()

# Create the ground
ground = chrono.ChBody()
ground.SetBodyFixed(True)
sys.Add(ground)

# Create the rigid body with contact mesh
body = chrono.ChBody()
sys.Add(body)
body.SetMass(100)
body.SetPos(chrono.ChVectorD(0, 0.2, 0))

# Load mesh
mesh = chrono.ChTriangleMeshConnected()
mesh.LoadWavefrontMesh(file_path)
mesh.Transform(chrono.ChVectorD(offset[0],offset[1],offset[2]), chrono.ChMatrix33D(mesh_scale)) # scale
mesh.Transform(chrono.ChVectorD(0,0,0), chrono.ChMatrix33D(-(math.pi) + flip_extra, chrono.ChVectorD(1, 0, 0))) # flip
mesh.Transform(chrono.ChVectorD(0,0,0), chrono.ChMatrix33D(mesh_rotation, chrono.ChVectorD(0, 1, 0))) # rotate

# Set visualization assets
vis_shape = chrono.ChTriangleMeshShape()
vis_shape.SetMesh(mesh)
# vis_shape.SetColor(chrono.ChColor(0.3, 0.3, 0.3))
vis_shape.SetWireframe(True)
body.AddVisualShape(vis_shape)

# Set collision shape
material = chrono.ChMaterialSurfaceSMC()

body.GetCollisionModel().ClearModel()
body.GetCollisionModel().AddTriangleMesh(material,                # contact material
                                        mesh,                    # the mesh 
                                        False,                   # is it static?
                                        False,                   # is it convex?
                                        chrono.ChVectorD(0,0,0), # position on body
                                        chrono.ChMatrix33D(1),   # orientation on body 
                                        0.01)                    # "thickness" for increased robustness
body.GetCollisionModel().BuildModel()
body.SetCollide(True)

terrain = veh.SCMDeformableTerrain(sys)
terrain.SetPlane(chrono.ChCoordsysD(chrono.ChVectorD(0,0,0), chrono.Q_from_AngX(-math.pi/2)))

terrain_sizeX = 0.3
terrain_sizeY = 0.75
terrain_delta = 0.007/2
terrain.Initialize(terrain_sizeX, terrain_sizeY, terrain_delta)

terrain.SetSoilParameters(2e6,      # Bekker Kphi
                            0,      # Bekker Kc
                            1.1,    # Bekker n exponent
                            1,      # Mohr cohesive limit (Pa)
                            5,      # Mohr friction limit (degrees)
                            0.1,    # Janosi shear coefficient (m)
                            2e9,    # Elastic stiffness (Pa/m), before plastic yield, must be > Kphi
                            3e4     # Damping (Pa s/m), proportional to negative vertical speed (optional)
    )

# Set terrain visualization mode
terrain.SetPlotType(veh.SCMDeformableTerrain.PLOT_PRESSURE_YELD, 0, 10000.2)

vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(sys)
vis.SetWindowSize(10,10)
vis.SetWindowTitle(filename)
vis.Initialize()
vis.AddSkyBox()
vis.AddCamera(chrono.ChVectorD(0.25,0.1,0), chrono.ChVectorD(0,0,0))
vis.AddTypicalLights()

frames = 0

while vis.Run():
    if frames == frame_stop:
        terrain_to_csv(terrain)
        # export_mesh(terrain)
        body.SetCollide(False)
        vis_shape.SetVisible(False)
        mesh.Clear()
        vis.GetGUIEnvironment()
        vis.Initialize()
        # break
    
    vis.BeginScene()

    vis.Render()

    plane: chrono.ChCoordsysD = terrain.GetPlane()
    

    vis.EndScene()
    sys.DoStepDynamics(0.002)
    frames += 1

