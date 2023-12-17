import open3d as o3d
import pymeshlab as plm
import numpy as np
import pandas as pd

from .file_importer import FileImporter


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
    def prepare_ref_skull(load_path: str, save_path: str, cell_size: int, offset: int, convex_hull: bool = False):
        """
        Loads an STL file with the desired reference skull and prepares it for the analysis before saving it to the
        given location.

        :param load_path: Path of the STL file of the reference skull
        :type load_path: str
        :param save_path: Path of the prepared output file.
        :type save_path: str
        :param cell_size: Defines the size of one resampling voxel in percent of the model size.
        :type cell_size: int
        :param offset: Offset of the resampled model compared to its original.
        :type offset: int
        :param convex_hull: Toggles whether the convex hull of the reference skull should be used for the analysis.
        :type convex_hull:  bool
        """

        del_ids = []
        ms = plm.MeshSet()
        ms.load_new_mesh(load_path)
        print(f'Loaded reference skull {load_path}')
        del_ids.append(ms.current_mesh_id())
        if convex_hull:
            ms.generate_convex_hull()
            print('Computed convex hull')
            del_ids.append(ms.current_mesh_id())
        cell_size = plm.Percentage(cell_size)
        offset = plm.Percentage(offset)
        ms.generate_resampled_uniform_mesh(cellsize=cell_size, offset=offset, multisample=True)
        print(f'Resampled mesh with cell size={cell_size.value()} % and offset={offset.value()} %')
        for id in del_ids:
            ms.set_current_mesh(id)
            ms.delete_current_mesh()

        print('Deleted leftover meshes')
        ms.save_current_mesh(file_name=save_path)
        print(f'Saved processed reference skull to {save_path}')

    @staticmethod
    def prepare_ray_casting(ref_skull_path: str):
        """
        Prepare the ray casting procedure by loading the reference skull model and computing the ray tensors.

        :param ref_skull_path: Path to the reference skull, preferably prepared by prepare_reference_skull
        :type ref_skull_path: str
        :return: Two 6D-tensors of the normal and anti-normal rays, respectively. Tensors hold the origins and
            directions of the rays.
        :rtype: Tuple(o3d.core.Tensor, o3d.core.Tensor)
        """

        ref_skull = o3d.io.read_triangle_mesh(filename=ref_skull_path, enable_post_processing=True)
        ref_skull = ref_skull.compute_triangle_normals()
        vertices = np.asarray(ref_skull.vertices)
        normals = np.asarray(ref_skull.triangle_normals)
        triangles = np.asarray(ref_skull.triangles)
        triangles_coords = vertices[triangles]
        ray_origins = np.mean(triangles_coords, axis=1)
        normal_rays = o3d.core.Tensor(np.concatenate((ray_origins, normals), axis=1), dtype=o3d.core.Dtype.Float32)
        anti_normal_rays = o3d.core.Tensor(np.concatenate((ray_origins, -1 * normals), axis=1),
                                           dtype=o3d.core.Dtype.Float32)

        return normal_rays, anti_normal_rays

    @staticmethod
    def do_ray_casting(intersect_mesh: o3d.geometry.TriangleMesh, normal_rays: o3d.core.Tensor,
                       anti_normal_rays: o3d.core.Tensor, margin: float):
        """
        Computes the actual ray casting procedure of the intersect_mesh with the rays defined in the ray tensors.

        :param intersect_mesh: Model to be analyzed. The rays will be cast and intersected with this model.
        :type intersect_mesh: o3d.geometry.TriangleMesh
        :param normal_rays: Ray tensor of the rays along normal direction of the reference model.
        :type normal_rays: o3d.core.Tensor
        :param anti_normal_rays: Ray tensor of the rays along anti-normal direction of the reference model.
        :type anti_normal_rays: o3d.core.Tensor
        :param margin: The margin around the surface of the reference model in which intersections will be counted.
            If the absolute distance to the intersection is larger than margin, the ray will always be counted as
            missed.
        :type margin: float
        :return: Array of hits, each entry corresponding to a face of the reference model where the ray originated from.
        :rtype: numpy.ndarray
        """

        scene = o3d.t.geometry.RaycastingScene()
        scene.add_triangles(o3d.t.geometry.TriangleMesh.from_legacy(mesh_legacy=intersect_mesh))
        print(f'Added intersection mesh to scene')
        normal_cast = scene.cast_rays(normal_rays, nthreads=0)
        print(f'Casted normal rays')
        anti_normal_cast = scene.cast_rays(anti_normal_rays, nthreads=0)
        print(f'Casted anti-normal rays')

        n_dist, an_dist = normal_cast['t_hit'].numpy(), anti_normal_cast['t_hit'].numpy()
        n_mask = np.ma.masked_where(np.abs(n_dist) <= margin, n_dist).mask
        an_mask = np.ma.masked_where(np.abs(an_dist) <= margin, an_dist).mask
        print(f'Computed distance mask and hit counts')

        return np.logical_or(n_mask, an_mask).astype(int)

    @staticmethod
    def export_ray_casting_result(ref_skull_path, hits, export_path: str):
        """
        Exports the summarized result of the whole ray casting procedure into a csv file. Using common STL notation,
            the file contains the coordinates of the vertices, the face indices and the number of hits corresponding to
            each face.

        :param ref_skull_path: Path to the exact reference model used for the analysis.
        :type ref_skull_path: str
        :param hits: Array of hit counts as returned by the ray casting procedure.
        :type hits: numpy.ndarray
        :param export_path: Path to the csv file to be exported.
        :type export_path: str
        """

        ms = plm.MeshSet()
        ms.load_new_mesh(file_name=ref_skull_path)
        ref_skull = ms.current_mesh()
        pad_length = ref_skull.face_number() - ref_skull.vertex_number()
        vertices = ref_skull.vertex_matrix()
        triangles = ref_skull.face_matrix()
        padded_vertices = np.pad(vertices, pad_width=((0, pad_length), (0, 0)), constant_values=np.nan)

        export_df = pd.DataFrame({'x': padded_vertices[:, 0],
                                  'y': padded_vertices[:, 1],
                                  'z': padded_vertices[:, 2],
                                  'hits': hits,
                                  'i': triangles[:, 0],
                                  'j': triangles[:, 1],
                                  'k': triangles[:, 2]})

        export_df.to_csv(path_or_buf=export_path, index=False)
        print(f'Exported results to {export_path}')

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
