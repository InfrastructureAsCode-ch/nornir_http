from nornir_http import __version__


def test_version():
    assert __version__ == "0.2.0"  # From Makefile
