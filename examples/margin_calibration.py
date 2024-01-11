from cranalyzer.geometry_processor import GeometryProcessor
from cranalyzer.file_importer import FileImporter
import numpy as np
import matplotlib.pyplot as plt

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

calibration_model_indices = [0, 5, 10, 15, 20, 25]
calibration_model_fpaths = [list(importer.import_fpaths.values())[i] for i in calibration_model_indices]

steps = 200

margins = np.linspace(1, 200, steps)
areas = np.zeros((len(calibration_model_indices), margins.shape[0]))
hits = np.zeros((len(calibration_model_indices), margins.shape[0]))


for i, path in enumerate(calibration_model_fpaths):
    print(f"\nProcessing {path}...")
    mesh = gm.load_file(fpath=path, library='open3d')
    for k, marg in enumerate(margins):
        print(f'\r{k+1:3.0f} of {steps}', end='')
        _, areas[i, k], hits[i, k] = gm.do_ray_casting(intersect_mesh=mesh, normal_rays=n_rays,
                                                       anti_normal_rays=an_rays,
                                                       margin=marg, triangle_areas=triangle_areas, out=False)

    print('\n-------------')

print(f'Done! Analysis took {datetime.now() - start}')

fig, ax = plt.subplots(2, 1, sharex=True)
for i, path in enumerate(calibration_model_fpaths):
    ax[0].plot(margins, areas[i], label=os.path.basename(path))
    ax[0].set_ylabel('Defect area')
    ax[1].plot(margins, hits[i], label=path)
    ax[1].set_xlabel('Margin parameter')
    ax[1].set_ylabel('Number of hits')
    fig.suptitle('Margin Calibration')
    ax[0].legend()
    ax[0].set_yscale('log')
    ax[1].set_yscale('log')


fig.savefig('calibration.pdf')

plt.show()
