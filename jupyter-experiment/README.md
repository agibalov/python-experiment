# jupyter-experiment

* `pipenv install && pipenv shell` to install the dependencies
* `jupyter notebook hello.ipynb` to launch it and open the notebook in the browser
* `jupyter nbconvert --execute --to html hello.ipynb --output-dir ./out` to render to HTML
* `jupyter nbconvert --execute --to pdf hello.ipynb --output-dir ./out` to render to PDF (on Ubuntu 18.04 this requires `texlive-xetex`)
* `jupyter nbconvert --execute --to markdown hello.ipynb --output-dir ./out` to render to Markdown
* `jupyter lab` to launch JupyterLab
