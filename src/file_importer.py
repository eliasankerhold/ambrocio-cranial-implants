import os


class FileImporter:
    """
    Implements a toolset to scan database file structures and prepare export directories.

    :ivar import_dir: Base directory of the import database.
    :type import_dir: str
    :ivar export_dir: Base directory of the desired export database. Will be created if not exists.
    :type export_dir: str
    """

    def __init__(self, import_dir: str, export_dir: str):
        self.import_dir = import_dir
        self.export_dir = export_dir
        self.import_fpaths = {}
        self.export_fpaths = {}

    def scan_import_export_structure(self, mask: str = None, file_prefix: str = "PROCESSED"):
        """
        Retrieves all files from subdirectories of import folder that end with mask.

        :param file_prefix: Prefix that will be added to all exported files.
        :type file_prefix: str
        :param mask: Only files that end with this mask will be added.
        :type mask: str
        """

        fpaths = {}
        export_paths = {}
        for dirpath, _, fname in os.walk(self.import_dir):
            cleared_stls = [i for i in fname if mask is not None and i.endswith(mask)]
            if cleared_stls:
                dirpath_from_main_dir = dirpath.split(f'{self.import_dir}{os.path.sep}')[1]
                fpaths[cleared_stls[0]] = os.path.join(dirpath, cleared_stls[0])
                export_paths[cleared_stls[0]] = os.path.join(self.export_dir, dirpath_from_main_dir,
                                                             f"{file_prefix}_{cleared_stls[0]}")

        print("Found " + str(len(fpaths)) + " files.")

        self.import_fpaths = fpaths
        self.export_fpaths = export_paths

    def prepare_export_directories(self):
        """
        Creates all necessary subdirectories of the export directory.
        """

        i = 0
        for path in self.export_fpaths.values():
            dir = os.path.dirname(path)
            if not os.path.isdir(dir):
                os.makedirs(dir)
                i += 1

        print(f"Created {i:3.0f} directories.")



