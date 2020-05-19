# ![logo](https://i.gyazo.com/af04cc6000f2815ebc00d4dcf06b1eb9.png)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/joycon-python)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/joycon-python)

Python driver for Nintendo Switch Joy-Con

We are referring to [dekuNukem/Nintendo_Switch_Reverse_Engineering](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering)

## Install

```shell
pip install joycon-python hidapi pyglm
```

## Usage

Quick status check

```shell
cd joycon-python/
python -m pyjoycon.joycon
```

or use as module

```python
from pyjoycon import JoyCon, get_R_id

joycon_id = get_R_id()
joycon = JoyCon(*joycon_id)

joycon.get_status()
```

## Status values

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

You need `cython-hidapi` to use Bluetooth / HID connection in Python.

Alternatively, you can use `hid` instead if `cython-hidapi` fails to find your JoyCons.


## Gyroscope

We have a specialized class which tracks the gyroscope for you, and
exposes this tracked state in a simplified manner:

```python
from pyjoycon import GyroTrackingJoyCon, get_R_id
import time

joycon_id = get_R_id()
joycon = GyroTrackingJoyCon(*joycon_id)
for i in range(20):
    print("joycon pointer:  ", joycon.pointer)
    print("joycon rotation: ", joycon.rotation)
    print("joycon direction:", joycon.direction)
    print()
    time.sleep(0.05)
```


## Button events

We have a specialized class which tracks the state of the JoyCon buttons and
provides changes as events. Here is an example of how it could be used with `pygame`:

```python
from pyjoycon import ButtonEventJoyCon, get_R_id
import pygame

joycon_id = get_R_id()
joycon = ButtonEventJoyCon(*joycon_id)

...

while 1:
    pygame.time.wait(int(1000/60))

    ...

    for event_type, status in joycon.events():
        print(event_type, status)

    ...

    pygame.display.flip()
```


## Combining multiple JoyCon helper classes

```python
import pyjoycon

class MyJoyCon(
        pyjoycon.GyroTrackingJoyCon,
        pyjoycon.ButtonEventJoyCon,
    ): pass
```


## Environments

- macOS Mojave (10.14.6)
- Python (3.7.4)
- hidapi (0.7.99.post21)
