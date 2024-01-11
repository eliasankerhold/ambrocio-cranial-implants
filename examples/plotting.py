import os
from cranalyzer.visualizer import CranialPlot

hits_path = os.path.join('exports', 'MUG500_DB_only_left_hits.csv')
areas_path = os.path.join('exports', 'MUG500_DB_only_left_areas.csv')
export_path = os.path.join('exports', 'heatmap_db_mug500_left_normal.html')

plotter = CranialPlot(hits_path=hits_path, areas_path=areas_path)

plotter.plot_area_histogram()
plotter.get_mesh_plot()
plotter.get_figure()
plotter.show_plot(save=True, filename=export_path)
