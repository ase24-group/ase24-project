ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive62 SimAnnealing9 SimAnnealing15 SimAnnealing62 bonr9 bonr15 bonr62 b29 b215 b262 rand9 rand15 rand62 ExpProgressive9 ExpProgressive15 ExpProgressive62 PI9 PI15 PI62 EI9 EI15 EI62 UCB9 UCB15 UCB62 rand3456

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive62:
	python3 gate.py -t progressive_stats -E 62 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing62:
	python3 gate.py -t SimAnnealing_stats -E 62 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr62:
	python3 gate.py -t bonr_stats -E 62 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b262:
	python3 gate.py -t b2_stats -E 62 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand62:
	python3 gate.py -t rand_stats -E 62 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive62:
	python3 gate.py -t ExpProgressive_stats -E 62 $(ARGUMENT)

PI9:
	python3 gate.py -t PI_stats -E 9 $(ARGUMENT)

PI15:
	python3 gate.py -t PI_stats -E 15 $(ARGUMENT)

PI62:
	python3 gate.py -t PI_stats -E 62 $(ARGUMENT)

EI9:
	python3 gate.py -t EI_stats -E 9 $(ARGUMENT)

EI15:
	python3 gate.py -t EI_stats -E 15 $(ARGUMENT)

EI62:
	python3 gate.py -t EI_stats -E 62 $(ARGUMENT)

UCB9:
	python3 gate.py -t UCB_stats -E 9 $(ARGUMENT)

UCB15:
	python3 gate.py -t UCB_stats -E 15 $(ARGUMENT)

UCB62:
	python3 gate.py -t UCB_stats -E 62 $(ARGUMENT)

rand3456:
	python3 gate.py -t rand_stats -E 3456 $(ARGUMENT)

