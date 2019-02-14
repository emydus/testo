# Meeting notes

## 12/2/2019 Meeting

### Weather/ geomapping

- Not everything needs to be done thoroughly, can just be done as proof of concept (with regards to maps)
- Search for "weird days" --> quantify things
- Weather --> effect on distributions
- Localized effects...?
  - Analyse a particular sensor over time

### Visualization

- More plotting software / mapping (3D-plots, animation, putting it on a map) 
  - Plotly / Bokeh / Geomapping but more fancy

### Predictive modelling

- Predictions based on congestion
  - congestion level should be a function of;
    - time,
    - previous sensors,
    - speeds.
- Thresholds? Critical points? What processes are chaotic and which are easily predicatable? 
- Chaotic processes (rogue / dangerous drivers, freak accidents) 
  - aim to quantify a form of probability that these will spontaneously cause an accident.

### Current course of action:

- Isolate ranges of congestion, ranges leading up to congestion, ranges of no interest
- This means:
  - Defining congestion
  - Classifying ranges of congestion
  - Building a model
    - What parameters should be used?
    - After constructing the model,
      - Testing against our intuition (do we think this range is "congested"?)
      - How reliable is the model overall?
- Use of linear correlation on sections?

## 5/2/2019 Meeting

### Report due W12/13

- Report is aimed to client
- Shouldn't be extremely complicated, if something interesting is made we should be able to pass it along to any given layperson

### Talk / presentation feedback

- Be more rehearsed next time
- Lack of structure
- Unsureness as to how to phrase parts of the presentation

### Tasklist/objectives

- More context
- multi-directional/ different aspects of the problem at once
- Differentiating weekends and weekdays
- Mapping
- Looking at distributions of speed or other measures, as opposed to means/averages
- Characteristic distributions for particular days/ times/ junctions/ sensors

### Types of distribution

- Stable distributions
- Normal -> Central limit theorem
- Levy distribution -> appears in nature a lot
- Skew kertosis
- Look at more distributions online