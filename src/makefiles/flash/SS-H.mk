ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive17 SimAnnealing9 SimAnnealing15 SimAnnealing17 bonr9 bonr15 bonr17 b29 b215 b217 rand9 rand15 rand17 ExpProgressive9 ExpProgressive15 ExpProgressive17 rand233

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive17:
	python3 gate.py -t progressive_stats -E 17 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing17:
	python3 gate.py -t SimAnnealing_stats -E 17 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr17:
	python3 gate.py -t bonr_stats -E 17 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b217:
	python3 gate.py -t b2_stats -E 17 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand17:
	python3 gate.py -t rand_stats -E 17 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive17:
	python3 gate.py -t ExpProgressive_stats -E 17 $(ARGUMENT)

rand233:
	python3 gate.py -t rand_stats -E 233 $(ARGUMENT)

