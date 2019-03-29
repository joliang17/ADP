#%%
import pandas as pd
import numpy as np

Origin_Data = pd.read_csv('ganxian.csv', encoding='GB2312')

Origin_Data

#%%
Origin_Data.groupby(['订单编号']).size()

#%% 
Spec = Origin_Data[Origin_Data['订单编号']==10038043]
Spec

#%%
Spec2 = Spec[-Spec.duplicated()]
Spec2

#%%
len(Spec2)

#%%
from datetime import datetime
Spec2.loc[:,'订单到达时间'] = Spec2['订单到达时间'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
Spec2

#%%
Spec2
#%% 
Spec2['订单到达时间']
#%%


Spec2.sort_values(by="订单到达时间")
Spec2