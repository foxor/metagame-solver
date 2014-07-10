all: analyze

hearthstone.stats: hearthstone.log calculator.py
	./calculator.py hearthstone.log > hearthstone.stats

hearthstone.meta: hearthstone.stats solver.py
	./solver.py hearthstone.stats > hearthstone.meta

.PHONY: analyze

analyze: analyzer.py hearthstone.log hearthstone.meta
	./analyzer.py hearthstone.log hearthstone.meta
