PROJECT=nornir_http
CODE_DIRS=${PROJECT} tests

# Run pytest
.PHONY: pytest
pytest:
	uv run pytest -vs ${ARGS}

# Check if the python code needs to be reformatted 
.PHONY: black
black:
	uv run black --check ${CODE_DIRS}

# Python type check
.PHONY: mypy
mypy:
	uv run mypy ${CODE_DIRS}

# Runn pytest, black and mypy
.PHONY: tests
tests: pytest black mypy

# use "make bump ARGS=patch" to bump the version. ARGS can be patch, minor or major.
.PHONY: bump
bump:
	uv version --bump ${ARGS}
	sed -i -E "s|\"\b[0-9]+.\b[0-9]+.\b[0-9]+\"  # From Makefile|\"`uv version -s`\"  # From Makefile|g" ${PROJECT}/__init__.py
	sed -i -E "s|\"\b[0-9]+.\b[0-9]+.\b[0-9]+\"  # From Makefile|\"`uv version -s`\"  # From Makefile|g" tests/test_${PROJECT}.py
