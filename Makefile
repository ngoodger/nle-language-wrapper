.PHONY: format-python
.PHONY: format-cpp
.PHONY: format-python-check
.PHONY: format-cpp-check
.PHONY: test

format-python:
	isort nle_language_wrapper
	black nle_language_wrapper --config pyproject.toml

format-cpp:
	clang-format -style=Google -i src/main.cpp

format-python-check:
	isort -c --diff nle_language_wrapper
	black --check --diff nle_language_wrapper
	pylint \
		nle_language_wrapper/agents/ \
		nle_language_wrapper/wrappers/ \
		nle_language_wrapper/scripts/ \
		nle_language_wrapper/tests/
	 
format-cpp-check:
	clang-format --dry-run src/main.cpp --style=Google

test:
	pytest nle_language_wrapper/tests --cov .
