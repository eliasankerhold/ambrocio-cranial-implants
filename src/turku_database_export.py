from file_importer import FileImporter
from geometry_processor import GeometryProcessor

import os
from datetime import datetime

database_directory = os.path.join('C:\\', 'Users', 'Elias', 'Downloads', 'A0036-A0040')
export_directory = f'..{os.path.sep}exports'

file_ending_mask = '_clear.stl'

importer = FileImporter(import_dir=database_directory, export_dir=export_directory)

importer.scan_import_export_structure(mask=file_ending_mask)
importer.prepare_export_directories()

processor = GeometryProcessor(file_importer=importer)

start = datetime.now()
print(f"{start}: Started...")

for i, paths in enumerate(zip(importer.import_fpaths.values(), importer.export_fpaths.values())):
    import_path, export_path = paths
    print(f"\rProcessing {i + 1:3.0f}/{len(importer.import_fpaths.values())}...", end='')
    ms = processor.load_file(fpath=import_path)
    hull = processor.get_convex_hull(ms)
    processor.save_mesh(mesh=hull, fpath=export_path)

end = datetime.now()
duration = end - start
print('\nDone!')
print(f'{end}: Operation took {duration}, ({duration / len(importer.import_fpaths.values())} per file).')
