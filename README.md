# PosAni

![logo.png](logo.png)

Automatically animates the transition of the widgets' position.
Unlike the [garden.magnet](https://github.com/kivy-garden/garden.magnet), this one does not require extra widgets.

[Youtube](https://youtu.be/Lb2zzaq3i0E) (This is an older implementation, and differs from the current one.)


## Installation

Pin the minor version.

```text
poetry add kivy-garden-posani@~0.2
pip install "kivy-garden-posani>=0.2,<0.3"
```

## Usage

```python
from kivy_garden import posani

posani.activate(widget)
```

Install if you prefer not to manually activate each individual widget.
All the widgets created after the installation will be automatically "activated".

```python
posani.install()
```

To install on a specific type of widgets:

```python
posani.install(target="WidgetClassName")
```
