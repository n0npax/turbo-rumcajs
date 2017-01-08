

test:
	pytest -vs

clean:
	find . -name .cache -type d | xargs rm -fr
	find . -name .rope -type d | xargs rm -fr
	find . -name *.pyc -delete -type f
	find . -name __pycache__ -type d | xargs rm -fr
