# Public Traffic Analysis Tool
A python script that identifies the most high-traffic locations in Lviv based on public transport data from an external website. May help find best places for commercial purposes (e.g. retail) 

### Features
- Asynchronous data fetching
- Data parsing into structured tables
- High-traffic locations are identified based on the number of vehicles per week
- Analysis also accounts for vehicles that are not on route every day (e.g. only on weekends)
- Clustering multiple stops together if they are very close (e.g. less than 50 meters away) 
- Bar chart generation for top high-traffic location
- Interactive, draggable map generated with colored markers to show top locations
- Logging for info, warning and error messages

### Installation guide
1. Clone the repository

  ### Technologies used
  - Python 3.9
  - requests - for data fetching
  - pandas - for data analysis
  - matplotlib - for chart visualisation
  - folium - for map visualization
    
