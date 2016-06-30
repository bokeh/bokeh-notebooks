# Bokeh Tutorial

## Setup

### Clone or download the repo

    $ git clone https://github.com/bokeh/bokeh-notebooks.git

Or download from: https://github.com/bokeh/bokeh-notebooks/archive/master.zip

### Install the dependencies

This tutorial has been tested on:
* bokeh=0.12.0
* pandas=0.18
* ipython-notebook=4.0.4
* ipywidgets=4.1.1

Other combinations may work also. Packages are available via PyPI and anaconda.org.

#### Installing with anaconda

Install [anaconda](http://continuum.io/downloads)

Anaconda should come with all the dependencies included, but you may need to update your versions.

#### Install with miniconda

Install [miniconda](http://conda.pydata.org/miniconda.html).

Use the command line to create an environment and install the packages:

    $ conda create -n bokeh_tutorial python=3.4
    $ source activate bokeh_tutorial
    $ conda install bokeh pandas ipython-notebook ipywidgets

#### Install with pip

We recommend creating a virtual environment.

    $ pip install bokeh pandas "ipython[notebook]" ipywidgets

### Get the sample data

Bokeh has a sample data download that gives us some data to build demo visualizations. To get
it run:

    $ bokeh sampledata

### Install datashader and holoviews (optional)

Optional tutorials 11 and 12 require the datashader and holoviews packages,
respectively, which can be installed with:

    $ conda install datashader
    $ conda install -c holoviews/label/dev holoviews
   
### Run Jupyter/IPython notebook

From this folder run jupyter notebook, and open the `00-intro.ipynb` notebook.

    $ jupyter notebook
