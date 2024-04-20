ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive33 SimAnnealing9 SimAnnealing15 SimAnnealing33 bonr9 bonr15 bonr33 rand9 rand15 rand33 ExpProgressive9 ExpProgressive15 ExpProgressive33 rand972

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive33:
	python3 gate.py -t progressive_stats -E 33 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing33:
	python3 gate.py -t SimAnnealing_stats -E 33 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr33:
	python3 gate.py -t bonr_stats -E 33 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand33:
	python3 gate.py -t rand_stats -E 33 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive33:
	python3 gate.py -t ExpProgressive_stats -E 33 $(ARGUMENT)

rand972:
	python3 gate.py -t rand_stats -E 972 $(ARGUMENT)
