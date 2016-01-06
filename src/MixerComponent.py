#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/midi-remote-scripts/_APC/MixerComponent.py
from _Framework.ChannelStripComponent import ChannelStripComponent as ChannelStripComponentBase
from _Framework.MixerComponent import MixerComponent as MixerComponentBase
from .Logger import custom_log
TRACK_FOLD_DELAY = 5

class ChanStripComponent(ChannelStripComponentBase):
    """ Subclass of channel strip component using select button for (un)folding tracks """

    def __init__(self, *a, **k):
        super(ChanStripComponent, self).__init__(*a, **k)
        self._toggle_fold_ticks_delay = -1
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        super(ChanStripComponent, self).disconnect()

    def _select_value(self, value):
        super(ChanStripComponent, self)._select_value(value)
        if self.is_enabled() and self._track != None:
            if self._track.is_foldable and self._select_button.is_momentary() and value != 0:
                self._toggle_fold_ticks_delay = TRACK_FOLD_DELAY
            else:
                self._toggle_fold_ticks_delay = -1

    def _on_timer(self):
        if self.is_enabled() and self._track != None and self._toggle_fold_ticks_delay > -1:
            if not self._track.is_foldable:
                raise AssertionError
                if self._toggle_fold_ticks_delay == 0:
                    self._track.fold_state = not self._track.fold_state
                self._toggle_fold_ticks_delay -= 1

    def _on_current_monitoring_state_changed(self):
        custom_log("MixerComponent._on_current_monitoring_state_changed")

    def _track_has_monitoring_state(self, track):
        custom_log("MixerComponent._track_has_monitoring_state")
        return track is not None and track in self.song().tracks and not track.is_foldable and hasattr(track, "current_monitoring_state")

    def set_track(self, track):
        custom_log("MixerComponent.set_track")
        # Remove monitoring listener for old track
        if self._track_has_monitoring_state(self._track):
            custom_log("(old) track.name = " + self._track.name)
            self._track.remove_current_monitoring_state_listener(self._on_current_monitoring_state_changed)
        ChannelStripComponentBase.set_track(self, track)
        # Set monitoring listener for new track
        if self._track_has_monitoring_state(track):
            custom_log("(new) track.name = " + track.name)
            track.add_current_monitoring_state_listener(self._on_current_monitoring_state_changed)


class MixerComponent(MixerComponentBase):
    """ Special mixer class that uses return tracks alongside midi and audio tracks """

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return ChanStripComponent()