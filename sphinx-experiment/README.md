# sphinx-experiment

Run `./download-plantuml.sh` before building the docs.

* `pipenv run docs-html` to build HTML docs
* `pipenv run docs-singlehtml` to build a one-page HTML docs
* `pipenv run docs-epub` to build ePub docs
* `pipenv run docs-text` to build text docs
* `./make-pdf.sh` to build PDF (requires `latexmk` on Ubuntu)
* `pipenv run clean` to delete `./build`
