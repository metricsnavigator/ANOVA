# ANOVA: Step-by-Step in Python
# Author: Eric Reschke
# License: Free Use
# Citation: metricsnavigator.com

import numpy as np
import pandas as pd
import scipy.stats as sp

'''
# manual data lists if needed
g1 = [10,9,8,7.5,8.5,9,10,8,8,9]
g2 = [8,9,10,8,8.5,7,9.5,9,7,10]
g3 = [9,8,7,10,9,8,7,10,9,8]
g4 = [11,7,9,10,8.5,9,7,10,9.5,7]
gAll = g1+g2+g3+g4
'''

# establish data from GitHub import
url = (r'https://raw.githubusercontent.com/metricsnavigator/ANOVA/main/data/anova_data.csv')
groupDF = pd.read_csv(url,index_col=False)

# number of groups
groups=0
for cols in groupDF:
    groups+=1

# passing column data to individual groups
g1,g2,g3,g4 = [],[],[],[]

g1 = groupDF.iloc[:,0].tolist()
g2 = groupDF.iloc[:,1].tolist()
g3 = groupDF.iloc[:,2].tolist()
g4 = groupDF.iloc[:,3].tolist()
gAll = g1+g2+g3+g4

# get the total amount of observations
obsCount = len(g1)

# average/mean of each group and complete group
g1_mean = round(np.mean(g1),2)
g2_mean = round(np.mean(g2),2)
g3_mean = round(np.mean(g3),2)
g4_mean = round(np.mean(g4),2)
gAll_mean = round(np.mean(gAll),2)

# between group variation
betweenGroupVar = np.round((obsCount*((g1_mean-gAll_mean)**2)+
                         obsCount*((g2_mean-gAll_mean)**2)+
                         obsCount*((g3_mean-gAll_mean)**2)+
                         obsCount*((g4_mean-gAll_mean)**2)),1)

# within group variation
def wiGroup(group,avg):
    x,y=0,0
    for i in group:
        x=(i-avg)**2
        y+=x
    return(y)

# sum of squared errors
g1_sse = round(wiGroup(g1,g1_mean),1)
g2_sse = round(wiGroup(g2,g2_mean),1)
g3_sse = round(wiGroup(g3,g3_mean),1)
g4_sse = round(wiGroup(g4,g4_mean),1)

withinGroupVar = round((g1_sse+g2_sse+g3_sse+g4_sse),2)

# sum of squares total (SST)
SST = (betweenGroupVar+withinGroupVar)

# significance value
alpha = .05

# degrees of freedom numerator = (# of samples minus 1)
# degrees of freedom denominator = (total values - groups)
# f-critical numerator degree of freedom / denominator degree of freedom
dof_numer = (groups-1)
dof_denom = len(gAll)-groups
f_critical = round(sp.f.ppf((1-alpha),dof_numer,dof_denom),2)

# mean-squares calculations
ms_between = round(betweenGroupVar/dof_numer,4)
ms_within = round(withinGroupVar/dof_denom,4)
f_ratio = round(ms_between/ms_within,4)
p_value = round(sp.f.sf(f_ratio,dof_numer,dof_denom),4)

'''
NULL hypothesis says there is no difference between the means of the groups
(variance between/variance within) <=1 then cannot reject null hypothesis
'''

# is f_ratio<f_critical? if yes, cannot reject NULL hypothesis
if(f_ratio<f_critical):
    print("\n","F_ratio, F-critical and p_value:",f_ratio,",",f_critical,",",p_value,"\n","Cannot reject NULL hypothesis; H0 accepted.","\n")
else:
    print("\n","F_ratio, F-critical and p_value:",f_ratio,",",f_critical,",",p_value,"\n","Reject the NULL hypothesis; H0 rejected.","\n")


## end of script

