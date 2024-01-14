import os
from cranalyzer.visualizer import CranialPlot

hits_path = os.path.join('exports', 'FULL_DB_only_left_hits.csv')
areas_path = os.path.join('exports', 'FULL_DB_only_left_areas.csv')
export_path = os.path.join('exports', 'heatmap_db_full_left.html')

plotter = CranialPlot(hits_path=hits_path, areas_path=areas_path)

plotter.plot_area_histogram(bins=100)
plotter.get_mesh_plot()
plotter.get_figure()
plotter.show_plot(save=True, filename=export_path)
