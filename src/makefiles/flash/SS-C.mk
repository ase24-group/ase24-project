ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive39 SimAnnealing9 SimAnnealing15 SimAnnealing39 bonr9 bonr15 bonr39 b29 b215 b239 rand9 rand15 rand39 ExpProgressive9 ExpProgressive15 ExpProgressive39 rand1360

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive39:
	python3 gate.py -t progressive_stats -E 39 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing39:
	python3 gate.py -t SimAnnealing_stats -E 39 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr39:
	python3 gate.py -t bonr_stats -E 39 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b239:
	python3 gate.py -t b2_stats -E 39 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand39:
	python3 gate.py -t rand_stats -E 39 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive39:
	python3 gate.py -t ExpProgressive_stats -E 39 $(ARGUMENT)

rand1360:
	python3 gate.py -t rand_stats -E 1360 $(ARGUMENT)

