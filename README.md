# Invisible Magnet

Automatically animates the transition of the widgets' position (and optionally size).
Unlike the [Magnet](https://github.com/kivy-garden/garden.magnet), this one does not require extra widgets.

[Youtube](https://youtu.be/Lb2zzaq3i0E)


## Installation

Pin the minor version.

```text
poetry add kivy-garden-invisible-magnet@~0.1
pip install "kivy-garden-invisible-magnet>=0.1,<0.2"
```

## Usage

```python
from kivy_garden.invisible_magnet import magnetize

magnetize(widget)
```

Install if you prefer not to manually magnetize each individual widget.

```python
from kivy_garden.invisible_magnet import install

install()
```

All the widgets created after the installation will be automatically magnetized.
