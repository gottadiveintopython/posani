import pytest


@pytest.fixture(autouse=True)
def _uninstall_all():
    from kivy_garden.posani import uninstall_all
    uninstall_all()


def test_global_state():
    from kivy_garden.posani import install, uninstall, _installed
    from kivy.uix.widget import Widget
    from kivy.uix.label import Label

    assert _installed == set()
    install(target=Widget)
    assert _installed == {'Widget', }
    install(target='Label')
    assert _installed == {'Widget', 'Label', }
    uninstall(target='Widget')
    assert _installed == {'Label', }
    uninstall(target=Label)
    assert _installed == set()


def test_install_and_uninstall():
    from kivy_garden.posani import install, uninstall, is_active
    from kivy.uix.widget import Widget

    install()
    w1 = Widget()
    assert is_active(w1)
    uninstall()
    w2 = Widget()
    assert is_active(w1)
    assert not is_active(w2)
