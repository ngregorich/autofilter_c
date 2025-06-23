from ableton.v2.control_surface import ControlSurface
from .AutoFilterController import AutoFilterController

class MyCustomSurface(ControlSurface):
    def __init__(self, c_instance):
        super().__init__(c_instance)
        self._autofilter = AutoFilterController(self)

    def disconnect(self):
        self._autofilter.disconnect()
        super().disconnect()
