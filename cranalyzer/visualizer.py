import plotly as po
import plotly_express as px
import pandas as pd


class CranialPlot:
    """
    Provides simple tools to visualize the results of ray casting analysis. All class variables can be easily retrieved
    and manipulated or integrated into other plots.
    """
    def __init__(self, hits_path: str, areas_path: str):
        self.hits_path = hits_path
        self.hits_results = pd.read_csv(hits_path)
        self.areas_path = areas_path
        self.areas_results = pd.read_csv(areas_path)
        self.mesh_plot = None
        self.fig = None

    def plot_area_histogram(self, bins: int = 20):
        fig = px.histogram(self.areas_results, x='abs_defect_area', nbins=bins)
        fig.show()

    def get_mesh_plot(self):
        """
        Generates a mesh plot of the given results file.

        :return: Mesh plot of the given results file with standard color map.
        :rtype: plotly.graph_objects.Mesh3d
        """
        result = self.hits_results
        self.mesh_plot = po.graph_objs.Mesh3d(x=result.x, y=result.y, z=result.z,
                                              i=result.i, j=result.j, k=result.k,
                                              intensitymode='cell', intensity=result.hits)

        return self.mesh_plot

    def get_figure(self):
        """
        Creates and returns the figure holding the mesh plot.

        :return: Figure holding the mesh plot.
        :rtype: plotly.graph_objects.Figure
        """
        assert self.mesh_plot is not None, "Generate mesh plot first."
        self.fig = po.graph_objs.Figure(data=[self.mesh_plot])
        camera = dict(eye=dict(x=-1.5, y=-2.5, z=1.25))
        self.fig.update_layout(scene_camera=camera)
        return self.fig

    def show_plot(self, save: bool = False, filename: str = None):
        """
        Shows and optionally saves the previously generated figure.

        :param save: Toggles export of the figure.
        :type save: bool
        :param filename: Path of the export file. Must end with .html extension.
        :type filename:
        """
        if save:
            assert filename is not None, "Filename is required for saving the figure."
            assert filename.endswith(".html"), "Filename must end with .html extension."
            self.fig.write_html(filename)
        self.fig.show()
