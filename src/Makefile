DATASETS := $(wildcard ../data/cat_a/*.csv)
TARGETS := $(DATASETS:../data/cat_a/%.csv=%)

all: $(TARGETS)

%: ../data/cat_a/%.csv
	python3 main.py "-f $<"

ranks:
	tail -q -n +2 ../results/sk/flash/*.sk.csv | awk -F, '{ treatment[$$2] = treatment[$$2] " " $$1 } END { for (t in treatment) print t, treatment[t] }' > ../results/stats/flash/ranks.stats.txt
	python3 -c "from stats import egSlurp; egSlurp('../results/stats/flash/ranks.stats.txt')" > ../results/sk/flash/ranks.sk.txt
	cat ../results/sk/flash/ranks.sk.txt

ranks_stats:
	tail -q -n +2 ../results/sk/flash/*.sk.csv | awk -F, '{ treatment[$$2] = treatment[$$2] " " $$1 } END { for (t in treatment) print t, treatment[t] }' > ../results/stats/flash/ranks.stats.txt
	cat ../results/stats/flash/ranks.stats.txt

ranks_sum:
	tail -q -n +2 ../results/sk/flash/*.sk.csv | awk -F, '{rank[$$2]+=$$1} END {for (treatment in rank) print rank[treatment] ", " treatment}' | sort -n > ../results/sk/flash/ranks.sum.txt
	cat ../results/sk/flash/ranks.sum.txt

ranks_plot:
	ls ../results/stats/flash/* | xargs -n 1 python3 plot_boxplot.py

barcharts_plot:
	ls ../results/sk/flash/*.sk.csv | xargs -n 1 python3 plot_stats.py > /dev/null

.SILENT: ranks ranks_stats ranks_sum ranks_plot barcharts_plot
