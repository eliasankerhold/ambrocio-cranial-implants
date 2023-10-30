import rhinoscriptsyntax as rs
import os, sys

db_path = os.path.join('C:\\', 'Users', 'ankerhe1', 'Downloads', 'skull_database')

def get_filepaths_from_folder(dpath):
    fpaths = []
    for dirpath, dirname, fname in os.walk(dpath):
        cleared_stls = [i for i in fname if i.endswith('_clear.stl')]
        if cleared_stls:
            fpaths.append(os.path.join(dirpath, cleared_stls[0]))
            
    
    print("Found " + str(len(fpaths)) + " files.")
    
    return fpaths
    
def import_files(fpaths):
    base_cmd = "Import "
    le = len(fpaths)
    for i, fpath in enumerate(fpaths):
        cmd = base_cmd + fpath
        rs.Command(cmd)
        print("File " + str(i+1) + " of " + str(le) + " imported.")

fpaths = get_filepaths_from_folder(db_path)
import_files(fpaths)