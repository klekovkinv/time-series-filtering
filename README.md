# Time series filtering algorithms

Here we consider the following algorithms:
* Moving average
* Exponential moving average
* One Euro 

This repository contains code for the Medium post, there you can read about filtering algorithms 
([link](https://medium.com/deelvin-machine-learning/time-series-filtering-algorithms-a-brief-overview-af2d3112cd03)).

#### Data and filters visualization
To visualize algorithms we took 450 points on the interval [0, 15],  
calculated a sinusoid on them (original data) and added Gaussian noise to it (noisy data).  
For each filtering algorithm, we filter the noisy data and visualize the resulting signal   
along with the original and the noisy sine wave.   

Operation of moving average filter:
<p>
    <img src="https://raw.githubusercontent.com/klekovkinv/time-series-filtering/main/images/moving-average-w-50.png" width="600" height="320">
<p/>

Operation of exponential moving average filter:
<p>
    <img src="https://raw.githubusercontent.com/klekovkinv/time-series-filtering/main/images/exponential-moving-average-alpha-0.05.png" width="600" height="320">
<p/>

Operation of one Euro filter:
<p>
    <img src="https://raw.githubusercontent.com/klekovkinv/time-series-filtering/main/images/one-euro-f_cmin-0.3-beta-0.07.png" width="600" height="320">
<p/>


All visualizations are in this file: `./visualize_filters.ipynb`  
Implementation of algorithms: `src/time_series_filtering.py`  
