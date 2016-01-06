#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/midi-remote-scripts/_APC/MixerComponent.py
from _Framework.ChannelStripComponent import ChannelStripComponent as ChannelStripComponentBase
from _Framework.MixerComponent import MixerComponent as MixerComponentBase
from .Logger import custom_log
TRACK_FOLD_DELAY = 5

class ChanStripComponent(ChannelStripComponentBase):
    """ Subclass of channel strip component using select button for (un)folding tracks """

    def __init__(self, *a, **k):
        super(ChanStripComponent, self).__init__(*a, **k)
        #Register current_monitoring_state_button
        self._current_monitoring_state_button = None
        self._current_monitoring_state_pressed = False
        self._track_property_slots.append(self.register_slot(None, getattr(self, '_on_current_monitoring_state_changed'), 'current_monitoring_state'))
        self._current_monitoring_state_button_slot = self.register_slot(None, getattr(self,  '_current_monitoring_state_value'), 'value')

        self._toggle_fold_ticks_delay = -1
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        #Remove current_monitoring_state listener and references
        if self._current_monitoring_state_button != None:
            self._current_monitoring_state_button.reset()
        self._current_monitoring_state_button = None
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

    def update(self):
        super(ChannelStripComponentBase, self).update()
        if self._allow_updates:
            if self.is_enabled():
                self._empty_control_slots.disconnect()
                if self._track != None:
                    self._connect_parameters()
                else:
                    self._disconnect_parameters()
                self.on_selected_track_changed()
                self._on_mute_changed()
                self._on_solo_changed()
                self._on_current_monitoring_state_changed()
                self._on_arm_changed()
                self._on_cf_assign_changed()
            else:
                self._disconnect_parameters()
        else:
            self._update_requests += 1

    def _on_current_monitoring_state_changed(self):
        custom_log("ChanStripComponent._on_current_monitoring_state_changed")
        if self.is_enabled() and self._current_monitoring_state_button != None:
            if self._track != None or self.empty_color == None:
                if self._track in self.song().tracks and hasattr(self._track, 'current_monitoring_state') and self._track.current_monitoring_state == 0:
                    self._current_monitoring_state_button.turn_on()
                else:
                    self._current_monitoring_state_button.turn_off()
            else:
                self._current_monitoring_state_button.set_light(self.empty_color)

    def _track_has_monitoring_state(self, track):
        custom_log("ChanStripComponent._track_has_monitoring_state")
        return track is not None and track in self.song().tracks and not track.is_foldable and hasattr(track, "current_monitoring_state")

    def set_track(self, track):
        custom_log("ChanStripComponent.set_track")
        # Remove monitoring listener for old track
        # if self._track_has_monitoring_state(self._track):
            # custom_log("(old) track.name = " + self._track.name)
            # self._track.remove_current_monitoring_state_listener(self._on_current_monitoring_state_changed)
        if self._current_monitoring_state_button != None:
            self._current_monitoring_state_button.turn_off()    
        ChannelStripComponentBase.set_track(self, track)
        # Set monitoring listener for new track
        # if self._track_has_monitoring_state(track):
            # custom_log("(new) track.name = " + track.name)
            # track.add_current_monitoring_state_listener(self._on_current_monitoring_state_changed)

    def set_current_monitoring_state_button(self, button):
        custom_log("ChanStripComponent.set_current_monitoring_state_button")
        if button != self._current_monitoring_state_button:
            self.reset_button_on_exchange(self._current_monitoring_state_button)
            self._current_monitoring_state_pressed = False
            self._current_monitoring_state_button = button
            self._current_monitoring_state_button_slot.subject = button
            self.update()

    def current_monitoring_state_button_pressed(self):
        return self._current_monitoring_state_pressed

    def _current_monitoring_state_value(self, value):
        custom_log("ChanStripComponent._current_monitoring_state_value with value = " + str(value))


class MixerComponent(MixerComponentBase):
    """ Special mixer class that uses return tracks alongside midi and audio tracks """

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return ChanStripComponent()

    def set_current_monitoring_state_buttons(self, buttons):
        for strip, button in map(None, self._channel_strips, buttons or []):
            strip.set_current_monitoring_state_button(button)
