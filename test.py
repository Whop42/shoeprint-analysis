# =============================================================================
# PROJECT CHRONO - http://projectchrono.org
#
# Copyright (c) 2014 projectchrono.org
# All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be found
# in the LICENSE file at the top level of the distribution and at
# http://projectchrono.org/license-chrono.txt.
#
# =============================================================================
# Authors: Radu Serban
# =============================================================================
# Demo of the SCM semi-empirical model for deformable soil
# =============================================================================

import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import pychrono.vehicle as veh
from PIL import Image
import numpy as np

import math

# The path to the Chrono data directory containing various assets (meshes, textures, data files)
# is automatically set, relative to the default location of this demo.
# If running from a different directory, you must change the path to the data directory with: 
#chrono.SetChronoDataPath('path/to/data')

# If true, use provided callback to change soil properties based on location
var_params = False

class MySoilParams (veh.SoilParametersCallback):
    def __init__(self):
        veh.SoilParametersCallback.__init__(self)
    def Set(self, loc, Kphi, Kc, n, coh, mu_angle, shear, K, R):
        Kphi_ = veh.doublep_value(Kphi)
        Kc_ = veh.doublep_value(Kc)
        n_ = veh.doublep_value(n)
        coh_ = veh.doublep_value(coh)
        mu_angle_ = veh.doublep_value(mu_angle)
        shear_ = veh.doublep_value(shear)
        K_ = veh.doublep_value(K)
        R_ = veh.doublep_value(R)
        if loc.y > 0 :
            Kphi_ = 0.2e6
            Kc_ = 0
            n_ = 1.1
            coh_ = 0
            mu_angle_ = 30
            shear_ = 0.01
            K_ = 4e7
            R_ = 3e4
        else:
            Kphi_ = 5301e3
            Kc_ = 102e3
            n_ = 0.793
            coh_ = 1.3e3
            mu_angle_ = 31.1
            shear_ = 1.2e-2
            K_ = 4e8
            R_ = 3e4
        veh.doublep_assign(Kphi, Kphi_)
        veh.doublep_assign(Kc, Kc_)
        veh.doublep_assign(n, n_)
        veh.doublep_assign(coh, coh_)
        veh.doublep_assign(mu_angle, mu_angle_)
        veh.doublep_assign(shear, shear_)
        veh.doublep_assign(K, K_)
        veh.doublep_assign(R, R_)
        

# Global parameters for tire
tire_rad = 0
tire_vel_z0 = -3
tire_center = chrono.ChVectorD(0, tire_rad, 0)
# tire_w0 = tire_vel_z0 / tire_rad

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
mesh.LoadWavefrontMesh("test-shoe.obj")
mesh.Transform(chrono.ChVectorD(0,0,0), chrono.ChMatrix33D(0.2)) #scale
mesh.Transform(chrono.ChVectorD(0,0,0), chrono.ChMatrix33D(-(math.pi), chrono.ChVectorD(1, 0, 0))) # rotate

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
my_params = MySoilParams()
if var_params:
    # Location-dependent soil properties
    terrain.RegisterSoilParametersCallback(my_params)
else :
    # Constant soil properties
    terrain.SetSoilParameters(2e6,  # Bekker Kphi
                               0,      # Bekker Kc
                               1.1,    # Bekker n exponent
                               0,      # Mohr cohesive limit (Pa)
                               30,     # Mohr friction limit (degrees)
                               0.01,   # Janosi shear coefficient (m)
                               2e8,    # Elastic stiffness (Pa/m), before plastic yield, must be > Kphi
                               3e4     # Damping (Pa s/m), proportional to negative vertical speed (optional)
    )

# Set terrain visualization mode
terrain.SetPlotType(veh.SCMDeformableTerrain.PLOT_PRESSURE_YELD, 0, 10000.2)
# ------------------------------------------
# Create the Irrlicht run-time visualization
# ------------------------------------------

vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(sys)
vis.SetWindowSize(1280,720)
vis.SetWindowTitle('Shoeprint Testing')
vis.Initialize()
# vis.AddLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
vis.AddSkyBox()
vis.AddCamera(chrono.ChVectorD(0.25,0.1,0), chrono.ChVectorD(0,0,0))
vis.AddTypicalLights()


# -------------------------------
# turn the terrain into a map png
# -------------------------------

def terrain_to_png(terrain: veh.SCMDeformableTerrain) -> None:
    mesh: chrono.ChTriangleMeshShape = terrain.GetMesh()
    mesh_mesh: chrono.ChTriangleMeshConnected = mesh.GetMesh()
    vertices: chrono.ChVectorD = mesh_mesh.m_vertices
    

    width_vertices = int(terrain_sizeX / terrain_delta)
    height_vertices = int(terrain_sizeY / terrain_delta)

    # print human readable information about the height and width vertices and the ratios between them
    count = 0
    heights = []
    for i in range(0,height_vertices):
        heights.append([])
        for j in range(0, width_vertices):
            loc: chrono.ChVectorD = vertices[((i-1)*j)+ j]
            height = loc.z
            count += 1
            heights[i].append(height)

    print(heights)
    print(count)
    print(count / (width_vertices * height_vertices))

    # normalize heights so that they are between 0 and 255
    max_height = max(max(heights))
    min_height = min(min(heights))
    for i in range(len(heights)):
        for j in range(len(heights[i])):
            heights[i][j] = int(255 * (heights[i][j] - min_height) / (max_height - min_height))
    print(heights)

    # turn heights into a grayscale image that is a heightmap
    img = Image.fromarray(np.uint8(heights), "L")
    img.show()
    

    img.save('terrain.png')


# ------------------
# Run the simulation
# ------------------

frames = 0

while vis.Run():
    if frames == 100:
        terrain_to_png(terrain)
        # exit()
        #terrain_to_png(terrain)
        body.SetCollide(False)
        vis_shape.SetVisible(False)
        mesh.Clear()
    
    
    vis.BeginScene()
    # vis.GetSceneManager().getActiveCamera().setTarget(chronoirr.vector3dfCH(body.GetPos()))
    vis.Render()

    plane: chrono.ChCoordsysD = terrain.GetPlane()
    

    vis.EndScene()
    sys.DoStepDynamics(0.002)
    frames += 1