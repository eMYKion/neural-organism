run:
	python -B run.py experiment.yaml
runv:
	python -B run.py experiment.yaml -v

run-profiler:
	python -B -m cProfile run.py experiment.yaml > profiler.log
	cat profile.log | grep -E "(genome|population|run|simulation).py"

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

conda-export:
	conda env export | grep -v "^prefix: " > environment.yml
