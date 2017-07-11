init:
	virtualenv venv
	pip install -r requirements.txt

start:
	source venv/bin/activate

download:
	@python tsedata/tsedata.py
