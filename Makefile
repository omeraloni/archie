install:
	poetry install

build:
	poetry build

clean:
	rm -dfr dist/
	rm -dfr logs/

.PHONY: install clean