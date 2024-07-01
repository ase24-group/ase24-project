find ../results/stats/cat_a_b -mindepth 1 -type d | xargs -I{} sh -c 'echo $((111-$(ls {} | wc -l))) {}' | grep -v '^0' | sort -nr
