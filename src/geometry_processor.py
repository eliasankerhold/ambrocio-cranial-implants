import open3d as o3d
from file_importer import FileImporter


class GeometryProcesser:
    """
    Provides tools to load geometries and process them. Reimplements even standard functions to provide flexibility
    towards the used library and easily changeable framework.
    :ivar file_importer: FileImporter object that holds the file lists as well as import and export structures.
    :type file_importer: FileImporter
    """

    def __init__(self, file_importer: FileImporter):
        self.file_importer = file_importer

    def load_file(self, fpath: str):
