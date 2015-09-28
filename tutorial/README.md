# Bokeh Tutorial

## Setup

### Clone or download the repo

    $ git clone https://github.com/bokeh/bokeh-notebooks.git

Or download from: https://github.com/bokeh/bokeh-notebooks/archive/master.zip

### Install the dependencies

This tutorial has been tested on:
* bokeh=0.10
* pandas=0.16
* ipython-notebook=4.0.4
* ipywidgets=4.0.3

Other combinations, may work. Packages are availalable via pypi and anaconda.org.

#### Installing with anaconda
Install [anaconda](http://continuum.io/downloads) 

Anaconda should come with all the dependencies included, you may need to update your versions.

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

    $ python -c "import bokeh; bokeh.sampledata.download()"

### Run ipython notebook

From this folder run ipython notebook, and open the `00-intro.ipynb` notebook.

    $ ipython notebook
