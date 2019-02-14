# Logs

## Tom, 13/12/2018

- Add flags for weekdays/weekends 
- Look at ratio of cars between lanes see if any correlation between variables
- Flag what junction points are between
- Mark points of interest(Airport,NEC)
- Get airport data
- Look for shape trends for days of the week for given areas

## 30/11/2018, interim report

### Eloisa

- Wrote the code to load in the initial one day data and group by geographic address/time so the data was in smaller, more manageable subsets. 
- Tried to plot data using seaborn module, but this plotted the data in the wrong order (reason for this is unclear). Resorted to using matplotlib instead.
- Plotted graph of geographic address vs speed, then created a widget to move through the different times of day. However, this is difficult to use.
- Plotted two variables against each other, eg flow and occupancy, and used KMeans clustering to classify this data into 3 different categories. However, as this data followed more of a normal distribution, the clustering was not very effective. 
- Wrote the code to concatenate the separate month data csvs into one big dataframe.
- Created a function to average variables across lanes.
- Used Facebook Prophet to create an ARIMA model to predict future traffic flow. Currently working on testing the accuracy of this. 
- Defined “congested” as any speeds less than 60mph, then created a boolean bar graph, which showed the percentage of congestion by time over all geographic addresses. 
- Plotted average occupancy per day for the month data
- Plotted speed per minute for a 24 hour period, averaged over the month. 
- Plotted occupancy and flow against time to check for a dependency between the two

### Titus

- Took the base of Tom / Eloisa’s initial plotting code and cleaning it up a bit by fitting it into functions 
- Made a few additions to said functions; including arguments to be able to specify a time, sensor range to plot, and dynamic changing of subplot size depending on number of sensors given
- (Attempt at manual version control)
- Worked off Eloisa’s “Help.py” file; I generalised the code by turning it into functions (- again). 
- Used said functions to make plots of occupancy and speed vs all given individual sensors (with flagged in-out slip road sensors). 
- Ran these functions in a loops to save the figures for all times, and then put them together into a video format using ffmpeg.