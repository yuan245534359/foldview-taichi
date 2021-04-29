import json
import taichi as ti 
import tina
import numpy as np
ti.init(arch=ti.gpu)

colors= []
all_polys=[]
all_edges= []
increments=0
num_face = 0
with open("traditionalcrane.fold") as fold_file:
    fold = json.load(fold_file)
    all_polys=[]
    edges_vex = fold["edges_vertices"]
    vertices_coords = []
    for frame in fold['file_frames']:
        polys = []
        edges = []
        vertices_coords = frame['vertices_coords']
        for face in fold['faces_vertices']:
            face_corrds = []
            for vertex in face:
                face_corrds.append(vertices_coords[vertex])
            polys.append(face_corrds)
        for edge in edges_vex:
            edge_corrds = []
            for vex in edge:
                edge_corrds.append(vertices_coords[vex])
            edges.append(edge_corrds)
        # input("continue..")
        all_polys.append(polys)
        all_edges.append(edges)
        colors = []
    for aa in fold['edges_assignment']:
        if aa=='B':
            colors.append('k')
        elif aa=='M':
            colors.append('r')
        elif aa=='V':
            colors.append('b')
        elif aa=='F':
            colors.append('y')
        else:
            colors.append('y')
        

metallic = tina.Param(float,initial=0.2)
roughness = tina.Param(float, initial= 0.5)
specular = tina.Param(float,initial= 0.5)
material = tina.PBR(metallic=metallic,roughness=roughness,specular=specular)
scene = tina.MeshNoCulling(tina.Scene())
mesh = tina.MeshNoCulling(tina.SimpleMesh())
scene.add_object(mesh,material)
gui = ti.GUI("foldViewer")
# scene.init_control(gui)
roughness.make_slider(gui, 'roughness')
metallic.make_slider(gui, 'metallic')
specular.make_slider(gui, 'specular')

percent = gui.slider("percent",0,99)

scene.lighting.clear_lights()
scene.lighting.add_light([-0.4, 1.5, 10.8], color=[0.8, 0.08, 0.8])
scene.lighting.add_light([-0.4, 1.5, -10.8], color=[0.08, 0.8, 0.8])
scene.lighting.add_light([-0.4, -11.5, 10.8], color=[0.8, 0.08, 0.8])
scene.lighting.set_ambient_light([0.3, 0.53, 0.3])

while gui.running and not gui.get_event(gui.ESCAPE):
    scene.input(gui)
    ii = int(len(all_polys)*percent.value/100)
    
    mesh.set_face_verts(np.array(all_polys[ii]))
    
    scene.render()
    gui.set_image(scene.img)
    gui.show()
