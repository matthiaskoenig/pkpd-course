#!/usr/bin/env python
# coding: utf-8

# # Pharmacokinetics Tutorial
# For questions contact konigmatt@googlemail.com. The latest version of the resources are available from https://github.com/matthiaskoenig/pkpd-course/releases

# ## Check requirements
# This tutorial works in a minimal python environment with the following package
# ```
# numpy
# scipy
# matplotlib
# pandas
# libroadrunner
# ```
# 
# The packages can be installed via
# ```
# pip install numpy scipy matplotlib pandas libroadrunner
# ```
# or in `conda` via
# ```
# conda install numpy scipy matplotlib pandas libroadrunner
# ```
# 
# The only new requirement for this tutorial is `libroadrunner`

# In[11]:


# some magic
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[12]:


import roadrunner


# In[13]:


# general imports for ode integration
import numpy as np
import pandas as pd
import roadrunner
from matplotlib import pylab as plt
from pprint import pprint

# global settings for plots (optional)
plt.rcParams.update({
        'axes.labelsize': 'large', 
        'axes.labelweight': 'bold',
        'axes.titlesize': 'large',
        'axes.titleweight': 'bold',
        'legend.fontsize': 'small',
        'xtick.labelsize': 'large',
        'ytick.labelsize': 'large',
    })


# ## Whole-body physiological based pharmacokinetics (PBPK) model for caffeine
# The model describes clearance of caffeine by the liver in Humans.
# 
# * Caffeine and the primary metabolite paraxanthine are removed from the blood stream by hepatic or renal clearance.
# * Caffeine can be applied either as intra-venous injection or by oral dose in the model
# 
# This notebook demonstrates some simple use cases and analysis of the model.
# 
# ![Fig.1 Caffeine PKPD Model](figures/caffeine_pkpd.png)

# ## Load the caffeine model
# The full model report with information about the parameter names is available at

# In[14]:


from helpers import *
print(caffeine_model)

# load the model
r = roadrunner.RoadRunner(caffeine_model)
# set variables in result
r.timeCourseSelections = ["time"] + r.model.getFloatingSpeciesIds() + r.model.getGlobalParameterIds()
# pprint(r.timeCourseSelections)


# The model is an SBML model and you can inspect the corresponding file and HTML report. This will provide a good overview over the content of the model.

# ## Example simulation
# We now simulate a 100 [mg] oral dose (p.o) of caffeine. 
# In a first step we perform this simulation and look at some state variables of the model.
# 
# The model time is in [h]. The simulation result is a pandas DataFrame which can easily be accessed.

# In[27]:


# reset model to initial state
r.reset(roadrunner.SelectionRecord.ALL)

# set the oral dose
r['init(PODOSE_caf)'] = 100  # [mg]
r['init(BW)'] = 100  # [kg]

# simulate the model for 24[hr]
s = simulate(r, start=0, end=24, steps=500)  # [hr]

# show the resulting DataFrame
display(s.head())


# In[28]:


# plot venous caffeine & paraxanthine concentrations against time
f1, ax1 = plt.subplots(1, 1, figsize=(5, 5))
ax1.plot(s.time, s.Cve_caf, linewidth=2, label="caffeine [mg/l]") # caffeine concentration, venous blood
ax1.plot(s.time, s.Cve_px, linewidth=2, label="paraxanthine [mg/l]")  # paraxanthine concentration, venous blood
ax1.set_title('100 [mg] caffeine (oral dose)')
ax1.set_ylabel('concentration [mg/l]')
ax1.set_xlabel('time [hr]')
ax1.legend()
plt.show()


# ## Compare amounts in different organs
# In the following we compare the amount of caffeine in the different organs.
# For this we select all the columns in the solution which belong the amount of caffeine.

# In[20]:


# plot caffeine and paraxanthine amounts
f1, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
axes = (ax1, ax2)
organs = ["li", "ki", "lu", "sp", "gu", "re"]

for organ in organs:
    sid = f"A{organ}_caf"
    label = f"caffeine ({organ}) [mg]"
    ax1.plot(s.time, s[sid], label=label)    
    
    sid = f"C{organ}_caf"
    label = f"caffeine ({organ}) [mg/l]"
    ax2.plot(s.time, s[sid], label=label)    


