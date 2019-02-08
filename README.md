# MWayComms dataset

To use this repository, clone it and run the files / analysis of interest.

## File organisation

All data files should be placed in the *"data"* folder, and so all code should target this folder. Natural Earth map data for use with geopandas has been placed in *"maps"* and weather data provided by Eloisa has been placed in *"weather"*

I've set up .gitignore files to ignore the data files as well as any produced results.

**DO NOT** push data files to the repository.

Happy coding! :+1:

## 5/2/2019 Meeting

### Report due W12/13

* report is aimed to client
* Shouldn't be extremely complicated, if something interesting is made we should be able to pass it along to any given layperson

### Talk / presentation feedback

* Be more rehearsed next time
* Lack of structure
* Unsureness as to how to phrase parts of the presentation

### Tasklist/objectives:

* More context
* multi-directional/ different aspects of the problem at once
* Differentiating weekends and weekdays
* Mapping
* Looking at distributions of speed or other measures, as opposed to means/averages
* Characteristic distributions for particular days/ times/ junctions/ sensors

### Types of distribution

* Stable distributions
* Normal -> Central limit theorem
* Levy distribution -> appears in nature a lot
* Skew kertosis
* Look at more distributions online

## Tasklist (3/12/2018)

* Merge everything in a more coherent way, i.e splitting functions and different types of analysis into different folders and modules.
* Look into principal component analysis during winter break
* Incorporate weather data from Jamie

### *Eloisa: some ideas*

* Flow, over or under some threshold, possibility of speed being some other threshold ? + other variables
* Facebook prophet - comparison between self-made model and prophet model

### Summary of existing work done:

#### Titus

* Animation of plots into .avi

#### Tom

* Bunch of plots (avg_speed vs time), (flow over time), total number of cars, comparison across carriageways.

#### Eloisa

* Initial data read-in into python pandas (similar to R)
* Facebook prophet analysis: comparison to own code
