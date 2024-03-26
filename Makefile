PYTEST = python -m pytest
FLAKE8 = python -m flake8

test:
	env KCFG_GRAPHICS_MAXFPS=0 $(PYTEST) ./tests

html:
	sphinx-build -M html ./sphinx ./docs

