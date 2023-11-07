from file_importer import FileImporter

import os

importer = FileImporter(import_dir=os.path.join('C:\\', 'Users', 'Elias', 'Downloads', 'A0036-A0040'),
                        export_dir=f'..{os.path.sep}exports')

importer.scan_import_export_structure(mask='_clear.stl')
print(importer.import_fpaths)
print(importer.export_fpaths)
importer.prepare_export_directories()

# def import_and_process(filepath: str):
#     ms = pml.MeshSet()
#     ms.load_new_mesh(filepath)
#     ms.generate_convex_hull()
#     ms.save_current_mesh('test.stl')
#
#
# db_path = os.path.join('C:\\', 'Users', 'Elias', 'Downloads', 'A0036-A0040')
#
# fpaths = get_filepaths_from_folder(db_path, '_clear.stl')
# import_and_process(fpaths[1])
#
# mesh = o3d.io.read_triangle_mesh('test.stl')
# mobb = mesh.get_oriented_bounding_box()
# triangle_mesh = o3d.geometry.TriangleMesh().create_from_oriented_bounding_box(obox=mobb)
# o3d.io.write_triangle_mesh(filename='mobb.stl', mesh=triangle_mesh.compute_triangle_normals())
