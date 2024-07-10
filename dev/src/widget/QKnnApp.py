from prof_utils.scatter_3d_viewer import QScatter3dViewer
from widget.QKnnControlPannel import QKnnControlPannel
from PySide6.QtWidgets import QHBoxLayout, QWidget

from __feature__ import snake_case, true_property

class QKnnApp(QWidget):
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent, )
            
        knn_data_display = QScatter3dViewer()
        knn_data_display.title = 'Knn data display'
        knn_data_display.axis_x.range = (0, 1.6)
        knn_data_display.axis_x.title = 'Isoperimetric Quotient'
        knn_data_display.axis_y.range = (0, 1)
        knn_data_display.axis_y.title = 'Centroid Area Ratio'
        knn_data_display.axis_z.range = (0, 1)
        knn_data_display.axis_z.title = 'Radius Min/Max Ratio'
        knn_control_panel = QKnnControlPannel(knn_data_display)

        app_layout = QHBoxLayout(self)
        app_layout.add_widget(knn_control_panel,1)
        app_layout.add_widget(knn_data_display, 4)
        
        