# Documentation

Create a virtual environment
```
mkvirtualenv pkpd-tutorial -p python3
```

Install requirements
```
pip install -r requirements.txt --upgrade
pip install ipykernel
pip install jupyterlab
```

Register a kernel
```
sudo python -m ipykernel install --name pkpd-tutorial
```