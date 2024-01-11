from cranalyzer.geometry_processor import GeometryProcessor
from cranalyzer.file_importer import FileImporter
import numpy as np

import os
from datetime import datetime

processed_ref_skull_path = os.path.join('exports', 'reference_skull_prepared_smoothing_v2.stl')

importer = FileImporter(import_dir='processed_skulls',
                        export_dir=f'exports')

importer.scan_import_export_structure()

gm = GeometryProcessor(file_importer=importer)

n_rays, an_rays, triangle_areas, total_area = gm.prepare_ray_casting(ref_skull_path=processed_ref_skull_path)
hits = np.zeros(n_rays.shape[0])
defect_areas_per_model = np.zeros(len(importer.import_fpaths.values()))
hits_per_model = np.zeros_like(defect_areas_per_model)

start = datetime.now()
print(f'{start}: Started ray casting with {hits.shape[0] * 2} rays.')

for i, paths in enumerate(zip(importer.import_fpaths.values(), importer.export_fpaths.values())):
    import_path, export_path = paths
    print(f"\nProcessing {import_path}...")
    mesh = gm.load_file(fpath=import_path, library='open3d')
    hit, defect_areas_per_model[i], hits_per_model[i] = gm.do_ray_casting(intersect_mesh=mesh, normal_rays=n_rays,
                                                                          anti_normal_rays=an_rays,
                                                                          margin=50, triangle_areas=triangle_areas)
    hits += hit

print(f'Done! Analysis took {datetime.now() - start}')

gm.export_ray_casting_result(ref_skull_path=processed_ref_skull_path, total_hits=hits,
                             export_path=os.path.join('exports', 'MUG500_DB_only_left'), triangle_areas=triangle_areas,
                             hits_per_model=hits_per_model, defect_areas_per_model=defect_areas_per_model,
                             total_area=total_area, import_paths=importer.import_fpaths.values())
