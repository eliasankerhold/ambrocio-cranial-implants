import os
from cranalyzer.visualizer import CranialPlot

data_path = os.path.join('exports', 'hits_db_01.csv')
export_path = os.path.join('exports', 'heatmap_db_01.html')

plotter = CranialPlot(results_path=data_path)

plotter.get_mesh_plot()
plotter.get_figure()
plotter.show_plot(save=True, filename=export_path)
