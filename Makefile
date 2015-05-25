all: gv overview overview2 sim better whered marketData trading

gv:
	dot -Tpng -o doit.png doit.gv

overview:
	dot -Tpng -Gsize=9,15 -Gdpi=100 -o overview.png overview.gv

overview2:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o overview2.png overview.gv

whered:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o whered.png whered.gv


better:
	dot -Tpng -o better.png better.gv

marketData:
	dot -Tpng -Gsize=10,20 -Gdpi=160 -o marketData.png marketData.gv

trading:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o trading.png trading.gv


sim:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o sim.png sim.gv


