#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler


# In[2]:

rr = pd.read_csv('time_series_covid19_recovered_global.csv', sep=',')
rr.set_index(['Country/Region','Province/State'],inplace=True)
rr2 = rr._drop_labels_or_levels(['Lat','Long'])

# In[3]:

# read csv:
#df = pd.read_csv('time_series_19-covid-Confirmed.csv', sep=';', index_col=0,keep_default_na=False).T
df = pd.read_csv('time_series_covid19_confirmed_global.csv', sep=',')
# re-set the index (row headers):
df.set_index(['Country/Region','Province/State'],inplace=True)
df2 = df._drop_labels_or_levels(['Lat','Long'])

# In[*]

#remove spurious last column:
#df2b = dfX.loc[:, ~df2.columns.str.contains('^Unnamed')]

# transpose:
rr3 = rr2.T
df3 = df2.T

# In[7]:


# convert index to dateTime:
df3.index = pd.DatetimeIndex(df3.index)
rr3.index = pd.DatetimeIndex(rr3.index)


# In[8]:

for jj in range(rr3.index.size):
    df3.iloc[:,jj] -= rr3.iloc[:,jj]

# In[*]:


# extract regions we are interested in:
df6 = df3.loc[:,[
    ('China','Hubei'),
    ('China','Beijing'),
    ('Germany',''),
    ('Italy',''),
    ('Japan',''),
    ('France',np.nan),
#    ('China','Anhui'),
    ('Switzerland',''),
    ('Singapore',''),
    ('Korea, South',''),
    ('Poland',''),
    ("US","Washington"),
    ("Spain",""),
    ("Austria",""),
    ("Sweden",""),
    ("Norway",""),
    ("South Africa","")
]]
df6.tail(3)


# In[9]:


# divide by population density.  first had this via separate csv files, 
# but the "countries" are not stable in the upstream data
df6.loc[:,('China','Beijing')] /= 22.
df6.loc[:,('China','Hubei')] /= 60.
df6.loc[:,('Japan',np.nan)] /= 126.8
df6.loc[:,('Korea, South',np.nan)] /= 52.
df6.loc[:,('Singapore',np.nan)] /= 5.85
df6.loc[:,('France',np.nan)] /= 67.
df6.loc[:,('Germany',np.nan)] /= 82.79
df6.loc[:,('Italy',np.nan)] /= 60.5
df6.loc[:,('Switzerland',np.nan)] /= 8.57
df6.loc[:,('Poland',np.nan)] /= 4.
df6.loc[:,('US',np.nan)] /= 328.
#df6.loc[:,("US","King County, WA")] /= 2.2
df6.loc[:,("Spain",np.nan)] /= 47.
df6.loc[:,("Austria",np.nan)] /= 8.8
df6.loc[:,("Sweden",np.nan)] /= 10.2
df6.loc[:,("Norway",np.nan)] /= 5.4
df6.loc[:,("South Africa",np.nan)] /= 56.8
df6.tail(3)


# In[10]:


# time-shifted Hubei values:
hb = df6["China","Hubei"]
hb.index = pd.date_range(start="2020-03-07",periods=hb.size)
hb.name=("China","Hubei time-shifted")
hb.tail(3)


# In[11]:


df6b = pd.concat([df6,hb],axis=1) #.fillna(value=0)
# mar/12 data looks faulty especially in Europe:
df6b.drop(index=pd.to_datetime('2020-03-12'),inplace=True)
# mar/23 data looks faulty (same as day before):
#df6b.drop(index=pd.to_datetime('2020-03-23'),inplace=True)
#df6b.loc['2020-03-10':'2020-03-15',:]


# In[12]:


germany = df6b['Germany']


# In[13]:
fact = 1

fit = pd.Series(fact*0.3*np.exp(np.arange(0,90,1)*np.log(2.)/2.8))
fit.index = pd.date_range(start="2020-02-22",periods=fit.size)
combinedTmp = pd.concat([germany,fit],axis=1)


# In[14]:


