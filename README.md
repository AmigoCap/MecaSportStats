# Characterization of Space and Time-Dependence of 3-Point Shots in Basketball
The main objective of this project is to use space occupation models to temporally and spatially characterize 3-point shots. In particular, we are introducing a new way to quantify the opening of shots.

## Code and details

* The notebook [1_Introduction_to_space_occupation](https://nbviewer.jupyter.org/github/AmigoCap/MecaSportStats/blob/master/1_Introduction_to_space_occupation.ipynb) introduces way of quantifying court occupation by basketball players.
* [2_time_calculation](https://nbviewer.jupyter.org/github/AmigoCap/MecaSportStats/blob/master/2_Time_calculation.ipynb) where we detail dynamic motion model and how to calcul time needed for a player to go from a point a to b with a given initial velocity.
* [3_Comparison_of_ways_to_quantify_free_space](https://nbviewer.jupyter.org/github/AmigoCap/MecaSportStats/blob/master/3_Comparison_of_ways_to_quantify_free_space.ipynb) in which the comparison of occupancy calculations is taken further and in which a new way to quantify how "free" a player is is introduced.
* [4_Free_space_and_3-points_efficiency](https://nbviewer.jupyter.org/github/AmigoCap/MecaSportStats/blob/master/4_Free_space_and_3-points_efficiency.ipynb) in which we focus on 3-points shot and the link between efficiency and free-space.
* [Animation and analysis of a Klay Thompson catch-and-shoot shot](https://amigocap.github.io/MecaSportStats/video.mp4)

## Work performed

### Publication

[**Article**](http://www.sloansportsconference.com/wp-content/uploads/2020/02/Rolland_characterization_of_Space_and_Time-Dependece_of_3-Point_Shots_in_Basketball.pdf)

[**MIT Sloan Sports Analytics Conference 2020 Poster**](https://github.com/AmigoCap/MecaSportStats/blob/master/MIT_Sloan_sports_Analytics_Conference_Poster.pdf)

### Abstract and key results

Understanding characteristics of 3-point shots is paramount for modern basketball success, as in recent decades, 3-point shots have become more prevalent in the NBA. They accounted for 33,6% of the number of total shots in 2017-2018, compared to only 3% in 1979-1980. In this paper, we aim at better understanding the connections between the type of 3-point shooting (catch-and-shoots and pull-ups) and the timing for shooting, using two distinct space-time models of player motion. Those models allow us to identify individual behavior as a function of specific defensive settings, e.g. shot-behavior when a player is guarded closely.

1. **Space occupation models**
We developped two space occupation models : a static one, i.e. only considering players' position, and a dynamic one including players' velocity and direction. By calculating space occupation for each point of the court we were able to determine occupation maps.

![space occuaption maps](https://github.com/AmigoCap/MecaSportStats/blob/master/images/github_occupation_maps.png "space occuaption maps")

2. **Free space evolution before 3-point shots**
By calculating the evolution of 3-point shooters' free space before the shot we’ve highlighted 3 behaviors :

* Pull-ups => global decrease as the shooter dribbles
* Catch-and-shoot 1 : the shooter is already free for a long time (usually from corners).
* Catch-and-shoot 2 : the shooter has to move to free himself to receive the ball  

![free space](https://github.com/AmigoCap/MecaSportStats/blob/master/images/github_free_space.png "free space")

3. **Do players adjust their release time (delay between catching the ball and releasing it) to the free space they have at catch time ?**

Korver does not seem to adapt his release time to the free space he has at catch time, while Matthews, Nowitzki or Thompson clearly take more time if they are more free when they catch the ball.

![individual behavior](https://github.com/AmigoCap/MecaSportStats/blob/master/images/t_recep_release.jpg "individual behavior")

4. **Analysis of a Klay Thompson catch-and-shoot shot**

Let’s analyse a Klay Thompson catch-and-shoot shot where he has to free himself from his defender to be able to receive the ball. 

![Klay](https://github.com/AmigoCap/MecaSportStats/blob/master/images/github_thompson.png "Klay Thompson")

[Animation and analysis of a Klay Thompson catch-and-shoot shot](https://amigocap.github.io/MecaSportStats/video.mp4)

## Data

The dataset we use is derived from ***Stats*** company data and *SportsVU* technology. These are the 632 men's basketball games in the NBA during 2015-2016 season. For each match we have the movement data for the ball and players taken 25 times per second and stored in the form _JavaScript Object Notation_ (JSON). You can download the data from [this GitHub repository](https://github.com/linouk23/NBA-Player-Movements/tree/master/data/2016.NBA.Raw.SportVU.Game.Logs). The following figure shows the general structure of the data:  

![dataschema](https://github.com/AmigoCap/MecaSportStats/blob/master/images/data.jpg "data schema")

## Authors

* Gabin Rolland : gabs.rol43@gmail.com, [LinkedIn](https://www.linkedin.com/in/gabin-rolland/), [Twitter](https://twitter.com/GabinRolland)
* Romain Vuillemot : romain.vuillemot@ec-lyon.fr
* Wouter Bos : wouter.bos@ec-lyon.fr
* Nathan Rivière : nathan.riviere@ecl17.ec-lyon.fr

## How to cite

If you find this work useful, please consider using the follwing citing template:

    @inproceedings{rolland:hal-02482706,
        TITLE = {Characterization of Space and Time-Dependence of 3-Point Shots in Basketball},
        AUTHOR = {Gabin Rolland, Romain Vuillemot, Wouter Bos, Nathan Rivière},
        URL = {https://hal.archives-ouvertes.fr/hal-02482706},
        BOOKTITLE = {{MIT Sloan Sports Analytics Conference}},
        ADDRESS = {Boston, United States},
        YEAR = {2020},
        MONTH = Mar,
        PDF = {https://hal.archives-ouvertes.fr/hal-02482706/file/characterization_of_Space_and_Time-Dependece_of_3-Point_Shots_in_Basketball.pdf},
        HAL_ID = {hal-02482706},
        HAL_VERSION = {v1},
        }
