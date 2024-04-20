ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive62 SimAnnealing9 SimAnnealing15 SimAnnealing62 bonr9 bonr15 bonr62 rand9 rand15 rand62 ExpProgressive9 ExpProgressive15 ExpProgressive62 rand3456

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

rand3456:
	python3 gate.py -t rand_stats -E 3456 $(ARGUMENT)

