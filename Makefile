install: 
	sudo apt-get update
	sudo apt-get install python3

init:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run: init 
	.venv/bin/python3 data_collector/__main__.py

clean:	
	rm -rf data_collector/src/services/__pycache__
	rm -rf data_collector/controllers/__pycache__
	rm -rf data_collector/collectors/__pycache__
	rm -rf data_collector/src/utils/__pycache__
	rm -rf data_collector/src/app/__pycache__
	rm -rf data_collector/src/__pycache__

	rm -rf .venv
