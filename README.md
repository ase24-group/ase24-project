# ase24-project

This repo houses the end semester project for CSC 591 (Automated Software Engineering), Group 17, Spring 2024 @ NC State

## Group Members

<table>
  <tr>
    <td align="center"><a href="https://github.com/ron-matt163"><img src="https://avatars.githubusercontent.com/u/56034964?v=4" width="75px;" alt=""/><br /><sub><b>Rohan Joseph Mathew</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/jwgerlach00"><img src="https://avatars.githubusercontent.com/u/57069011?v=4" width="75px;" alt=""/><br /><sub><b>Jacob Gerlach</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/tackyunicorn"><img src="https://avatars.githubusercontent.com/u/26558907?v=4" width="75px;" alt=""/><br /><sub><b>Joshua Joseph</b></sub></a></td>
  </tr>
</table>

We are proposing an alternate acquisition function, `FOCUS` that adaptively    shifts from exploration to exploitation as more  data is collected. Unlike standard   acquisition functions like `UCB`, `FOCUS` makes no use of standard deviations or means. This makes it run an order of magnitude faster and scale better for larger problems.

## Running experiments on a single machine

To run our methods and generate results:

```bash
python3 -m venv .venv
pip install -r requirements.txt
cd src
make DATADIR=../data/cat_a_b
```

## Running experiments on an HPC cluster

You may also run our experiments as a slurm job:

```bash
cd src
sbatch job.config
```

Once the job has completed, generate the results using:

```bash
find ../data/cat_a_b -maxdepth 1 -type f | xargs -I{} python3 results.py {}
```

All the results will be written into:
| Folder | Content |
|-------------------------|--------------------------------------------------|
| `results/sk/cat_a_b`    | Scott Knott results |
| `results/stats/cat_a_b` | Intermediate results for Scott Knott |
| `results/plots/cat_a_b` | Graphical plots for select acquisition functions |

## Comparing experiments

Once the results are generated, the acquisition functions can be compared using the following script:

```bash
cd src
./rq.sh > ../results/sk/cat_a_b/rq.out
```
