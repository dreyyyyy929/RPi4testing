import numpy as np
a = np.full((16,1),0)
print(a)
b = np.full((16,8),1)
print(np.concatenate((a,b),axis=1))