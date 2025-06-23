from ableton.v2.control_surface import ControlSurface
from ableton.v2.control_surface import MIDI_NOTE_TYPE, MIDI_CC_TYPE
from ableton.v2.control_surface.input_control_element import MIDI_CC_TYPE
from ableton.v2.base import listens

class AutoFilterController(ControlSurface):
    def __init__(self, c_instance):
        super(AutoFilterController, self).__init__(c_instance)
        self._autofilters = []
        self._current_index = 0
        self._selected_parameter = None

        self._collect_autofilters()

        self._cutoff_control = self._create_midi_input_control(cc=0, channel=0)
        self._cutoff_control.add_value_listener(self._on_cutoff_change)

        self._button_control = self._create_midi_input_control(cc=1, channel=0)
        self._button_control.add_value_listener(self._on_button_press)

    def _create_midi_input_control(self, cc, channel):
        return self._control_surface()._c_instance.get_control_input(
            is_momentary=True,
            msg_type=MIDI_CC_TYPE,
            channel=channel,
            identifier=cc
        )

    def _collect_autofilters(self):
        self._autofilters = []
        for track in self.song.tracks:
            if track.devices:
                for device in track.devices:
                    if device.name == 'Auto Filter' or 'Auto Filter' in device.class_display_name:
                        self._autofilters.append(device)
        self._select_autofilter(0)

    def _select_autofilter(self, index):
        if not self._autofilters:
            self._selected_parameter = None
            return
        self._current_index = index % len(self._autofilters)
        device = self._autofilters[self._current_index]
        for param in device.parameters:
            if param.name in ('Frequency', 'Freq', 'Cutoff'):
                self._selected_parameter = param
                break

    def _on_cutoff_change(self, value):
        if self._selected_parameter:
            scaled = float(value) / 127.0
            param_range = self._selected_parameter.max - self._selected_parameter.min
            self._selected_parameter.value = self._selected_parameter.min + param_range * scaled

    def _on_button_press(self, value):
        if value > 0:
            self._select_autofilter(self._current_index + 1)

    def disconnect(self):
        super(AutoFilterController, self).disconnect()
        if self._cutoff_control:
            self._cutoff_control.remove_value_listener(self._on_cutoff_change)
        if self._button_control:
            self._button_control.remove_value_listener(self._on_button_press)
