all: hearthstone.meta

hearthstone.stats: hearthstone.log calculator.py
	./calculator.py hearthstone.log > hearthstone.stats

hearthstone.meta: hearthstone.stats solver.py
	./solver.py hearthstone.stats > hearthstone.meta
	cat hearthstone.meta
	./picker.py hearthstone.meta
