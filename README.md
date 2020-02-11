# pkpd-tutorial


## Installation
We need an environment with the libraries listed in `requirements.txt`
These are standard python libraries and `libroadrunner` for simulation of SBML models.

### Virtualenv
One possible solution is to setup a virtual environment with all system dependencies.
Create a virtual environment
```
mkvirtualenv pk-tutorial --python=python3.7
```

Install requirements
```
(pk-tutorial) pip install -r requirements.txt --upgrade
(pk-tutorial) pip install ipykernel jupyterlab
```

Register a kernel
```
python -m ipykernel install --user --name pk-tutorial
```