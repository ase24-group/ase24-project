DATADIR ?= ../data/cat_a/cat_a_1
DATASETS := $(wildcard $(DATADIR)/*.csv)
TARGETS := $(DATASETS:$(DATADIR)/%.csv=%)

all: $(TARGETS)

%: $(DATADIR)/%.csv
	python3 main.py "-f $<"

ranks:
	cat ../results/sk/cat_a_b/*.sk.txt | grep -v '^#' | awk -F, '{ treatment[$$2 "," $$3] = treatment[$$2 "," $$3] " " $$1 } END { for (t in treatment) print t, treatment[t] }' > ../results/stats/cat_a_b/ranks.stats.txt
	python3 -c "from stats import egSlurp; egSlurp('../results/stats/cat_a_b/ranks.stats.txt')" > ../results/sk/cat_a_b/ranks.sk.txt
	cat ../results/sk/cat_a_b/ranks.sk.txt

ranks_stats:
	cat ../results/sk/cat_a_b/*.sk.txt | grep -v '^#' | awk -F, '{ treatment[$$2 "," $$3] = treatment[$$2 "," $$3] " " $$1 } END { for (t in treatment) print t, treatment[t] }' > ../results/stats/cat_a_b/ranks.stats.txt
	cat ../results/stats/cat_a_b/ranks.stats.txt

ranks_sum:
	cat ../results/sk/cat_a_b/*.sk.txt | grep -v '^#' | awk -F, '{rank[$$2 "," $$3] += $$1} END {for (treatment in rank) print rank[treatment] ", " treatment}' | sort -n > ../results/sk/cat_a_b/ranks.sum.txt
	cat ../results/sk/cat_a_b/ranks.sum.txt

ranks_plot:
	ls ../results/stats/cat_a_b/* | xargs -n 1 python3 plot_boxplot.py

barcharts_plot:
	ls ../results/sk/cat_a_b/*.sk.csv | xargs -n 1 python3 plot_stats.py > /dev/null

.SILENT: ranks ranks_stats ranks_sum ranks_plot barcharts_plot
