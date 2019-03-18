import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

prospect = raw_input("Please enter the prospective client name: ")
prospect = str(prospect)

client = raw_input("Please enter path to client census data: ")
client = str(client)

data = pd.read_csv(client)

col = 'DOB'
data[col] = pd.to_datetime(data[col])
future = data[col] > date(year=2020,month=1,day=1)
data.loc[future, col] -= timedelta(days=365.25*100)

data['age'] = ((datetime.now() - data['DOB']).astype('timedelta64[D]')) / 365.25
data['age'] = (data['age'].round()).astype(int)

data = data.loc[data['age']>= 18].copy()

plt.hist(data['age'])
plt.show()

data.State.describe()

#data.loc[data['State'].isnull(), 'State'] = 'CO'

print data.groupby('State').agg({'State' : 'count'}).sort_values(by=['State'], ascending=False)

regions = pd.read_csv('pre_sales/non_claims_presales/input/state_regions.csv')

data_regions = pd.merge(data, regions, how='left', left_on = 'State', right_on = 'state_code')

print data_regions.groupby('sub_region').agg({'sub_region' : 'count'}).sort_values(by=['sub_region'], ascending=False)
print data_regions.groupby('region').agg({'region' : 'count'}).sort_values(by=['region'], ascending=False)

data_regions['age_categories'] = pd.cut(data_regions['age'], [18, 44, 64, 84], labels=['18-44', '45-64', '65-84'])

data_regions['gender_female'] = np.where((data_regions['Gender']== 'Female'), 1, 0)
#data_regions['gender_female'] = np.where((data_regions['Gender']== 'F'), 1, 0)

data_regions['gender_male'] = np.where(data_regions['gender_female'] == 0, 1, 0)
data_regions['over_45'] = np.where(data_regions['age_categories'] == '45-64', 1, 0)


#when no dependent info is there
dep_data = data_regions.loc[(data_regions['Tier'] == 'EE + Family') | (data_regions['Tier'] == 'EE + SP')].copy()

dep_data['gender_female'] = np.where(dep_data['gender_female'] == 1, 0, 1)
dep_data['gender_male'] = np.where(dep_data['gender_male'] == 1, 0, 1)
dep_data['Relationship Code'] = 'Spouse'

all_data = pd.concat([data_regions, dep_data], ignore_index=True)
all_data['Relationship Code'] = all_data['Relationship Code'].replace(np.nan, 'Employee')



print 'Mean Gender (female): ', all_data['gender_female'].mean()

all_data['male_less_45'] = np.where((all_data['gender_male']==1) & (all_data['over_45']==0), 1, 0)
all_data['female_less_45'] = np.where((all_data['gender_female']==1) & (all_data['over_45']==0), 1, 0)
all_data['male_plus_45'] = np.where((all_data['gender_male']==1) & (all_data['over_45']==1), 1, 0)
all_data['female_plus_45'] = np.where((all_data['gender_female']==1) & (all_data['over_45']==1), 1, 0)


print 'Distributions:'
print all_data.describe()

#emp_dist = all_data.groupby('State').agg({'Zip': 'count', 'over_45': 'sum', 'gender_female': 'sum', 'gender_male': 'sum', 'female_plus_45': 'sum', 'male_plus_45': 'sum', 'female_less_45': 'sum', 'male_less_45': 'sum',}).reset_index().rename(columns={'Zip': 'Estimated Adult Lives', 'over_45' : '45 and older', 'gender_female' : 'Eligible Women' , 'gender_male' : 'Eligible Men'})

all_data.to_csv('/Users/lauren/pre_sales/non_claims_presales/input/' + prospect + '/zayo_data_modified.csv')


emp_dist = all_data.groupby('State').agg({'DOB': 'count', 'over_45': 'sum', 'gender_female': 'sum', 'gender_male': 'sum', 'female_plus_45': 'sum', 'male_plus_45': 'sum', 'female_less_45': 'sum', 'male_less_45': 'sum',}).reset_index().rename(columns={'DOB': 'Estimated Adult Lives', 'over_45' : '45 and older', 'gender_female' : 'Eligible Women' , 'gender_male' : 'Eligible Men'})


emp_dist['total_female'] = emp_dist['Eligible Women']
emp_dist['total_male'] = emp_dist['Eligible Men']
emp_dist['total_male_less_45'] = emp_dist['male_less_45']
emp_dist['total_female_less_45'] = emp_dist['female_less_45']
emp_dist['total_male_plus_45'] = emp_dist['male_plus_45']
emp_dist['total_female_plus_45'] =  emp_dist['female_plus_45']

emp_dist['percent_45_plus'] = emp_dist['45 and older']/emp_dist['Estimated Adult Lives']

emp_data = emp_dist[['State', 'total_male', 'total_female', 'total_male_less_45', 'total_female_less_45', 'total_male_plus_45', 'total_female_plus_45', 'percent_45_plus', 'Estimated Adult Lives']]
emp_data.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/employee_demographics.csv')
