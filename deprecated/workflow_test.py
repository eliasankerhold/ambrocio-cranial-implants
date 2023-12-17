from cranalyzer.file_importer import FileImporter
from cranalyzer.geometry_processor import GeometryProcessor

import os
from datetime import datetime

importer = FileImporter(import_dir=os.path.join('C:\\', 'Users', 'Elias', 'Downloads', 'A0036-A0040'),
                        export_dir=f'..{os.path.sep}exports')

importer.scan_import_export_structure(mask='_clear.stl')
importer.prepare_export_directories()

processor = GeometryProcessor(file_importer=importer)

start = datetime.now()

for import_path, export_path in zip(importer.import_fpaths.values(), importer.export_fpaths.values()):
    print(f"Processing {import_path}...")
    ms = processor.load_file(fpath=import_path)
    hull = processor.get_convex_hull(ms)
    processor.save_mesh(mesh=hull, fpath=export_path)
    print(f"Saved to {export_path}\n")

print(datetime.now() - start)
print('Done!')

#
# mesh = o3d.io.read_triangle_mesh('test.stl')
# mobb = mesh.get_oriented_bounding_box()
# triangle_mesh = o3d.geometry.TriangleMesh().create_from_oriented_bounding_box(obox=mobb)
# o3d.io.write_triangle_mesh(filename='mobb.stl', mesh=triangle_mesh.compute_triangle_normals())
