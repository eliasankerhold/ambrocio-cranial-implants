import rhinoscriptsyntax as rs
import scriptcontext as sc
import clr
import os
from datetime import datetime

db_path = os.path.join('C:\\', 'Users', 'ankerhe1', 'Downloads', 'skull_database')

def get_filepaths_from_folder(dpath):
    fpaths = []
    for dirpath, dirname, fname in os.walk(dpath):
        cleared_stls = [i for i in fname if i.endswith('_clear.stl')]
        if cleared_stls:
            fpaths.append(os.path.join(dirpath, cleared_stls[0]))
            
    
    print("Found " + str(len(fpaths)) + " files.")
    
    return fpaths
    
def reduce_mesh(mesh_id, reduced_polygon_count, accuracy = 4, threaded = True):
    mesh = rs.coercemesh(mesh_id)
    print("Reducing mesh to " + str(reduced_polygon_count) + " polygons...")
    success = mesh.Reduce(reduced_polygon_count, threaded, accuracy, False, True)
    if success:
        print("Success!")
        sc.doc.Objects.Replace(mesh_id, mesh)
        sc.doc.Views.Redraw()
    else:
        print("Unable to reduce mesh")
    
def import_files(fpaths, reduced_mesh = 200001):
    start = datetime.now()
    print(str(start) + ": Starting file import.")
    base_cmd = "Import "
    le = len(fpaths)
    for i, fpath in enumerate(fpaths):
        cmd = base_cmd + fpath
        rs.Command(cmd)
        name = os.path.basename(fpath).split(".")[0]
        rs.AddGroup(name)
        print("File " + str(i+1) + " of " + str(le) + " imported.")
        objs = rs.SelectedObjects()
        print("Found " + str(len(objs)) + " meshes.")
        for j, obj_id in enumerate(objs):
            reduce_mesh(obj_id, reduced_mesh)
            rs.ObjectName(obj_id, name + "_" + str(j))
        
        rs.AddObjectsToGroup(objs, name)
        rs.UnselectAllObjects()            
        print("File " + str(i+1) + " of " + str(le) + " processed.")
        
    print(str(datetime.now()) + ": File import and processing finished.")
    print("Total duration: " + str(datetime.now() - start))

fpaths = get_filepaths_from_folder(db_path)
import_files(fpaths)