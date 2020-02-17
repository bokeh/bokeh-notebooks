Notes for Making Changes
==========================

1. The notebooks need to contain execution output for NBViewer
1. The notebooks should be run in an env created with `conda env create -n bokeh-notebooks -f environment.yml`. Make sure to activate your env with `conda activate bokeh-notebooks` before using or developing the notebooks!
1. Oneliner to run the notebooks `git ls-files -z \*.ipynb | xargs -0 jupyter nbconvert --to notebook --inplace --execute`
1. While working on changes, if you want to strip the output from the notebooks you can `git ls-files -z \*.ipynb | xargs -0  jupyter nbconvert --clear-output`
