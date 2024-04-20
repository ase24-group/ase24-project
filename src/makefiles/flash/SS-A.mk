ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive37 SimAnnealing9 SimAnnealing15 SimAnnealing37 bonr9 bonr15 bonr37 b29 b215 b237 rand9 rand15 rand37 ExpProgressive9 ExpProgressive15 ExpProgressive37 rand1208

base:
	python3 gate.py -t base_stats $(ARGUMENT)

progressive9:
	python3 gate.py -t progressive_stats -E 9 $(ARGUMENT)

progressive15:
	python3 gate.py -t progressive_stats -E 15 $(ARGUMENT)

progressive37:
	python3 gate.py -t progressive_stats -E 37 $(ARGUMENT)

SimAnnealing9:
	python3 gate.py -t SimAnnealing_stats -E 9 $(ARGUMENT)

SimAnnealing15:
	python3 gate.py -t SimAnnealing_stats -E 15 $(ARGUMENT)

SimAnnealing37:
	python3 gate.py -t SimAnnealing_stats -E 37 $(ARGUMENT)

bonr9:
	python3 gate.py -t bonr_stats -E 9 $(ARGUMENT)

bonr15:
	python3 gate.py -t bonr_stats -E 15 $(ARGUMENT)

bonr37:
	python3 gate.py -t bonr_stats -E 37 $(ARGUMENT)

b29:
	python3 gate.py -t b2_stats -E 9 $(ARGUMENT)

b215:
	python3 gate.py -t b2_stats -E 15 $(ARGUMENT)

b237:
	python3 gate.py -t b2_stats -E 37 $(ARGUMENT)

rand9:
	python3 gate.py -t rand_stats -E 9 $(ARGUMENT)

rand15:
	python3 gate.py -t rand_stats -E 15 $(ARGUMENT)

rand37:
	python3 gate.py -t rand_stats -E 37 $(ARGUMENT)

ExpProgressive9:
	python3 gate.py -t ExpProgressive_stats -E 9 $(ARGUMENT)

ExpProgressive15:
	python3 gate.py -t ExpProgressive_stats -E 15 $(ARGUMENT)

ExpProgressive37:
	python3 gate.py -t ExpProgressive_stats -E 37 $(ARGUMENT)

rand1208:
	python3 gate.py -t rand_stats -E 1208 $(ARGUMENT)

