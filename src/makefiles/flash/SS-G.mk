ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive14 SimAnnealing9 SimAnnealing15 SimAnnealing14 bonr9 bonr15 bonr14 b29 b215 b214 rand9 rand15 rand14 ExpProgressive9 ExpProgressive15 ExpProgressive14 PI9 PI15 PI14 UCB9 UCB15 UCB14 rand176

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive14:
	python3 gate.py -t progressive_stats -E 14 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing14:
	python3 gate.py -t SimAnnealing_stats -E 14 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr14:
	python3 gate.py -t bonr_stats -E 14 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b214:
	python3 gate.py -t b2_stats -E 14 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand14:
	python3 gate.py -t rand_stats -E 14 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive14:
	python3 gate.py -t ExpProgressive_stats -E 14 $(ARGUMENT)

PI9:
	python3 gate.py -t PI_stats -E 9 $(ARGUMENT)

PI15:
	python3 gate.py -t PI_stats -E 15 $(ARGUMENT)

PI14:
	python3 gate.py -t PI_stats -E 14 $(ARGUMENT)

UCB9:
	python3 gate.py -t UCB_stats -E 9 $(ARGUMENT)

UCB15:
	python3 gate.py -t UCB_stats -E 15 $(ARGUMENT)

UCB14:
	python3 gate.py -t UCB_stats -E 14 $(ARGUMENT)

rand176:
	python3 gate.py -t rand_stats -E 176 $(ARGUMENT)

