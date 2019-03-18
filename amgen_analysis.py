import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

data = pd.read_csv('non_claims_presales/input/amgen_census_cleaned.csv')
#medicare_data = pd.read_csv('non_claims_presales/input/medicare_table.csv')

col = 'date_of_birth'
data[col] = pd.to_datetime(data[col])
future = data[col] > date(year=2020,month=1,day=1)
data.loc[future, col] -= timedelta(days=365.25*100)

data['age'] = ((datetime.now() - data['date_of_birth']).astype('timedelta64[D]')) / 365.25
data['age'] = (data['age'].round()).astype(int)

data['age_categories'] = pd.cut(data['age'], [18, 44, 64, 84], labels=['18-44', '45-64', '65-84'])

data['gender_female'] = pd.to_numeric(data['gender_female'], errors='coerce')

data.age.loc[data['gender_female']==0].mean()

data['over_45'] = np.where(data['age_categories'] == '45-64', 1, 0)
data['gender_male'] = np.where(data['gender_female'] == 0, 1, 0)

data['female_partners'] = np.where((data['gender_female']==0) & (data['adult_coverage']>1), 1, 0)
data['male_partners'] = np.where((data['gender_female']==1) & (data['adult_coverage']>1), 1, 0)

data['male_emp_less_45'] = np.where((data['gender_male']==1) & (data['over_45']==0), 1, 0)
data['female_emp_less_45'] = np.where((data['gender_female']==1.0) & (data['over_45']==0), 1, 0)
data['male_emp_plus_45'] = np.where((data['gender_male']==1) & (data['over_45']==1), 1, 0)
data['female_emp_plus_45'] = np.where((data['gender_female']==1.0) & (data['over_45']==1), 1, 0)

data['male_partner_less_45'] = np.where((data['male_partners']==1) & (data['over_45']==0), 1, 0)
data['female_partner_less_45'] = np.where((data['female_partners']==1) & (data['over_45']==0), 1, 0)
data['male_partner_plus_45'] = np.where((data['male_partners']==1) & (data['over_45']==1), 1, 0)
data['female_partner_plus_45'] = np.where((data['female_partners']==1) & (data['over_45']==1), 1, 0)

emp_dist = data.groupby('State').agg({'adult_coverage': 'sum', 'over_45': 'sum', 'female_partners': 'sum', 'gender_female': 'sum', 'gender_male': 'sum', 'male_partners': 'sum', 'female_emp_plus_45': 'sum', 'male_emp_plus_45': 'sum', 'female_emp_less_45': 'sum', 'male_emp_less_45': 'sum','female_partner_plus_45': 'sum', 'male_partner_plus_45': 'sum', 'female_partner_less_45': 'sum', 'male_partner_less_45': 'sum'}).reset_index().rename(columns={'adult_coverage': 'Estimated Adult Lives', 'over_45' : '45 and older', 'female_partners' : 'Female Spouses', 'male_partners' : 'Male Spouses' , 'gender_female' : 'Female Employees' , 'gender_male' : 'Male Employees'})
#emp_dist.to_csv('/Users/lauren/amgen/employee_demographics.csv')

emp_dist['total_female'] = emp_dist['Female Employees'] + emp_dist['Female Spouses']
emp_dist['total_male'] = emp_dist['Male Employees'] + emp_dist['Male Spouses']
emp_dist['total_male_less_45'] = emp_dist['male_partner_less_45'] + emp_dist['male_emp_less_45']
emp_dist['total_female_less_45'] = emp_dist['female_partner_less_45'] + emp_dist['female_emp_less_45']
emp_dist['total_male_plus_45'] = emp_dist['male_partner_plus_45'] + emp_dist['male_emp_plus_45']
emp_dist['total_female_plus_45'] = emp_dist['female_partner_plus_45'] + emp_dist['female_emp_plus_45']

emp_dist['percent_45_plus'] = emp_dist['45 and older']/emp_dist['Estimated Adult Lives']

emp_data = emp_dist[['State', 'total_male', 'total_female', 'total_male_less_45', 'total_female_less_45', 'percent_45_plus', 'total_male_plus_45', 'total_female_plus_45', 'Estimated Adult Lives']]
emp_data.to_csv('/Users/lauren/non_claims_presales/output/employee_demographics.csv')

'''matched = pd.merge(emp_data, medicare_data, how='left', left_on='State', right_on='state_abbrev')

matched['bariatric_estimate'] = matched['Estimated Adult Lives'] * (matched['bariatric_rate']*20)
matched['female_back_estimate'] = matched['total_female'] * matched['back_female_rate']
matched['male_back_estimate'] = matched['total_male'] * matched['back_male_rate']
matched['female_coronary_estimate'] = matched['total_female'] * matched['coronary_female_rate']
matched['male_coronary_estimate'] = matched['total_male'] * matched['coronary_male_rate']
matched['female_hip_estimate'] = matched['total_female'] * matched['hip_female_rate']
matched['male_hip_estimate'] = matched['total_male'] * matched['coronary_male_rate']
matched['female_knee_estimate'] = matched['total_female'] * matched['knee_female_rate']
matched['male_knee_estimate'] = matched['total_male'] * matched['knee_male_rate']

result = matched[['State','bariatric_estimate', 'female_back_estimate', 'male_back_estimate', 'female_coronary_estimate', 'male_coronary_estimate', 'female_hip_estimate', 'male_hip_estimate', 'female_knee_estimate', 'male_knee_estimate']]

result.to_csv('/Users/lauren/non_claims_presales/output/medicare_estimates.csv')'''
