# PosAni

![logo.png](logo.png)

Automatically animates changes in widget positions.

[Youtube](https://youtu.be/ifF7onEub1A)


## Installation

Pin the minor version.

```text
poetry add kivy-garden-posani@~0.3
pip install "kivy-garden-posani>=0.3,<0.4"
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

## Q&A

### Why is it implemented through a widget's canvas rather than just updating the widget's position?

Many layouts, such as `BoxLayout` and `GridLayout`, constrain the positions of their children, so moving a widget to an arbitrary position isn't always possible.

### Why does it not animate widget sizes?

It used to until version 0.1.x but this feature was dropped in version 0.2.0.
The reason is that scaling a widget using `kivy.graphics.Scale` produces visually unappealing results.
