#%%
import numpy as np

#%%
Vehnum = 6
packnum = 8
stopnum = 6
column1 = bnds=np.array((np.zeros(Vehnum),np.ones(Vehnum))).T

column1

#%%
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
x

#%%
x1 = x[:6]
x1

#%%
x1.reshape((2,3))

#%%
x2 = x[6:]
x2