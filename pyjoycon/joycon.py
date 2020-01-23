import hid
import time
import threading
import pyjoycon.device as d

class JoyCon:
    VENDOR_ID = 0x057E
    L_PRODUCT_ID = 0x2006
    R_PRODUCT_ID = 0x2007
    _L_ACCEL_OFFSET_X = 350
    _L_ACCEL_OFFSET_Y = 0
    _L_ACCEL_OFFSET_Z = 4081
    _R_ACCEL_OFFSET_X = 350
    _R_ACCEL_OFFSET_Y = 0
    _R_ACCEL_OFFSET_Z = -4081

    _INPUT_REPORT_SIZE = 49
    _INPUT_REPORT_FREQ = 1.0 / 60.0
    _RUMBLE_DATA = b'\x00\x01\x40\x40\x00\x01\x40\x40'

    def __init__(self, vendor_id, product_id):
        if vendor_id != self.VENDOR_ID:
            raise ValueError('vendor_id is invalid')

        if product_id not in [self.L_PRODUCT_ID, self.R_PRODUCT_ID]:
            raise ValueError('product_id is invalid')

        self._joycon_device = self._open(vendor_id, product_id)
        self._PRODUCT_ID = product_id
        self._packet_number = 0
        self._setup_sensors()

        self._input_report = bytes(self._INPUT_REPORT_SIZE)
        self._update_input_report_thread = threading.Thread(
            target=self._update_input_report)
        self._update_input_report_thread.setDaemon(True)
        self._update_input_report_thread.start()

    def _open(self, vendor_id, product_id):
        _joycon_device = hid.device()
        try:
            _joycon_device.open(vendor_id, product_id)
        except IOError:
            raise IOError('joycon connect failed')
        return _joycon_device

    def _close(self):
        self._joycon_device.close()

    def _read_input_report(self):
        return self._joycon_device.read(self._INPUT_REPORT_SIZE)

    def _write_output_report(self, command, subcommand, argument):
        self._joycon_device.write(command
                                  + self._packet_number.to_bytes(1, byteorder='big')
                                  + self._RUMBLE_DATA
                                  + subcommand
                                  + argument)
        self._packet_number = (self._packet_number + 1) & 0xF

    def _update_input_report(self):
        while True:
            self._input_report = self._read_input_report()

    def _setup_sensors(self):
        # Enable 6 axis sensors
        self._write_output_report(b'\x01', b'\x40', b'\x01')
        # It needs delta time to update the setting
        time.sleep(0.02)
        # Change format of input report
        self._write_output_report(b'\x01', b'\x03', b'\x30')

    def _to_int16le_from_2bytes(self, hbytebe, lbytebe):
        uint16le = (lbytebe << 8) | hbytebe
        int16le = uint16le if uint16le < 32768 else uint16le - 65536
        return int16le

    def _get_nbit_from_input_report(self, offset_byte, offset_bit, nbit):
        return (self._input_report[offset_byte] >> offset_bit) & ((1 << nbit) - 1)

    def __del__(self):
        self._close()

    def is_left(self):
        return self._PRODUCT_ID == self.L_PRODUCT_ID

    def is_right(self):
        return self._PRODUCT_ID == self.R_PRODUCT_ID

    def get_battery_charging(self):
        return self._get_nbit_from_input_report(2, 4, 1)

    def get_battery_level(self):
        return self._get_nbit_from_input_report(2, 5, 3)

    def get_button_y(self):
        return self._get_nbit_from_input_report(3, 0, 1)

    def get_button_x(self):
        return self._get_nbit_from_input_report(3, 1, 1)

    def get_button_b(self):
        return self._get_nbit_from_input_report(3, 2, 1)

    def get_button_a(self):
        return self._get_nbit_from_input_report(3, 3, 1)

    def get_button_right_sr(self):
        return self._get_nbit_from_input_report(3, 4, 1)

    def get_button_right_sl(self):
        return self._get_nbit_from_input_report(3, 5, 1)

    def get_button_r(self):
        return self._get_nbit_from_input_report(3, 6, 1)

    def get_button_zr(self):
        return self._get_nbit_from_input_report(3, 7, 1)

    def get_button_minus(self):
        return self._get_nbit_from_input_report(4, 0, 1)

    def get_button_plus(self):
        return self._get_nbit_from_input_report(4, 1, 1)

    def get_button_r_stick(self):
        return self._get_nbit_from_input_report(4, 2, 1)

    def get_button_l_stick(self):
        return self._get_nbit_from_input_report(4, 3, 1)

    def get_button_home(self):
        return self._get_nbit_from_input_report(4, 4, 1)

    def get_button_capture(self):
        return self._get_nbit_from_input_report(4, 5, 1)

    def get_button_charging_grip(self):
        return self._get_nbit_from_input_report(4, 7, 1)

    def get_button_down(self):
        return self._get_nbit_from_input_report(5, 0, 1)

    def get_button_up(self):
        return self._get_nbit_from_input_report(5, 1, 1)

    def get_button_right(self):
        return self._get_nbit_from_input_report(5, 2, 1)

    def get_button_left(self):
        return self._get_nbit_from_input_report(5, 3, 1)

    def get_button_left_sr(self):
        return self._get_nbit_from_input_report(5, 4, 1)

    def get_button_left_sl(self):
        return self._get_nbit_from_input_report(5, 5, 1)

    def get_button_l(self):
        return self._get_nbit_from_input_report(5, 6, 1)

    def get_button_zl(self):
        return self._get_nbit_from_input_report(5, 7, 1)

    def get_stick_left_horizontal(self):
        return self._get_nbit_from_input_report(6, 0, 8) | (self._get_nbit_from_input_report(7, 0, 4) << 8)

    def get_stick_left_vertical(self):
        return self._get_nbit_from_input_report(7, 4, 4) | (self._get_nbit_from_input_report(8, 0, 8) << 4)

    def get_stick_right_horizontal(self):
        return self._get_nbit_from_input_report(9, 0, 8) | (self._get_nbit_from_input_report(10, 0, 4) << 8)

    def get_stick_right_vertical(self):
        return self._get_nbit_from_input_report(10, 4, 4) | (self._get_nbit_from_input_report(11, 0, 8) << 4)

    def get_accel_x(self, sample_idx=0):
        if sample_idx not in [0, 1, 2]:
            raise IndexError('sample_idx should be between 0 and 2')
        return (self._to_int16le_from_2bytes(self._get_nbit_from_input_report(13 + sample_idx * 12, 0, 8),
                                             self._get_nbit_from_input_report(14 + sample_idx * 12, 0, 8))
                - (self._L_ACCEL_OFFSET_X if self.is_left() else self._R_ACCEL_OFFSET_X))

    def get_accel_y(self, sample_idx=0):
        if sample_idx not in [0, 1, 2]:
            raise IndexError('sample_idx should be between 0 and 2')
        return (self._to_int16le_from_2bytes(self._get_nbit_from_input_report(15 + sample_idx * 12, 0, 8),
                                             self._get_nbit_from_input_report(16 + sample_idx * 12, 0, 8))
                - (self._L_ACCEL_OFFSET_Y if self.is_left() else self._R_ACCEL_OFFSET_Y))

    def get_accel_z(self, sample_idx=0):
        if sample_idx not in [0, 1, 2]:
            raise IndexError('sample_idx should be between 0 and 2')
        return (self._to_int16le_from_2bytes(self._get_nbit_from_input_report(17 + sample_idx * 12, 0, 8),
                                             self._get_nbit_from_input_report(18 + sample_idx * 12, 0, 8))
                - (self._L_ACCEL_OFFSET_Z if self.is_left() else self._R_ACCEL_OFFSET_Z))

    def get_gyro_x(self, sample_idx=0):
        if sample_idx not in [0, 1, 2]:
            raise IndexError('sample_idx should be between 0 and 2')
        return self._to_int16le_from_2bytes(self._get_nbit_from_input_report(19 + sample_idx * 12, 0, 8),
                                            self._get_nbit_from_input_report(20 + sample_idx * 12, 0, 8))

    def get_gyro_y(self, sample_idx=0):
        if sample_idx not in [0, 1, 2]:
            raise IndexError('sample_idx should be between 0 and 2')
        return self._to_int16le_from_2bytes(self._get_nbit_from_input_report(21 + sample_idx * 12, 0, 8),
                                            self._get_nbit_from_input_report(22 + sample_idx * 12, 0, 8))

    def get_gyro_z(self, sample_idx=0):
        if sample_idx not in [0, 1, 2]:
            raise IndexError('sample_idx should be between 0 and 2')
        return self._to_int16le_from_2bytes(self._get_nbit_from_input_report(23 + sample_idx * 12, 0, 8),
                                            self._get_nbit_from_input_report(24 + sample_idx * 12, 0, 8))

    def get_status(self):
        return {
            "battery": {
                "charging": self.get_battery_charging(),
                "level": self.get_battery_level(),
            },
            "buttons": {
                "right": {
                    "y": self.get_button_y(),
                    "x": self.get_button_x(),
                    "b": self.get_button_b(),
                    "a": self.get_button_a(),
                    "sr": self.get_button_right_sr(),
                    "sl": self.get_button_right_sl(),
                    "r": self.get_button_r(),
                    "zr": self.get_button_zr(),
                },
                "shared": {
                    "minus": self.get_button_minus(),
                    "plus": self.get_button_plus(),
                    "r-stick": self.get_button_r_stick(),
                    "l-stick": self.get_button_l_stick(),
                    "home": self.get_button_home(),
                    "capture": self.get_button_capture(),
                    "charging-grip": self.get_button_charging_grip(),
                },
                "left": {
                    "down": self.get_button_down(),
                    "up": self.get_button_up(),
                    "right": self.get_button_right(),
                    "left": self.get_button_left(),
                    "sr": self.get_button_left_sr(),
                    "sl": self.get_button_left_sl(),
                    "l": self.get_button_l(),
                    "zl": self.get_button_zl(),
                }
            },
            "analog-sticks": {
                "left": {
                    "horizontal": self.get_stick_left_horizontal(),
                    "vertical": self.get_stick_left_vertical(),
                },
                "right": {
                    "horizontal": self.get_stick_right_horizontal(),
                    "vertical": self.get_stick_right_vertical(),
                },
            },
            "accel": {
                "x": self.get_accel_x(),
                "y": self.get_accel_y(),
                "z": self.get_accel_z(),
            },
            "gyro": {
                "x": self.get_gyro_x(),
                "y": self.get_gyro_y(),
                "z": self.get_gyro_z(),
            },
        }

    def set_player_lamp_on(self, on_pattern):
        self._write_output_report(
            b'\x01', b'\x30', (on_pattern & 0xF).to_bytes(1, byteorder='big'))

    def set_player_lamp_flashing(self, flashing_pattern):
        self._write_output_report(
            b'\x01', b'\x30', ((flashing_pattern & 0xF) << 4).to_bytes(1, byteorder='big'))

    def set_player_lamp(self, pattern):
        self._write_output_report(
            b'\x01', b'\x30', pattern.to_bytes(1, byteorder='big'))


if __name__ == '__main__':
    ids = d.get_L_ids() if None not in d.get_L_ids() else d.get_R_ids()

    if None not in ids:
        joycon = JoyCon(*ids)
        lamp_pattern = 0
        while True:
            print(joycon.get_status())
            joycon.set_player_lamp_on(lamp_pattern)
            lamp_pattern = (lamp_pattern + 1) & 0xf
            time.sleep(0.2)
