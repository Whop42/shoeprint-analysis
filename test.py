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
filename = "11.obj"

# change this value until the mesh fits (after rotation)
mesh_scale = 0.17

# change this until the mesh is rotated properly (it's in radians)
mesh_rotation = math.pi

# the frame at which to end (don't give it time to jiggle around)
frame_stop = 105 # set this so it stops once the print solidly hits the terrain

# the degrees to rotate over flipping the print
# (for if you want it to not land in the middle of the print)
flip_extra = 0*math.pi

# offset the mesh (sometimes you just can't be bothered to edit it again, yk)
offset = [0.02, 0, 0]

# automatic mode: do an entire folder (as long as they don't have "-scan")
automatic_mode = True

###########################
###########################
###########################

def normalize(value, _min, _max, norm_max):
    return int((value - _min) / (_max - _min) * norm_max if _max - _min > 0 else 0)

# -------------------------------
# turn the terrain into a map png
# -------------------------------

def terrain_to_png(terrain: veh.SCMDeformableTerrain) -> None:
    mesh: chrono.ChTriangleMeshShape = terrain.GetMesh()
    mesh_mesh: chrono.ChTriangleMeshConnected = mesh.GetMesh()
    vertices: chrono.ChVectorD = mesh_mesh.getCoordsVertices()
    
    # for v in vertices:
    #     print(f"{v.x}, {v.y}, {v.z}")

    # length of lists: width_vertices
    # number of lists: height_vertices

    # print(mesh_mesh.GetFileName())

    width_vertices = int(terrain_sizeX / terrain_delta)
    height_vertices = int(terrain_sizeY / terrain_delta)

    heights = []
    max_height = -100
    min_height = 100

    # while(len(vertices) > (width_vertices * height_vertices)):
        

    # vs = np.reshape(vertices, (width_vertices, height_vertices))

    # for i in vs:
    #     print(i.x)


    for i in range(0,height_vertices):
        heights.append([])
        for j in range(0, width_vertices):
            loc: chrono.ChVectorD = vertices[((i - 1) * j) + j]

            if loc.y > max_height:
                max_height = loc.y
            if loc.y < min_height:
                min_height = loc.y

            height = loc.y
            heights[i].append(height)


    # print(max_height)
    # print(min_height)

    # normalize the vertice coordinates to an image size
    mins = [min([i.x for i in vertices]), min([i.y for i in vertices]), max([i.z for i in vertices])]
    maxes = [max([i.x for i in vertices]), max([i.y for i in vertices]), max([i.z for i in vertices])]

    normed_vertices = []
    for vertex in vertices:
        nx = normalize(vertex.x, mins[0], maxes[0], terrain_sizeX * 1000)
        ny = normalize(vertex.y, mins[1], maxes[1], 255)
        nz = normalize(vertex.z, mins[2], maxes[2], terrain_sizeY * 1000)

        normed_vertices.append([nx, ny, nz])

    # print(normed_vertices)
    
    csv = open(csv_path, "w")
    csv.flush()
    csv.write("x, y, z\n")
    for v in vertices:
        csv.write(f"{v.x}, {v.y}, {v.z}\n")
    csv.close()
    print("saved csv")


    # final = []
    # # for i in range(0, int(maxes[0] * 1000)):
    # #     final.insert(i, [])

    # print(final)

    # for vertex in normed_vertices:
    #     # final[vertex[0]][vertex[2]] = vertex[1]
    #     final.insert(vertex[0], [])
    #     print(vertex[0])
    #     final[vertex[0]].insert(vertex[2], vertex[1])
    #     # for row in final:
    #     #     row.insert(vertex[2], vertex[1])
    # print(final)

    # # normalize heights so they are between 0 and 255
    # # for i in range(0, height_vertices):
    # #     for j in range(0, width_vertices):
    # #         heights[i][j] = (heights[i][j] - min_height) / (max_height - min_height) * 255

    # # turn heights into a grayscale image that is a heightmap
    # img = Image.fromarray(np.uint8(final), "L")
    # img.show()

    # img.save('terrain.png')

def export_mesh(terrain: veh.SCMDeformableTerrain):
    mesh: chrono.ChTriangleMeshShape = terrain.GetMesh()
    mesh_mesh: chrono.ChTriangleMeshConnected = mesh.GetMesh()
    # chrono.ChTriangleMeshConnected_WriteWavefront("terrain.obj", mesh_mesh)

    # print(type(chrono.vector_ChMesh(mesh_mesh)))
    mesh_mesh.WriteWavefront("terrain.obj", mesh_mesh)

base_path = "data"

filenames = [filename]

