import os
import pandas as pd
import roadrunner

dir_name = os.path.dirname(os.path.abspath(__file__))
caffeine_model = os.path.join(dir_name, "model", "caffeine_pkpd_9.xml")


################################
# Simulation Helper Functions
################################
def resetValues(r):
    """ Reset all model variables to CURRENT init(X) values.

    This resets all variables, S1, S2 etc to the CURRENT init(X) values. It also resets all
    parameters back to the values they had when the model was first loaded.

    :param r: roadrunner model
    :return:
    """
    r.reset(roadrunner.SelectionRecord.TIME |
            roadrunner.SelectionRecord.RATE |
            roadrunner.SelectionRecord.FLOATING |
            roadrunner.SelectionRecord.GLOBAL_PARAMETER)


def simulate(r, start=0, end=10, steps=200, reset=True):
    """ Simulate given roadrunner model.

    :param r: roadrunner model
    :param start: start time
    :param end: end time
    :param steps: simulation steps
    :param reset: resets the model after simulation
    :return:
    """
    if reset:
        resetValues(r)
    s = r.simulate(start=start, end=end, steps=steps)
    return pd.DataFrame(s, columns=s.colnames)
