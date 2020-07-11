install:
	poetry install

build:
	poetry build

clean:
	rm -dfr {dist,logs,archie_cli.egg-info,__pycache__}

.PHONY: install clean