pkpd-course: A python introduction to PK/PD models
===================================================
Matthias König, `https://livermetabolism.com <https://livermetabolism.com>`__

The introductory lecture is available here



<a href="https://docs.google.com/presentation/d/e/2PACX-1vQG8vtoCVWW3yOQFczrevLZmluhHrKpGVztJho-SY-nbTis8XNYNQyZ3src6AkrL5n3Sv2F6tlL3Fyu/pub?start=false&loop=false&delayms=3000" target="_blank">
    <img src="./presentation/presentation.png" height="150"/>
</a>


This course provides resources for a simple introduction to PK/PD models
using a `caffeine` physiological-based whole body model.

The course contains the following information::

./notebooks: tutorial notebooks
./presentation: introductory presentation
./literature: relevant literature

Installation
============
We need an environment with the libraries listed in `requirements.txt`
These are standard python libraries and `libroadrunner` for simulation of SBML models.

Conda
-----
The easiest way to use this tutorial is to use conda/bioconda.

After installation add the additional library `libroadrunner` via::

    pip install libroadrunner

Virtualenv
----------

One possible solution is to setup a virtual environment with all system dependencies.

Create a virtual environment via::

    mkvirtualenv pkpd-course

Install requirements::

    (pkpd-course) pip install -r requirements.txt --upgrade
    (pkpd-course) pip install ipykernel jupyterlab

Register the virtualenv as a kernel::

    python -m ipykernel install --user --name pkpd-course



Funding
=======
Matthias König is supported by the Federal Ministry of Education and Research (BMBF, Germany)
within the research network Systems Medicine of the Liver (**LiSyM**, grant number 031L0054), 
by the German Research Foundation (DFG) within the Research Unit 
Programme FOR 5151 "QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex 
Resection - A Systems Medicine Approach)" by grant number 436883643 and by grant no. 465194077 
(Priority Programme SPP 2311, Subproject SimLivA).

License
=======

* Source Code: `LGPLv3 <http://opensource.org/licenses/LGPL-3.0>`__
* Documentation: `CC BY-SA 4.0 <http://creativecommons.org/licenses/by-sa/4.0/>`__

© 2018-2022 Matthias König
