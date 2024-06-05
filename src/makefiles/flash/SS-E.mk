ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive28 SimAnnealing9 SimAnnealing15 SimAnnealing28 bonr9 bonr15 bonr28 b29 b215 b228 rand9 rand15 rand28 ExpProgressive9 ExpProgressive15 ExpProgressive28 PI9 PI15 PI28 EI9 EI15 EI28 UCB9 UCB15 UCB28 rand680

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive28:
	python3 gate.py -t progressive_stats -E 28 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing28:
	python3 gate.py -t SimAnnealing_stats -E 28 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr28:
	python3 gate.py -t bonr_stats -E 28 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b228:
	python3 gate.py -t b2_stats -E 28 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand28:
	python3 gate.py -t rand_stats -E 28 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive28:
	python3 gate.py -t ExpProgressive_stats -E 28 $(ARGUMENT)

PI9:
	python3 gate.py -t PI_stats -E 9 $(ARGUMENT)

PI15:
	python3 gate.py -t PI_stats -E 15 $(ARGUMENT)

PI28:
	python3 gate.py -t PI_stats -E 28 $(ARGUMENT)

EI9:
	python3 gate.py -t EI_stats -E 9 $(ARGUMENT)

EI15:
	python3 gate.py -t EI_stats -E 15 $(ARGUMENT)

EI28:
	python3 gate.py -t EI_stats -E 28 $(ARGUMENT)

UCB9:
	python3 gate.py -t UCB_stats -E 9 $(ARGUMENT)

UCB15:
	python3 gate.py -t UCB_stats -E 15 $(ARGUMENT)

UCB28:
	python3 gate.py -t UCB_stats -E 28 $(ARGUMENT)

rand680:
	python3 gate.py -t rand_stats -E 680 $(ARGUMENT)

