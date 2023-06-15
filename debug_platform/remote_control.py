import XInput
from XInput import *
import _thread, time

MAX_POWER = 255
TURN_RATIO = 0.6


class remote_control():

    def __init__(self):


        self.last_keyboard_key = ""
        self.mode = "k"
        self.motors = [0, 0, 0, 0] #LF, RF, LB, RB
        self.__motors_old = [0, 0, 0, 0]
        _thread.start_new_thread(self.__polling_thread, ())
        self.__controller_connected_callback = None
        self.__controller_disconnected_callback = None
        self.__motor_data_ready_callback = None

    def motor_diff(self):
        a = self.motors
        b = self.__motors_old
        return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]) + abs(a[3]-b[3])

    def register_controller_connected_callback(self, callback):
        self.__controller_connected_callback = callback;

    def register_controller_disconnected_callback(self, callback):
        self.__controller_disconnected_callback = callback;

    def register_motor_data_ready_callback(self, callback):
        self.__motor_data_ready_callback = callback

    def __polling_thread(self):
        while(1):
            self.__motors_old = self.motors
            events = get_events()
            for event in events:
                if (event.type == XInput.EVENT_CONNECTED) and get_connected()[0]:
                    if (self.__controller_connected_callback != None):
                        self.__controller_connected_callback()

                if (event.type == XInput.EVENT_DISCONNECTED):
                    self.mode = "k"
                    if (self.__controller_disconnected_callback != None):
                        self.__controller_disconnected_callback()


            if self.mode == "k":
                if self.last_keyboard_key == "w":
                    self.motors = [MAX_POWER, MAX_POWER, 0, 0]
                elif self.last_keyboard_key == "s":
                    self.motors = [0, 0, MAX_POWER, MAX_POWER]
                elif self.last_keyboard_key == "a":
                    self.motors = [MAX_POWER, int(TURN_RATIO * MAX_POWER), 0, 0]
                elif self.last_keyboard_key == "d":
                    self.motors = [int(TURN_RATIO * MAX_POWER), MAX_POWER, 0, 0]
                else:
                    self.motors = [0, 0, 0, 0]
            elif self.mode == "c0":
                vals = get_button_values(get_state(0))
                if vals["LEFT_SHOULDER"]:
                    self.motors = [0, MAX_POWER, MAX_POWER, 0]
                elif vals["RIGHT_SHOULDER"]:
                    self.motors = [MAX_POWER, 0, 0, MAX_POWER]
                elif vals["DPAD_UP"]:
                    self.motors = [MAX_POWER, MAX_POWER, 0, 0]
                elif vals["DPAD_DOWN"]:
                    self.motors = [0, 0, MAX_POWER, MAX_POWER]
                elif vals["DPAD_LEFT"]:
                    self.motors = [MAX_POWER, int(TURN_RATIO * MAX_POWER), 0, 0]
                elif vals["DPAD_RIGHT"]:
                    self.motors = [int(TURN_RATIO * MAX_POWER), MAX_POWER, 0, 0]
                else:
                    thumbs = get_thumb_values(get_state(0))
                    triggers = get_trigger_values(get_state(0))
                    turn_ratio = 0.5 * (thumbs[0][0] + 1)
                    turn_ratio_bar = 0.5 * (-thumbs[0][0] + 1)
                    dir = triggers[1] - triggers[0]
                    self.motors = [int(max(dir * turn_ratio * MAX_POWER, 0)), int(max(dir * turn_ratio_bar * MAX_POWER, 0)), int(max(-dir * turn_ratio * MAX_POWER, 0)), int(max(-dir * turn_ratio_bar * MAX_POWER, 0))]
            if (self.__motor_data_ready_callback != None) and ((self.motor_diff() > 10) or (self.motors == [0,0,0,0])):
                self.__motor_data_ready_callback(self.motors)
            time.sleep(0.2)
