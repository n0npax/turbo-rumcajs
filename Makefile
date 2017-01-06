

test:
	pytest -vs

clean:
	find . -name *.pyc -delete -type f
	find . -name __pycache__ -delete -type d
