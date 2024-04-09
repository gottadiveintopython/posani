import pytest


@pytest.fixture(autouse=True)
def _uninstall_all():
    from kivy_garden.invisible_magnet import uninstall_all
    uninstall_all()


def test_global_state():
    from kivy_garden.invisible_magnet import install, uninstall
    from kivy_garden.invisible_magnet._install import _installed
    from kivy.uix.widget import Widget
    from kivy.uix.label import Label

    v = '_magnetize_soon'

    assert _installed == set()
    assert v not in Widget.__dict__
    assert v not in Label.__dict__

    install(target=Widget)
    assert _installed == {'Widget', }
    assert v in Widget.__dict__
    assert v not in Label.__dict__

    install(target='Label')
    assert _installed == {'Widget', 'Label', }
    assert v in Widget.__dict__
    assert v in Label.__dict__

    uninstall(target='Widget')
    assert _installed == {'Label', }
    assert v not in Widget.__dict__
    assert v in Label.__dict__

    uninstall(target=Label)
    assert _installed == set()
    assert v not in Widget.__dict__
    assert v not in Label.__dict__


def test_install_and_uninstall(kivy_clock):
    from kivy_garden.invisible_magnet import install, uninstall, is_magnetized
    from kivy.uix.widget import Widget

    install()
    w1 = Widget()
    assert not is_magnetized(w1)
    kivy_clock.tick()
    assert is_magnetized(w1)

    uninstall()
    w2 = Widget()
    assert is_magnetized(w1)
    assert not is_magnetized(w2)
    kivy_clock.tick()
    assert is_magnetized(w1)
    assert not is_magnetized(w2)
