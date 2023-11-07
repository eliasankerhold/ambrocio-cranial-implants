import rhinoscriptsyntax as rs
import scriptcontext as sc
import clr
import os
from datetime import datetime

db_path = os.path.join('C:\\', 'Users', 'ankerhe1', 'Downloads', 'skull_database')


def get_filepaths_from_folder(dpath, mask):
    """ 
    Retrieves all files from subdirectories of main folder that end with mask.
    
    :param dpath: The path to the main database directory.
    :type dpath: str
    :param mask: Only files that end with this mask will be added.
    :type mask: str
    :return: List of full filepaths.
    :rtype: list[str]
    """

    fpaths = []
    for dirpath, dirname, fname in os.walk(dpath):
        cleared_stls = [i for i in fname if i.endswith(mask)]
        if cleared_stls:
            fpaths.append(os.path.join(dirpath, cleared_stls[0]))

    print("Found " + str(len(fpaths)) + " files.")

    return fpaths


def reduce_mesh(mesh_id, reduced_polygon_count, accuracy=4, threaded=True):
    """
    Reduces number of polygons of a mesh.
    
    :param mesh_id: GUID of mesh to reduce.
    :type mesh_id: Rhino.GUID
    :param reduced_polygon_count: Target number of polygons of reduced mesh.
    :type reduced_polygon_count: int
    :param accuracy: Accuracy of mesh reduction, between 1 (worst, fastest) and 10 (best, slowest)
    :type accuracy: int
    :param threaded: Toggles whether reduction should be computed in parallel.
    :param threaded: bool
    """

    mesh = rs.coercemesh(mesh_id)
    print("Reducing mesh to " + str(reduced_polygon_count) + " polygons...")
    success = mesh.Reduce(reduced_polygon_count, threaded, accuracy, False, True)
    if success:
        print("Success!")
        sc.doc.Objects.Replace(mesh_id, mesh)
        sc.doc.Views.Redraw()
    else:
        print("Unable to reduce mesh")


def import_files(fpaths, reduced_mesh=200001):
    """
    Imports all files in fpaths and processes them by reducing their mesh, renamind them and grouping all meshes from one file together.
    
    :param fpaths: List of all complete file paths.
    :type fpaths: list[str]
    :param reduced_mesh: Target number of polygons of reduced mesh. 
    :type reduce_mesh: int
    """

    start = datetime.now()
    print(str(start) + ": Starting file import.")
    base_cmd = "Import "
    le = len(fpaths)
    for i, fpath in enumerate(fpaths):
        cmd = base_cmd + fpath
        rs.Command(cmd)
        name = os.path.basename(fpath).split(".")[0]
        rs.AddGroup(name)
        print("File " + str(i + 1) + " of " + str(le) + " imported.")
        objs = rs.SelectedObjects()
        print("Found " + str(len(objs)) + " meshes.")
        for j, obj_id in enumerate(objs):
            reduce_mesh(obj_id, reduced_mesh)
            rs.ObjectName(obj_id, name + "_" + str(j))

        rs.AddObjectsToGroup(objs, name)
        rs.UnselectAllObjects()
        print("File " + str(i + 1) + " of " + str(le) + " processed.")

    print(str(datetime.now()) + ": File import and processing finished.")
    print("Total duration: " + str(datetime.now() - start))


fpaths = get_filepaths_from_folder(db_path, '_clear.stl')
import_files(fpaths)