fit = pd.Series(fact*16.0*np.exp(np.arange(0,90,1)*np.log(2.)/5.))
fit.index = pd.date_range(start="2020-03-1",periods=fit.size)
combinedTmp2 = pd.concat([combinedTmp,fit],axis=1)


# In[*]:


fit = pd.Series(fact*85*np.exp(np.arange(0,90,1)*np.log(2.)/9.))
fit.index = pd.date_range(start="2020-03-1",periods=fit.size)
combinedTmp3 = pd.concat([combinedTmp2,fit],axis=1)


# In[15]:


# we have approx 14k IC beds for Germany.  div 80 is 175 per 1 mio inhab.  Assuming that 1% of _measured_ cases
# progress to IC level, overload starts at 17500 cases per 1 mio inhab.  This somewhat optimistic since they 
# stay there for 10 days,
# but on the other hand, if the curve was flat, then it would still just be the share of "infected" cases that 
# needs IC. (To cleanly account for the 10 days, we would need to plot _new_ cases.)
fit = pd.Series(fact*(0*np.arange(0,90,1)+17500))
fit.index = pd.date_range(start="2020-03-1",periods=fit.size)
combined = pd.concat([combinedTmp3,fit],axis=1)


# In[16]:


plt.close('all')
plt.rcParams['figure.figsize']=[12,7]
default_cycler = (cycler(color=['r', 'g', 'b', 'y']) +
                  cycler(linestyle=['', '-', ':', '-.']) +
                  cycler(marker=['o','','','']))
plt.rc('lines', linewidth=1)
plt.rc('axes', prop_cycle=default_cycler)
plotGermany = combined.plot(kind='line',
                     logy=True,ylim=(0.1,20000),xlim=("2020-02-22","2020-06-01"),
                    grid=True)
plt.show()

# In[17]:


default_cycler = (cycler(color=['blue','orange','green','red','purple','brown','pink'
                                ,'gray','olive','cyan',
                               'blue','orange','green','red','purple','brown','pink'
                                ,'gray','olive','cyan']) +
                  cycler(linestyle=['-','-','-','-','-','-','-','-','-','-',
                                   '--','--','--','--','--','--','--','--','--','--']) +
                  cycler(marker=['','','','','','','','','','','','','','','','','','','','']))
plt.rc('axes', prop_cycle=default_cycler)
plt.rc('lines', linewidth=2)
df6b.plot(kind='line',logy=True,ylim=(10,2500),xlim=('2020-02-15','2020-04-15'),grid=True)
plt.show()


# In[18]:


df6b.diff().rolling(2).mean().plot(kind='line',ylim=(0.01,200),xlim=("2020-03-15","2020-04-05"))
plt.show()


# In[ ]:



#
#
# # In[ ]:
#
#
# df6.loc[:,('Poland',np.nan)].to_string()
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# df6.loc[:,('Poland',np.nan)]
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# df5.loc[:,('Mainland China','Anhui')] /= 9999999.
# df5.head(3)
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# df5.to_csv("all.csv")
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# df6['idx'] = df6.reset_index().index
# df6.tail(3)
#
#
# # In[ ]:
#
#
# df6.to_csv("reduced.csv",sep='\t',header=False)
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# get_ipython().run_line_magic('pinfo', 'df6.iterrows')
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# hb = df6["Mainland China"]["Hubei"]
# hb.index = pd.date_range(start="2020-02-22",periods=hb.size)
# hb.head(3)
#
#
# # In[ ]:
#
#
# get_ipython().set_next_input('hb.index = pd.DatetimeIndex');get_ipython().run_line_magic('pinfo', 'pd.DatetimeIndex')
#
#
# # In[ ]:
#
#
# pd.date_range(start="2020-01-22",periods=5)
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# fit = pd.Series(np.exp(np.arange(0,10,1)/8))
# fit.index = pd.date_range(start="2020-02-22",periods=fit.size)
# fit
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
# 3.9*np.log(10.)
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
#
# # In[ ]:
#
#
#
#
