run:
	python -B run.py experiment.yaml
runv:
	python -B run.py experiment.yaml -v

run-profiler:
	python -B -m cProfile run.py experiment.yaml > profiler.log
	cat profile.log | grep -E "(genome|population|run|simulation).py"

clean:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

conda-export:
	conda env export | grep -v "^prefix: " > environment.yml
