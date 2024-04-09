import pytest


@pytest.mark.parametrize('animate_size', [True, False])
def test_magnetize_and_unmagnetize(animate_size):
    from kivy_garden.invisible_magnet import magnetize, unmagnetize
    from kivy.uix.widget import Widget

    w = Widget(pos=(0, 0))
    magnetize(w, animate_size=animate_size)
    unmagnetize(w)
