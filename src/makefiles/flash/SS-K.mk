ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive54 SimAnnealing9 SimAnnealing15 SimAnnealing54 bonr9 bonr15 bonr54 b29 b215 b254 rand9 rand15 rand54 ExpProgressive9 ExpProgressive15 ExpProgressive54 PI9 PI15 PI54 UCB9 UCB15 UCB54 rand2592

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

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b254:
	python3 gate.py -t b2_stats -E 54 $(ARGUMENT)

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

PI9:
	python3 gate.py -t PI_stats -E 9 $(ARGUMENT)

PI15:
	python3 gate.py -t PI_stats -E 15 $(ARGUMENT)

PI54:
	python3 gate.py -t PI_stats -E 54 $(ARGUMENT)

UCB9:
	python3 gate.py -t UCB_stats -E 9 $(ARGUMENT)

UCB15:
	python3 gate.py -t UCB_stats -E 15 $(ARGUMENT)

UCB54:
	python3 gate.py -t UCB_stats -E 54 $(ARGUMENT)

rand2592:
	python3 gate.py -t rand_stats -E 2592 $(ARGUMENT)

