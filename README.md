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

We are proposing an alternative acquisition function that incorporates exploitation in the later stages of the SMO
algorithm rather than selecting new samples solely based on "interestingness".

### Progressive SMO algorithm
i) budget0 rows are put in ‘lite’ and the rest are put in ‘dark’
ii) Sort the rows in ‘lite’ in the increasing order of their d2h values
Repeat steps iii) to v) Budget times:
iii) First √n data rows are assigned to best and the remaining rows are put in rest
iv) Append to ‘past_best_d2hs’ the row in ‘best’ that is closest to heaven
v) If less 85% of the SMO iterations are complete, use the progressive scoring function to select the next sample to move from dark to lite. Else, simply pick the sample that is most likely to belong to ‘best’. 
vi) Return the row with the least distance to heaven.

### Progressive Scoring function
A weighted average between the exploitation function `(b)`and the exploration function `((b+r)/(b-r))` is taken. The weights are calculated based on the rate of change of the d2h values and the d2h values themselves.
