ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive40 SimAnnealing9 SimAnnealing15 SimAnnealing40 bonr9 bonr15 bonr40 b29 b215 b240 rand9 rand15 rand40 ExpProgressive9 ExpProgressive15 ExpProgressive40 PI9 PI15 PI40 EI9 EI15 EI40 UCB9 UCB15 UCB40

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive40:
	python3 gate.py -t progressive_stats -E 40 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing40:
	python3 gate.py -t SimAnnealing_stats -E 40 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr40:
	python3 gate.py -t bonr_stats -E 40 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b240:
	python3 gate.py -t b2_stats -E 40 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand40:
	python3 gate.py -t rand_stats -E 40 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive40:
	python3 gate.py -t ExpProgressive_stats -E 40 $(ARGUMENT)

PI9:
	python3 gate.py -t PI_stats -E 9 $(ARGUMENT)

PI15:
	python3 gate.py -t PI_stats -E 15 $(ARGUMENT)

PI40:
	python3 gate.py -t PI_stats -E 40 $(ARGUMENT)

EI9:
	python3 gate.py -t EI_stats -E 9 $(ARGUMENT)

EI15:
	python3 gate.py -t EI_stats -E 15 $(ARGUMENT)

EI40:
	python3 gate.py -t EI_stats -E 40 $(ARGUMENT)

UCB9:
	python3 gate.py -t UCB_stats -E 9 $(ARGUMENT)

UCB15:
	python3 gate.py -t UCB_stats -E 15 $(ARGUMENT)

UCB40:
	python3 gate.py -t UCB_stats -E 40 $(ARGUMENT)

