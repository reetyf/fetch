# Hailey Weinschenk Fetch Rewards Hiring Assingment November 3, 2022

This project was created for the assignment [here](https://fetch-hiring.s3.amazonaws.com/machine-learning-engineer/image-coordinates.html) as a part of [Fetch Rewards](https://www.fetchrewards.com/careers) hiring process.

The application is hosted at this address: https://6GXUPVRXW6A67APZ.anvil.app/BNIXWBZZ5HOB2JUFRCM77ROH.

This app's functionality is contingent on a script being run on my personal computer. This should not be an issue as this will be perpetually running, but if for any reason there is an "anvil.server.UplinkDisconnected" Error, please contact me and I will restart the script.
Instructions for running: 
- 1. Type in coordinates and dimensions.
- 2. Click run. A plotly graph should be displayed, ensure pop-ups are allowed.
- 3. Type a 3-tuple in the 'search' text box and click enter for a point you want to locate. 

This app calculates and displays the coordinates of evenly spaced pixels of a rectangle, given the dimensions and corner coordinates of the rectangle. Firstly, the user inputs are verified (corners are checked for forming a rectangle and the dimensions of the rectangle's dots must be integers), then the required increments are calculated. Finally, the solution points are found using these increments, and saved to a 3-D numpy array and plotted using a Plotly Express scatterplot.
##### NOTE: because of numpy's notation quirks, the solution array is of 3 dimensions representing (depth, rows, cols). Counterintuitively, this corresponds to (z, y, x). This should be noted when searching for individual solution values. 


This application and linked script is dynamic - differing user inputs for these values and is able to be rerun in the sample instance. 


This app was built with [anvil](anvil.works), a browser based Python web app builder. For posterity purposes, the anvil app code is viewable above. This application is able to interact with a script on my personal computer through the use of [anvil-uplink](https://anvil.works/docs/uplink). Because of this, no requirements for different packages are needed for the client side app users as long as they have the web app link. 

There is a consistent error during runtime, which I was unable to quell. It is caused by some interaction from passing the plotly object back to the app server, but is negligible to graph results. 
