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
cd src
make -j 8
```

All the results will be written into:
| Folder                | Content                                          |
|-----------------------|--------------------------------------------------|
| `results/sk/flash`    | Scott Knott results                              |
| `results/stats/flash` | Intermediate results for Scott Knott             |
| `results/plots/flash` | Graphical plots for select acquisition functions |
