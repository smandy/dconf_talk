all: gv overview overview2 sim better whered marketData trading structure

gv:
	dot -Tpng -o doit.png doit.gv

overview:
	dot -Tpng -Gsize=10,20 -Gdpi=150 -o overview.png overview.gv

overview2:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o overview2.png overview.gv

whered:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o whered.png whered.gv

structure:
	dot -Tpng -Gsize=10,20 -Gdpi=120 -o structure.png structure.gv



better:
	dot -Tpng -o better.png better.gv



marketData:
	dot -Tpng -Gsize=10,20 -Gdpi=160 -o marketData.png marketData.gv

trading:
	dot -Tpng -Gsize=10,20 -Gdpi=160 -o trading.png trading.gv

sim:
	dot -Tpng -Gsize=10,20 -Gdpi=150 -o sim.png sim.gv


