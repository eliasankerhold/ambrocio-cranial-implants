from geometry_processor import GeometryProcessor
from file_importer import FileImporter
import numpy as np

import os
from datetime import datetime

ref_skull_path = os.path.join('..', 'standard_skull', 'Standard_Skull_A0035_topOnly.stl')
processed_ref_skull_path = os.path.join('..', 'exports', 'reference_skull_prepared.stl')

importer = FileImporter(import_dir=os.path.join('..', 'ProcessedSkulls'),
                        export_dir=f'..{os.path.sep}exports')

importer.scan_import_export_structure()
# importer.prepare_export_directories()

gm = GeometryProcessor(file_importer=importer)
# gm.prepare_ref_skull(load_path=ref_skull_path, save_path=processed_ref_skull_path, cellsize=1, offset=50)

n_rays, an_rays = gm.prepare_ray_casting(ref_skull_path=processed_ref_skull_path)
hits = np.zeros(n_rays.shape[0])

start = datetime.now()
print(f'{start}: Started raycasting with {hits.shape[0] * 2} rays.')

for import_path, export_path in zip(importer.import_fpaths.values(), importer.export_fpaths.values()):
    print(f"\nProcessing {import_path}...")
    mesh = gm.load_file(fpath=import_path, library='open3d')
    hits += gm.do_ray_casting(intersect_mesh=mesh, normal_rays=n_rays, anti_normal_rays=an_rays, margin=10)

print(datetime.now() - start)
print('Done!')

gm.export_ray_casting_result(ref_skull_path=processed_ref_skull_path, hits=hits,
                             export_path=os.path.join('..', 'exports', 'hits.csv'))
