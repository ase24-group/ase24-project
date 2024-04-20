ARGUMENT := -f ../data/auto93.csv

ifdef ARG
	ARGUMENT := $(ARG)
endif

all: base progressive9 progressive15 progressive14 SimAnnealing9 SimAnnealing15 SimAnnealing14 bonr9 bonr15 bonr14 rand9 rand15 rand14 ExpProgressive9 ExpProgressive15 ExpProgressive14 rand176

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

rand176:
	python3 gate.py -t rand_stats -E 176 $(ARGUMENT)

