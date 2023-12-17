from cranalyzer.geometry_processor import GeometryProcessor
from cranalyzer.file_importer import FileImporter

import os

ref_skull_path = os.path.join('standard_skull', 'Standard_Skull_A0035_topOnly_flattened_smoothed.stl')
processed_ref_skull_path = os.path.join('exports', 'reference_skull_prepared_smoothing.stl')

importer = FileImporter(import_dir='ProcessedSkulls',
                        export_dir=f'exports')

importer.scan_import_export_structure()

gm = GeometryProcessor(file_importer=importer)
gm.prepare_ref_skull(load_path=ref_skull_path, save_path=processed_ref_skull_path, cell_size=1, offset=50)
