.PHONY: format-python
.PHONY: format-cpp
.PHONY: format-python-check
.PHONY: format-cpp-check
.PHONY: test

format-python:
	isort setup.py nle_language_wrapper
	black setup.py nle_language_wrapper --config pyproject.toml

format-cpp:
	clang-format -style=Google -i src/main.cpp

format-python-check:
	isort -c --diff setup.py nle_language_wrapper
	black --check --diff setup.py nle_language_wrapper
	pylint setup.py \
		nle_language_wrapper/agents/ \
		nle_language_wrapper/wrappers/ \
		nle_language_wrapper/scripts/ \
		nle_language_wrapper/tests/
	 
format-cpp-check:
	cpplint --filter -readability/braces src/main.cpp

test:
	pytest nle_language_wrapper/tests
