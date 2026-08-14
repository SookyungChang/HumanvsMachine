import numpy as np
from hVmFigures.config import Nspectra

def reshape_2d_data(x, y, z):
    sorted_points = sorted(zip(x,y,z))
    x, y, z = zip(*sorted_points)
    new_x, new_y = np.unique(x), np.unique(y)
    new_z = np.reshape(np.copy(z), (len(new_x), len(new_y)))
    return new_x, new_y, new_z

def summary_prepro(Smock, Smodel):                     
    Nsimulation = len(Smodel)  
                 # total simulation points in the thermal parameter space
    Smodel_mean = []
    for i in range(Nsimulation):
        Smodel_mean.append(np.mean(Smodel[i], axis=0))
    Smodel_mean = np.array(Smodel_mean)

    Sn = {'Smock': Smock, 'Smodel_mean': Smodel_mean}
    return Sn