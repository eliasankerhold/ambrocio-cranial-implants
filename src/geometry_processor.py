import open3d as o3d
import pymeshlab as plm

from file_importer import FileImporter


class GeometryProcessor:
    """
    Provides tools to load geometries and process them. Reimplements even standard functions to provide flexibility
    towards the used library and easily changeable framework. PyMeshLab has superior performance in regard to file
    import and basic geometric computations, while Open3D offers more versatile functionalities. Some functions are
    implemented in both libraries, others are exclusive to either of them.

    :ivar file_importer: FileImporter object that holds the file lists as well as import and export structures.
    :type file_importer: FileImporter
    """

    def __init__(self, file_importer: FileImporter):
        self.file_importer = file_importer

    def load_file(self, library: str = 'pymeshlab', index: int = None, name: str = None, fpath: str = None):
        """
        Loads a triangle mesh using Open3D or pymeshlab libraries. File path can be specified directly, or by index or
        name with respect to FileImporter instance passed at initialization.

        :param library: Library to be used for file import.
        :type library: str
        :param index: Index of filepath in FileImporter import dictionary.
        :type index: int
        :param name: Key of filepath in FileImporter import dictionary.
        :type name: str
        :param fpath: Direct path to file.
        :type fpath: str
        :return: Opened file.
        :rtype: plm.MeshSet or o3d.geometry.TriangleMesh
        """
        assert index is not None or fpath is not None or name is not None, "Provide index, file path or name."
        assert library in ['pymeshlab', 'open3d']

        if library == 'open3d':
            func = o3d.io.read_triangle_mesh

        elif library == 'pymeshlab':
            def func(path: str):
                ms = plm.MeshSet()
                ms.load_new_mesh(path)
                return ms

        else:
            raise NotImplementedError

        if index is not None:
            try:
                return func(list(self.file_importer.import_fpaths.values())[index])

            except IndexError as ex:
                print('Could not import file!')
                print(ex)

        elif name is not None:
            try:
                return func(self.file_importer.import_fpaths[name])

            except KeyError as ex:
                print('Could not import file!')
                print(ex)

        elif fpath is not None:
            return func(fpath)

    @staticmethod
    def get_convex_hull(mesh_set: plm.MeshSet):
        """
        Generates convex hull using pymeshlab.

        :param mesh_set: MeshSet with loaded mesh.
        :type mesh_set: plm.MeshSet
        :return: Convex hull of input mesh.
        :rtype: plm.MeshSet
        """
        mesh_set.generate_convex_hull()
        return mesh_set

    def save_mesh(self, mesh, library: str = 'pymeshlab', index: int = None, name: str = None, fpath: str = None):
        """
        Saves a triangle mesh using Open3D or pymeshlab libraries. File path can be specified directly, or by index or
        name with respect to FileImporter instance passed at initialization.

        :param mesh: Mesh object to be saved.
        :type: mesh: plm.MeshSet or o3d.geometry.TriangleMesh
        :param library: Library to be used.
        :type library: str
        :param index: Index of filepath in FileImporter import dictionary.
        :type index: int
        :param name: Key of filepath in FileImporter import dictionary.
        :type name: str
        :param fpath: Direct path to file.
        :type fpath: str
        """

        assert index is not None or fpath is not None or name is not None, "Provide index, file path or name."
        assert library in ['pymeshlab', 'open3d']

        if library == 'open3d':
            def func(filename: str, mesh: o3d.geometry.TriangleMesh):
                o3d.io.write_triangle_mesh(filename=filename, mesh=mesh.compute_triangle_normals())

        elif library == 'pymeshlab':
            def func(filename: str, mesh: plm.MeshSet):
                mesh.save_current_mesh(file_name=filename)

        else:
            raise NotImplementedError

        if index is not None:
            try:
                return func(list(self.file_importer.import_fpaths.values())[index], mesh)

            except IndexError as ex:
                print('Could not import file!')
                print(ex)

        elif name is not None:
            try:
                return func(self.file_importer.import_fpaths[name], mesh)

            except KeyError as ex:
                print('Could not import file!')
                print(ex)

        elif fpath is not None:
            return func(fpath, mesh)
