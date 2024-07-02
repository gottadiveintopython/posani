# PosAni

Automatically animates the transition of the widgets' position.
Unlike the [Magnet](https://github.com/kivy-garden/garden.magnet), this one does not require extra widgets.

[Youtube](https://youtu.be/Lb2zzaq3i0E)


## Installation

Pin the minor version.

```text
poetry add kivy-garden-posani@~0.2
pip install "kivy-garden-posani>=0.2,<0.3"
```

## Usage

```python
from kivy_garden.posani import activate

activate(widget)
```

Install if you prefer not to manually activate each individual widget.

```python
from kivy_garden.posani import install

install()
```

All the widgets created after the installation will be automatically "activated".
