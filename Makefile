all: hearthstone.meta

hearthstone.stats: hearthstone.log calculator.py
	./calculator.py hearthstone.log 2 > hearthstone.stats

hearthstone.meta: hearthstone.stats solver.py
	./solver.py hearthstone.stats > hearthstone.meta
	cat hearthstone.meta
