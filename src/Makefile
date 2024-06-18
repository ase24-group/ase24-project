DATADIR ?= ../data/cat_b/cat_b_2
DATASETS := $(wildcard $(DATADIR)/*.csv)
TARGETS := $(DATASETS:$(DATADIR)/%.csv=%)

all: $(TARGETS)

%: $(DATADIR)/%.csv
	python3 main.py "-f $<"

rq_table:
	./rqTable.sh > ../results/sk/cat_a_b/rqTable.out

ranks_plot:
	ls ../results/stats/cat_a_b/* | xargs -n 1 python3 plot_boxplot.py

barcharts_plot:
	ls ../results/sk/cat_a_b/*.sk.csv | xargs -n 1 python3 plot_stats.py > /dev/null

.SILENT: ranks ranks_stats ranks_sum ranks_plot barcharts_plot
