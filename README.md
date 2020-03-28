# ![logo](https://i.gyazo.com/af04cc6000f2815ebc00d4dcf06b1eb9.png)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/joycon-python)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/joycon-python)

Python driver for Nintendo Switch Joy-Con

## install

```shell
pip install joycon-python
```

## usage

Quick status check

```shell
cd joycon-python/
python pyjoycon/joycon.py
```

or use as module

```python
from pyjoycon import device
from pyjoycon.joycon import JoyCon


joycon_id = device.get_R_id()
joycon = JoyCon(*joycon_id)

joycon.get_status()
```

## status values

```python
{
  'battery': {
    'charging': 0,
    'level': 2
  },
  'buttons': {
    'right': {
      'y': 0,
      'x': 0,
      'b': 0,
      'a': 0,
      'sr': 0,
      'sl': 0,
      'r': 0,
      'zr': 0
    },
    'shared': {
      'minus': 0,
      'plus': 0,
      'r-stick': 0,
      'l-stick': 0,
      'home': 0,
      'capture': 0,
      'charging-grip': 0
    },
    'left': {
      'down': 0,
      'up': 0,
      'right': 0,
      'left': 0,
      'sr': 0,
      'sl': 0,
      'l': 0,
      'zl': 0
    }
  },
  'analog-sticks': {
    'left': {
      'horizontal': 0,
      'vertical': 0
    },
    'right': {
      'horizontal': 2170,
      'vertical': 1644
    }
  },
  'accel': {
    'x': 879,
    'y': 1272,
    'z': 549
  },
  'gyro': {
    'x': -354,
    'y': -7,
    'z': 281
  }
}

```

`cython-hidapi` to use Bluetooth / HID connection in Python.

## environments

- macOS Mojave (10.14.6)
- Python (3.7.4)
- hidapi (0.7.99.post21)
