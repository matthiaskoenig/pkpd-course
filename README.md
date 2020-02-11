# pkpd-tutorial


## Installation
We need an environment with the libraries listed in `requirements.txt`
These are standard python libraries and `libroadrunner` for simulation of SBML models.

### Virtualenv
One possible solution is to setup a virtual environment with all system dependencies.
Create a virtual environment
```
mkvirtualenv pkpd-tutorial --python=python3.7
```

Install requirements
```
pip install -r requirements.txt --upgrade
pip install ipykernel jupyterlab
```

Register a kernel
```
sudo python -m ipykernel install --name pkpd-tutorial
```