ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive54 SimAnnealing9 SimAnnealing15 SimAnnealing54 bonr9 bonr15 bonr54 rand9 rand15 rand54 ExpProgressive9 ExpProgressive15 ExpProgressive54 rand2592

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive54:
	python3 gate.py -t progressive_stats -E 54 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing54:
	python3 gate.py -t SimAnnealing_stats -E 54 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr54:
	python3 gate.py -t bonr_stats -E 54 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand54:
	python3 gate.py -t rand_stats -E 54 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive54:
	python3 gate.py -t ExpProgressive_stats -E 54 $(ARGUMENT)

rand2592:
	python3 gate.py -t rand_stats -E 2592 $(ARGUMENT)

