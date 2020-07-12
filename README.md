# dash-pathway
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecell/dash-pathway/master?filepath=notebooks)
[![PyPI version](https://badge.fury.io/py/dash-pathway.svg)](https://badge.fury.io/py/dash-pathway)

A dash component for pathway visualization, wrapped around [dash-cytoscape](https://github.com/plotly/dash-cytoscape)

![demo](./dash-pathway-demo.gif)

## Getting Started in JupyterLab

### Prerequisites
Make sure that dash and jupyter dependent libraries are correctly installed:
```
conda install pandas pip
conda install -c conda-forge jupyterlab
conda install -c conda-forge -c plotly jupyter-dash
```

### Usage
Install the library using `pip`:
```
pip install dash-pathway
```

Run the following command in your terminal to run JupyterLab:
```
jupyter lab
```

Run the following cell inside JupyterLab cell: (This reproduces the visualization like animated gif at the beginning.)
```
from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_pathway

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(id='pathway-body', children=[
    dash_pathway.KeggScape(pathwayid="eco00020", width=1200, height=1200,
                           node_style={"font-size":14}, edge_style={"width":10.0})
])

app.run_server()
```

### Advanced Usage
dash-pathway not only allows you to visualize pathways, but also maps and integrates data into pathways.

In the example below, we have mapped the quantitative values of a compound's time series onto KEGG global metabolism map.
The size of compound nodes in the metabolism map increase or decrease in size depending on the amount of the mapped quantitative value.
And we used the dash slider component to change the quantitative value of each time series.

This allows us to determine how the abundance of compounds in which pathway function changes over time.

```
```
