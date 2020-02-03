# MecaSportStats
The main objective of this project is to use motion model to temporally and spatially characterize 3-point shots. 

## Work performed

* The notebook [1_Introduction_to_space_occupation](https://github.com/AmigoCap/MecaSportStats/blob/master/1_Introduction_to_space_occupation.ipynb) introduces way of quantifying court occupation by basketball players.
* [2_time_calculation](https://github.com/AmigoCap/MecaSportStats/blob/master/2_Time_calculation.ipynb) where we detail dynamic motion model and how to calcul time needed for a player to go from a point a to b with a given initial velocity.
* [3_Comparison_of_ways_to_quantify_free_space](https://nbviewer.jupyter.org/github/AmigoCap/MecaFootCo/blob/master/3_Comparison_of_ways_to_quantify_free_space.ipynb) in which the comparison of occupancy calculations is taken further and in which a new way to quantify how "free" a player is is introduced.
* [4_Free_space_and_3-points_efficiency](https://nbviewer.jupyter.org/github/AmigoCap/MecaFootCo/blob/master/4_Free_space_and_3-points_efficiency.ipynb) in which we focus on 3-points shot and the link between efficiency and free-space.

## Data

The dataset we use is derived from ***Stats*** company data and *SportsVU* technology. These are the 632 men's basketball games in the NBA during 2015-2016 season. For each match we have the movement data for the ball and players taken 25 times per second and stored in the form _JavaScript Object Notation_ (JSON). The following figure shows the general structure of the data:  
![dataschema](https://github.com/AmigoCap/MecaFootCo/blob/master/Images/data.jpg "data schema")

## Contact

* Gabin Rolland : gabs.rol43@gmail.com
* Romain Vuillemot : romain.vuillemot@ec-lyon.fr
* Wouter Bos : wouter.bos@ec-lyon.fr
* Nathan Rivière : nathan.riviere@ecl17.ec-lyon.fr
