all: flash_stats

flash_stats: SS-A SS-B SS-C SS-D SS-E SS-F SS-G SS-H SS-I SS-J SS-K

SS-A:
	python3 main.py "-f ../data/flash/SS-A.csv"

SS-B:
	python3 main.py "-f ../data/flash/SS-B.csv"

SS-C:
	python3 main.py "-f ../data/flash/SS-C.csv"

SS-D:
	python3 main.py "-f ../data/flash/SS-D.csv"

SS-E:
	python3 main.py "-f ../data/flash/SS-E.csv"

SS-F:
	python3 main.py "-f ../data/flash/SS-F.csv"

SS-G:
	python3 main.py "-f ../data/flash/SS-G.csv"

SS-H:
	python3 main.py "-f ../data/flash/SS-H.csv"

SS-I:
	python3 main.py "-f ../data/flash/SS-I.csv"

SS-J:
	python3 main.py "-f ../data/flash/SS-J.csv"

SS-K:
	python3 main.py "-f ../data/flash/SS-K.csv"

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
