run:
	python src/game.py

run_tests:
	python -m unittest discover

run_tests_with_coverage:
	coverage run -m unittest discover

display_coverage:
	coverage html
	firefox htmlcov/index.html &

run_tests_and_display_coverage: run_tests_with_coverage display_coverage