if automatic_mode:
    for f in os.listdir(os.path.join(base_path, "objs")):
        if not "scan" in f and f != filenames[0] and ".obj" in f and "empty" not in f:
            filenames.append(f)

for filename in filenames:
    print(">> starting " + filename)
    # filename = input(f"filename (in /{base_path}/objs/): ")
    file_path = os.path.join(base_path, "objs", filename)

    csv_path = os.path.join(base_path, "csvs", filename.replace(".obj", ".csv"))

    # The path to the Chrono data directory containing various assets (meshes, textures, data files)
    # is automatically set, relative to the default location of this demo.
    # If running from a different directory, you must change the path to the data directory with: 
    # chrono.SetChronoDataPath("data")     

    # Global parameters for tire
    tire_rad = 0
    tire_vel_z0 = -3
    tire_center = chrono.ChVectorD(0, tire_rad, 0)

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
    body.SetMass(50)
    body.SetPos(tire_center + chrono.ChVectorD(0, 0.2, 0))

    # Load mesh
    mesh = chrono.ChTriangleMeshConnected()
    mesh.LoadWavefrontMesh(file_path)
    mesh.Transform(chrono.ChVectorD(offset[0],offset[1],offset[2]), chrono.ChMatrix33D(mesh_scale)) # scale
    mesh.Transform(chrono.ChVectorD(0,0,0), chrono.ChMatrix33D(-(math.pi) + flip_extra, chrono.ChVectorD(1, 0, 0))) # flip
    mesh.Transform(chrono.ChVectorD(0,0,0), chrono.ChMatrix33D(mesh_rotation, chrono.ChVectorD(0, 1, 0)))

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

    # Create motor
    # motor = chrono.ChLinkMotorRotationAngle()
    # motor.SetSpindleConstraint(chrono.ChLinkMotorRotation.SpindleConstraint_OLDHAM)
    # motor.SetAngleFunction(chrono.ChFunction_Ramp(0, math.pi / 4))
    # motor.Initialize(body, ground, chrono.ChFrameD(tire_center, chrono.Q_from_AngY(math.pi/2)))
    # sys.Add(motor)

    # ------------------------
    # Create SCM terrain patch
    # ------------------------

    # Note that SCMDeformableTerrain uses a default ISO reference frame (Z up). Since the mechanism is modeled here in
    # a Y-up global frame, we rotate the terrain plane by -90 degrees about the X axis.
    terrain = veh.SCMDeformableTerrain(sys)
    terrain.SetPlane(chrono.ChCoordsysD(chrono.ChVectorD(0,0,0), chrono.Q_from_AngX(-math.pi/2)))

    terrain_sizeX = 0.3
    terrain_sizeY = 0.75
    terrain_delta = 0.007/2
    terrain.Initialize(terrain_sizeX, terrain_sizeY, terrain_delta)

    terrain.SetSoilParameters(2e6,      # Bekker Kphi
                                0,      # Bekker Kc
                                1.1,    # Bekker n exponent
                                0,      # Mohr cohesive limit (Pa)
                                30,     # Mohr friction limit (degrees)
                                0.01,   # Janosi shear coefficient (m)
                                2e9,    # Elastic stiffness (Pa/m), before plastic yield, must be > Kphi
                                3e4     # Damping (Pa s/m), proportional to negative vertical speed (optional)
        )

    # Set terrain visualization mode
    terrain.SetPlotType(veh.SCMDeformableTerrain.PLOT_PRESSURE_YELD, 0, 10000.2)

    # ------------------------------------------
    # Create the Irrlicht run-time visualization
    # ------------------------------------------

    vis = chronoirr.ChVisualSystemIrrlicht()
    vis.AttachSystem(sys)
    vis.SetWindowSize(10,10)
    vis.SetWindowTitle(filename)
    vis.Initialize()
    vis.AddSkyBox()
    vis.AddCamera(chrono.ChVectorD(0.25,0.1,0), chrono.ChVectorD(0,0,0))
    vis.AddTypicalLights()

    # ------------------
    # Run the simulation
    # ------------------

    frames = 0

    while vis.Run():
        if frames == frame_stop:
            terrain_to_png(terrain)
            # export_mesh(terrain)
            body.SetCollide(False)
            vis_shape.SetVisible(False)
            mesh.Clear()
            vis.GetGUIEnvironment()
            vis.Initialize()
            break
        
        vis.BeginScene()

        vis.Render()

        plane: chrono.ChCoordsysD = terrain.GetPlane()
        

        vis.EndScene()
        sys.DoStepDynamics(0.002)
        frames += 1
    
