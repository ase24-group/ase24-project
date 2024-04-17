ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive SimAnnealing bonr rand

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive:
	python3 gate.py -t progressive_stats $(ARGUMENT)

SimAnnealing:
	python3 gate.py -t SimAnnealing_stats $(ARGUMENT)

bonr:
	python3 gate.py -t bonr_stats $(ARGUMENT)

rand:
	python3 gate.py -t rand_stats $(ARGUMENT)
