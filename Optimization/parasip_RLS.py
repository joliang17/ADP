import numpy as np
import matplotlib.pylab as plt
import padasip as pa 

# creation of data
N = 1
x = np.array([[0.2, 0.3]])
w1 = np.array([0.1, 0.3])
# v = np.random.normal(0, 0.1, N) # noise
# d = 2*x[:,0] + 0.1*x[:,1] - 4*x[:,2] + 0.5*x[:,3] + v # target
d = np.array([2.0])

# identification
f = pa.filters.FilterRLS(n=2, mu=0.98, eps=0.2, w=w1)
y, e, w = f.run(d, x)

# show results
plt.figure(figsize=(15,9))
plt.subplot(211);plt.title("Adaptation");plt.xlabel("samples - k")
plt.plot(d,"b", label="d - target")
plt.plot(y,"g", label="y - output");plt.legend()
plt.subplot(212);plt.title("Filter error");plt.xlabel("samples - k")
plt.plot(10*np.log10(e**2),"r", label="e - error [dB]");plt.legend()
plt.tight_layout()
plt.show()