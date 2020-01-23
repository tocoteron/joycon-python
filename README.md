# joycon-python

Python driver for Nintendo Switch Joy-Con

## Usage

```python
from pyjoycon import device
from pyjoycon.joycon import JoyCon


r_ids = device.get_ids("R")
r_joycon = JoyCon(*r_ids)

r_joycon.get_accel_x()

```

## install

```shell
pip install -r requirements.txt
```

`cython-hidapi` to use Bluetooth / HID connection in Python.

## environments

- macOS Mojave (10.14.6)
- Python (3.7.4)
- hidapi (0.7.99.post21)
