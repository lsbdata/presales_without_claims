import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

data = pd.read_csv('non_claims_presales/input/Tripoint/tripoint_census.csv')

col = 'DOB'
data[col] = pd.to_datetime(data[col])
future = data[col] > date(year=2020,month=1,day=1)
data.loc[future, col] -= timedelta(days=365.25*100)

data['age'] = ((datetime.now() - data['DOB']).astype('timedelta64[D]')) / 365.25
data['age'] = (data['age'].round()).astype(int)

data = data.loc[data['age']>= 18].copy()

data['age_categories'] = pd.cut(data['age'], [18, 44, 64, 84], labels=['18-44', '45-64', '65-84'])

data['gender_female'] = np.where((data['Gender']== 'Female'), 1, 0)
data['gender_male'] = np.where(data['gender_female'] == 0, 1, 0)
data['over_45'] = np.where(data['age_categories'] == '45-64', 1, 0)

data.age.loc[data['gender_female']==0].mean()
data.age.loc[data['gender_female']==1].mean()

data['male_less_45'] = np.where((data['gender_male']==1) & (data['over_45']==0), 1, 0)
data['female_less_45'] = np.where((data['gender_female']==1) & (data['over_45']==0), 1, 0)
data['male_plus_45'] = np.where((data['gender_male']==1) & (data['over_45']==1), 1, 0)
data['female_plus_45'] = np.where((data['gender_female']==1) & (data['over_45']==1), 1, 0)

emp_dist = data.groupby('State').agg({'Zip': 'count', 'over_45': 'sum', 'gender_female': 'sum', 'gender_male': 'sum', 'female_plus_45': 'sum', 'male_plus_45': 'sum', 'female_less_45': 'sum', 'male_less_45': 'sum',}).reset_index().rename(columns={'Zip': 'Estimated Adult Lives', 'over_45' : '45 and older', 'gender_female' : 'Female Subscribers' , 'gender_male' : 'Male Subscribers'})

emp_dist['total_female'] = emp_dist['Female Subscribers']
emp_dist['total_male'] = emp_dist['Male Subscribers']
emp_dist['total_male_less_45'] = emp_dist['male_less_45']
emp_dist['total_female_less_45'] = emp_dist['female_less_45']
emp_dist['total_male_plus_45'] = emp_dist['male_plus_45']
emp_dist['total_female_plus_45'] =  emp_dist['female_plus_45']

emp_dist['percent_45_plus'] = emp_dist['45 and older']/emp_dist['Estimated Adult Lives']

emp_data = emp_dist[['State', 'total_male', 'total_female', 'total_male_less_45', 'total_female_less_45', 'percent_45_plus', 'total_male_plus_45', 'total_female_plus_45', 'Estimated Adult Lives']]
emp_data.to_csv('/Users/lauren/non_claims_presales/output/Tripoint/employee_demographics.csv')
