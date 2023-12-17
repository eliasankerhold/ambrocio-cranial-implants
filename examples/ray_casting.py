from cranalyzer.geometry_processor import GeometryProcessor
from cranalyzer.file_importer import FileImporter
import numpy as np

import os
from datetime import datetime

processed_ref_skull_path = os.path.join('exports', 'reference_skull_prepared_smoothing.stl')

importer = FileImporter(import_dir='processed_skulls',
                        export_dir=f'exports')

importer.scan_import_export_structure()

gm = GeometryProcessor(file_importer=importer)

n_rays, an_rays = gm.prepare_ray_casting(ref_skull_path=processed_ref_skull_path)
hits = np.zeros(n_rays.shape[0])

start = datetime.now()
print(f'{start}: Started ray casting with {hits.shape[0] * 2} rays.')

for import_path, export_path in zip(importer.import_fpaths.values(), importer.export_fpaths.values()):
    print(f"\nProcessing {import_path}...")
    mesh = gm.load_file(fpath=import_path, library='open3d')
    hits += gm.do_ray_casting(intersect_mesh=mesh, normal_rays=n_rays, anti_normal_rays=an_rays, margin=300)

print(f'Done! Analysis took {datetime.now() - start}')

gm.export_ray_casting_result(ref_skull_path=processed_ref_skull_path, hits=hits,
                             export_path=os.path.join('exports', 'hits_db_01.csv'))
