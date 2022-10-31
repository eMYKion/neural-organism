clean:
	rm -rf __pycache__/

conda-export:
	conda env export | grep -v "^prefix: " > environment.yml
