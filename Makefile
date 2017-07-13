clean:
	@rm -rf *.pyc **/*.pyc *~

test:
	@make clean
	@nosetests -s --verbose --with-coverage --cover-erase --cover-package=tsedata tests/*
	@make clean
