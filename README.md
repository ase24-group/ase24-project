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

We are proposing alternate acquisition functions that incorporates exploitation in the later stages of the SMO algorithm rather than selecting new samples solely based on "interestingness".
* `progressive`
* `SimAnnealing`
* `ExpProgressive`

## Running experiments on `flash`
To run our methods and generate results:
```bash
python3 -m venv .venv
pip install -r requirements.txt
cd src
make -j 8
```

All the results will be written into:
| Folder                | Content                                          |
|-----------------------|--------------------------------------------------|
| `results/sk/flash`    | Scott Knott results                              |
| `results/stats/flash` | Intermediate results for Scott Knott             |
| `results/plots/flash` | Graphical plots for select acquisition functions |

## Comparing experiments
Once the results are generated, the acquisition functions can be compared by running a Scott Knott analysis on their ranks across all datasets. This may be done by:
```bash
cd src
make ranks
```

Here is the result of `make ranks`, which places `SimAnnealing_sqrt` above all other SMO variants:
```
#
 0,             rand_p90,  0.00,  0.00, *                   |                   ,  0.00,  8.00
#
 1,    SimAnnealing_sqrt,  1.00,  1.00,      *----          |                   ,  0.00,  8.00
#
 2,       SimAnnealing_9,  2.00,  1.00,           *----     |                   ,  0.00,  8.00
 2,      SimAnnealing_15,  2.00,  2.00,      -----*----     |                   ,  0.00,  8.00
 2,              b2_sqrt,  2.00,  2.00,      -----*----     |                   ,  0.00,  8.00
 2,                b2_15,  2.00,  1.00,           *----     |                   ,  0.00,  8.00
 2,  ExpProgressive_sqrt,  2.00,  2.00,      -----*----     |                   ,  0.00,  8.00
 2,                 b2_9,  2.00,  1.00,           *----     |                   ,  0.00,  8.00
 2,            bonr_sqrt,  2.00,  1.00,      -----*         |                   ,  0.00,  8.00
#
 3,     progressive_sqrt,  2.00,  2.00,      -----*----     |                   ,  0.00,  8.00
#
 4,               bonr_9,  3.00,  2.00,           -----*----|                   ,  0.00,  8.00
 4,     ExpProgressive_9,  3.00,  2.00,           -----*----|                   ,  0.00,  8.00
 4,       progressive_15,  3.00,  2.00,      ----------*    |                   ,  0.00,  8.00
 4,        progressive_9,  3.00,  2.00,           -----*----|                   ,  0.00,  8.00
#
 5,              bonr_15,  3.00,  1.00,           -----*    |                   ,  0.00,  8.00
 5,    ExpProgressive_15,  3.00,  1.00,           -----*    |                   ,  0.00,  8.00
#
 6,                 base,  5.00,  3.00,                -----|----*----          ,  0.00,  8.00
 6,            rand_sqrt,  5.00,  3.00,                -----|----*----          ,  0.00,  8.00
#
 7,              rand_15,  5.00,  2.00,                     |----*----          ,  0.00,  8.00
 7,               rand_9,  6.00,  2.00,                     |    -----*----     ,  0.00,  8.00
```