ax1.set_ylabel('caffeine [mg]')
ax2.set_ylabel('caffeine [mg/l]')
for ax in axes:
    ax.set_xlabel('time [h]')
    ax.legend()

plt.show()


# ## Plot the organ volumes
# In the following we plot the organ volumes by querying the model. Model variables and parameters are available via the dot syntax (`.`) or the bracket access (`[]`).

# In[21]:


for oid in organs:
    vid = f"V{oid}"
    print(f"V{oid} = {r[vid]} [l]")


# In[22]:


print("relative volume:", r.FVli)
print("relative perfusion:", r.FQh)


# ## Stepwise increase of the caffeine dose
# Now we see what happens if we drink more coffee every day

# In[23]:


doses = np.linspace(0, 500, num=11)
results = []

for dose in doses:
    # reset model to initial state
    r.reset(roadrunner.SelectionRecord.ALL)
    
    # set the oral dose
    r['init(PODOSE_caf)'] = dose  # [mg]

    # simulate the model for 24[h]
    s = simulate(r, start=0, end=24, steps=500)
    results.append(s)

# plot venous caffeine & paraxanthine against time
f1, ax1 = plt.subplots(1, 1, figsize=(5, 5))
for k, s in enumerate(results):
    if k == 1:
        label = "caffeine [mg/l]"
    else:
        label = "__nolabel__"
    ax1.plot(s.time, s.Cve_caf, linewidth=2, color="blue", label=label, alpha=0.8)
    if k == 1:
        label = "paraxanthine [mg/l]"
    else:
        label = "__nolabel__"
    ax1.plot(s.time, s.Cve_px, linewidth=2, color="darkorange", label=label, alpha=0.8)
ax1.set_title('caffeine (oral dose)')
ax1.set_ylabel('concentration')
ax1.set_xlabel('time [h]')
ax1.legend()
plt.show()


# # Exercises
# ## E1 Your caffeine level
# The first exercise is to calculate the timecourse of the expected venous caffeine level after you drink some caffeinated beverage. To estimate your oral dose of caffeine you can estimate the caffeine content from the following chart
# 
# ![Fig.2 Caffeine Content of Beverages](figures/caffeine_levels.jpg)
# 
# The oral dose is defined in the model via parameter `r['init(PODOSE_caf)'] = 100` [mg]. In addition you can also adjust the bodyweight to get a more realistic estimation via the parameter `r['init(BW)'] = 70` [kg].
# 
# * What would be your level of caffeine now, if you had two cups of coffee for breakfast this morning?
# * How would your time course and level of caffeine look if you would take the same amount of caffeine intravenously (I.V)? (Hint: you have to set the set the i.v. dose via `r['init(IVDOSE_caf)'] = 100`)
# * What is the peak time of caffeine in venous blood? What is the peak concentration?

# ## E2 Interindividual variability
# We saw that there is a large variability in caffeine kinetics in the population. Depending on if you are a fast or slow metabolizer of caffeine the timecourses can look very different. In E1 you calculated the mean timecourse for the population. Now we will look at the interindividual differences.
# 
# Your caffeine clearance by the liver depends on the activity of CYP1A2 in the liver, the main enzyme metabolizing caffeine. The activity is defined via the apparent clearance caffeine by hepatic microsomes (`r[init('HLM_CLint_caf')] = 2` [mul/min/mg]).
# 
# * How would your time course / level of caffeine change if you are a slow metabolizer (small apparent clearance), or if you are a fast metabolizer (large apperent clearance)?
# * Simulate the effect of lifestyle changes on your caffeine clearance via adjusting the caffeine clearance accordingly. For instance simulate changes in your coffee intake or smoking habit. An overview over the changes in apparent clearance are given in Tab.1. 
# * How would your caffeine timecourse change if you smoke >20 cigarettes per day and drink 1 liter of coffee (the effects are additive) compared to being abstinent?
# * Also the bodyweight has a strong influence on the distribution of caffeine. What happens when setting your body weight? (`r.BW = 75` [kg]) 
# 
# ![Tab.1 Lifestyle Effects](figures/Tantcheva-Poor1999_Tab4.png)

# In[ ]:




