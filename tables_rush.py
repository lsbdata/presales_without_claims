import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

#Parameters
utilization = 1.0
avoidance_rate = 0.23
travel = 3000
avoidance_dollars = 2500

prospect = raw_input("Please enter the prospetive client name: ")

client_pop_size = raw_input("Please enter number of total people in client population: ")
client_pop_size = int(client_pop_size)

employee_pop_size = raw_input("Please enter number of client employees: ")
employee_pop_size = int(employee_pop_size)
print '\n'

#join all three tables so there is one row per procedure, demographic, drg group, and state
costs = pd.read_csv('pre_sales/non_claims_presales/output/bhi_470_costs.csv', header=[2, 3, 4])
costs.columns = costs.columns.map('_'.join)
costs_long = pd.melt(costs, id_vars=['demographic_group_procedure_drg_group'], value_vars=list(costs.columns)[1:], var_name='procedure_demographic', value_name='estimated_unit_costs')
costs_long.rename(columns={'demographic_group_procedure_drg_group':'state'}, inplace=True)

carrum_prices = pd.read_csv('pre_sales/non_claims_presales/output/estimated_carrum_prices.csv', header=[2, 3, 4])
carrum_prices.columns = carrum_prices.columns.map('_'.join)
carrum_prices_long = pd.melt(carrum_prices, id_vars=['demographic_group_procedure_drg_group'], value_vars=list(carrum_prices.columns)[1:], var_name='procedure_demographic', value_name='estimated_carrum_price')
carrum_prices_long.rename(columns={'demographic_group_procedure_drg_group':'state'}, inplace=True)
###above pricing csvs need to have some output reconfigured (get rid of header, make state first column, drop 2 columns in pricing related to Carrum_Price)

incidence_table = pd.read_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/his_estimates.csv')
incidence_table = incidence_table.loc[incidence_table['State'].notnull()]

#incidence_table.columns = incidence_table.columns.str.replace('_estimate', '')
incidence_table.drop(['Unnamed: 0', 'Estimated Adult Lives'], axis=1, inplace=True)
#incidence_table_long = pd.wide_to_long(incidence_table, stubnames=['female_plus_45_upper_', 'female_less_45_', 'male_plus_45_upper_', 'male_less_45_'], i='State', j='estimated_incidence')
incidence_table_long = pd.melt(incidence_table, id_vars=['State'], value_vars=list(incidence_table.columns)[1:], var_name='procedure_demographic', value_name='estimated_incidence')
incidence_table_long["procedure_demographic"] = incidence_table_long["procedure_demographic"].str.replace('_estimate', '')
incidence_table_long.rename(columns={'State':'state'}, inplace=True)


incidences_costs = pd.merge(incidence_table_long, costs_long, on=['state', 'procedure_demographic'])

incidences_costs_prices = pd.merge(incidences_costs, carrum_prices_long, on=['state', 'procedure_demographic'])

data_eps = incidences_costs_prices.loc[incidences_costs_prices['estimated_incidence']!=0].copy()
data_eps['DRGs'] = data_eps['procedure_demographic'].str.split("_").str[-1]

#over-write prices for the state of IL###
real_carrum_prices = pd.read_csv('/Users/lauren/pre_sales/input_tables/carrum_drg_prices_nebh.csv', header=0, low_memory=False)


########DRG summary table########
drg_agg = data_eps.groupby('DRGs').agg({'estimated_incidence': 'sum', 'estimated_unit_costs': 'mean'}).reset_index()
drg_agg['Incidence Rate'] = drg_agg['estimated_incidence'].astype(float)/client_pop_size * 100

drg_group_list = drg_agg['DRGs'].unique()

real_carrum_prices = real_carrum_prices.loc[real_carrum_prices['DRGs'].isin(drg_group_list)]

for i in drg_group_list:
    drg_agg.loc[drg_agg['DRGs']== i, 'estimated_carrum_price'] = real_carrum_prices['rush_price_category'].loc[real_carrum_prices['DRGs']==i].min()

drg_agg['Unit Savings'] = drg_agg['estimated_unit_costs'] - drg_agg['estimated_carrum_price']
drg_agg['Percent Savings'] = (drg_agg['Unit Savings'] / drg_agg['estimated_unit_costs']) * 100

wm_percent_savings = np.average(drg_agg['Percent Savings'], weights=drg_agg['estimated_incidence'])
wm_savings = np.average(drg_agg['Unit Savings'], weights=drg_agg['estimated_incidence'])

print 'IP DRG Summary Statistics: '
print "Overall IP Annual Incidence Rate (~0.4-0.6%): ", drg_agg['Incidence Rate'].sum()
print "DRG 470 Annual Incidence Rate (~0.3%): ",  (drg_agg['Incidence Rate'].loc[drg_agg['DRGs'] == '469-470']).values.round(2)
print "WA % Savings (~20-40%): ",  (wm_percent_savings).round(2)
print "WA $ Savings (~$5-$15K): ",  (wm_savings).round(2)
print '\n'

drg_agg.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/drg_table.csv')


########State table########
drg_state_agg = data_eps.groupby(['DRGs', 'state']).agg({'estimated_incidence': 'sum', 'estimated_unit_costs': 'mean', 'estimated_carrum_price': 'mean'}).reset_index()
drg_state_agg['Incidence Rate'] = drg_state_agg['estimated_incidence'].astype(float)/client_pop_size * 100

drg_group_list = drg_state_agg['DRGs'].unique()

for i in drg_group_list:
    drg_state_agg.loc[drg_state_agg['DRGs']== i, 'estimated_carrum_price'] = real_carrum_prices['rush_price_category'].loc[real_carrum_prices['DRGs']==i].min()

drg_state_agg['Unit Savings'] = drg_state_agg['estimated_unit_costs'] - drg_state_agg['estimated_carrum_price']
drg_state_agg['Percent Savings'] = (drg_state_agg['Unit Savings']/ drg_state_agg['estimated_unit_costs'])*100

state_wm_percent_savings = np.average(drg_state_agg['Percent Savings'], weights=drg_state_agg['estimated_incidence'])
state_wm_savings = np.average(drg_state_agg['Unit Savings'], weights=drg_state_agg['estimated_incidence'])

print 'IP State/DRG Summary Statistics: '
print "Overall IP Annual Incidence Rate (~0.4-0.6%): ", drg_state_agg['Incidence Rate'].sum()
print "DRG 470 Annual Incidence Rate (~0.3%): ",  drg_state_agg['Incidence Rate'].loc[drg_state_agg['DRGs'] == '469-470'].sum()
print "WA % Savings (~20-40%): ",  (state_wm_percent_savings).round(2)
print "WA $ Savings (~$5-$15K): ",  (state_wm_savings).round(2)
print '\n'

drg_state_agg['Carrum Txn'] = drg_state_agg['estimated_incidence'] * utilization
drg_state_agg['Carrum Avoid'] = (drg_state_agg['Carrum Txn'] * avoidance_rate).round(0)
drg_state_agg['Carrum Surgeries'] = (drg_state_agg['Carrum Txn'] - drg_state_agg['Carrum Avoid']).round(0)
drg_state_agg['Proc Savings'] = (drg_state_agg['Carrum Surgeries'] * (drg_state_agg['Unit Savings'] - travel)).round(2)
drg_state_agg['Avoid Savings'] = (drg_state_agg['Carrum Avoid'] * (drg_state_agg['estimated_unit_costs'] - avoidance_dollars)).round(2)
drg_state_agg['Total Savings'] = (drg_state_agg['Proc Savings'] + drg_state_agg['Avoid Savings']).round(2)

print 'Total inpatient savings', drg_state_agg['Total Savings'].sum()
print '\n'

drg_state_agg.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/state_table.csv')



##############Outpatient###############
out_data = pd.read_csv('pre_sales/non_claims_presales/input/outpatient_annual_template.csv')
out_data['Estimated Episode Count'] = np.round((out_data['incidence_rate']/100) * float(client_pop_size), 0)

out_data_eps = out_data.loc[out_data['Estimated Episode Count']!=0].copy()

out_data_eps['Incidence Rate'] = out_data_eps['Estimated Episode Count'].astype(float)/client_pop_size * 100
out_data_eps['Unit Savings'] = out_data_eps['Total Episode Cost (mean)'] - out_data_eps['Carrum Price']
out_data_eps['Percent Savings'] = (out_data_eps['Unit Savings']/ out_data_eps['Total Episode Cost (mean)'])*100

out_data_eps['Carrum Txn'] = out_data_eps['Estimated Episode Count'] * utilization
out_data_eps['Carrum Avoid'] = (out_data_eps['Carrum Txn'] * avoidance_rate).round(0)
out_data_eps['Carrum Surgeries'] = (out_data_eps['Carrum Txn'] - out_data_eps['Carrum Avoid']).round(0)
out_data_eps['Proc Savings'] = (out_data_eps['Carrum Surgeries'] * (out_data_eps['Unit Savings'] - travel)).round(2)
out_data_eps['Avoid Savings'] = (out_data_eps['Carrum Avoid'] * (out_data_eps['Total Episode Cost (mean)'] - avoidance_dollars)).round(2)
out_data_eps['Total Savings'] = (out_data_eps['Proc Savings'] + out_data_eps['Avoid Savings']).round(2)

print 'Total outpatient savings', out_data_eps['Total Savings'].sum()
print '\n'

one_year_net_savings = drg_state_agg['Total Savings'].sum() + out_data_eps['Total Savings'].sum()


out_data_eps.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/outpatient_cpt_summary.csv')

out_cat_agg = out_data_eps.groupby('Procedure Category').agg({'Estimated Episode Count': 'sum', 'Total Episode Cost (mean)': 'mean', 'Carrum Price': 'mean'}).reset_index()
out_cat_agg['Incidence Rate'] = out_cat_agg['Estimated Episode Count'].astype(float)/client_pop_size * 100
out_cat_agg['Unit Savings'] = out_cat_agg['Total Episode Cost (mean)'] - out_cat_agg['Carrum Price']
out_cat_agg['Percent Savings'] = (out_cat_agg['Unit Savings']/ out_cat_agg['Carrum Price'])*100

out_cat_agg['Carrum Txn'] = out_cat_agg['Estimated Episode Count'] * utilization
out_cat_agg['Carrum Avoid'] = (out_cat_agg['Carrum Txn'] * avoidance_rate).round(0)
out_cat_agg['Carrum Surgeries'] = (out_cat_agg['Carrum Txn'] - out_cat_agg['Carrum Avoid']).round(0)
out_cat_agg['Proc Savings'] = (out_cat_agg['Carrum Surgeries'] * (out_cat_agg['Unit Savings'] - travel)).round(2)
out_cat_agg['Avoid Savings'] = (out_cat_agg['Carrum Avoid'] * (out_cat_agg['Total Episode Cost (mean)'] - avoidance_dollars)).round(2)
out_cat_agg['Total Savings'] = (out_cat_agg['Proc Savings'] + out_cat_agg['Avoid Savings']).round(2)

out_wm_percent_savings = np.average(out_cat_agg['Percent Savings'], weights=out_cat_agg['Estimated Episode Count'])
out_wm_savings = np.average(out_cat_agg['Unit Savings'], weights=out_cat_agg['Estimated Episode Count'])

print 'OP Summary Statistics: '
print "Overall OP Annual Incidence Rate (~2%): ", out_cat_agg['Incidence Rate'].sum()
print "WA % Savings (~5-20%): ",  (out_wm_percent_savings).round(2)
print "WA $ Savings (~$5-8K): ",  (out_wm_savings).round(2)
print '\n'

print 'One Year Net OP + IP Savings: ', one_year_net_savings
print '\n'

out_cat_agg.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/outpatient_category_summary.csv')

out_proc_agg = out_data_eps.groupby('cpt_desc_list').agg({'Estimated Episode Count': 'sum', 'Total Episode Cost (mean)': 'mean', 'Carrum Price': 'mean'}).reset_index()
out_proc_agg['Incidence Rate'] = out_proc_agg['Estimated Episode Count'].astype(float)/client_pop_size * 100
out_proc_agg['Unit Savings'] = out_proc_agg['Total Episode Cost (mean)'] - out_proc_agg['Carrum Price']
out_proc_agg['Percent Savings'] = (out_proc_agg['Unit Savings']/ out_proc_agg['Carrum Price'])*100
out_proc_agg.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/outpatient_procedure_summary.csv')

##############Annualized Table##############

annual_projections = pd.DataFrame({"Achievable Savings": [one_year_net_savings, one_year_net_savings,one_year_net_savings,one_year_net_savings,one_year_net_savings], "Eligibile EE": [employee_pop_size,employee_pop_size,employee_pop_size,employee_pop_size,employee_pop_size], "Utilization": [0.15, 0.20, 0.30, 0.40, 0.50], "Incidence Growth": [0, 0.20, 0.20, 0.20, 0.20], "Compounding Growth Constant": [1.00, 1.20, 1.44, 1.73, 2.07], "Carrum Subscription": [1.00, 1.50, 2.00, 2.00, 2.00]})


annual_projections['Total Net Savings'] = (annual_projections['Achievable Savings'] * annual_projections['Utilization'] * annual_projections['Compounding Growth Constant']).round(0)
annual_projections['PEPY Savings'] = (annual_projections['Total Net Savings']/annual_projections['Eligibile EE']).round(2)
annual_projections['PEPM Savings'] = (annual_projections['PEPY Savings']/12).round(2)
annual_projections['True Net Savings PEPM'] = (annual_projections['PEPM Savings'] - annual_projections['Carrum Subscription']).round(2)
annual_projections['True Net Savings PEPY'] = (annual_projections['True Net Savings PEPM']*12).round(2)
annual_projections['Subsciption ROI'] = (annual_projections['True Net Savings PEPM']/annual_projections['Carrum Subscription']).round(1)

annual_projections_t = annual_projections.T

annual_projections_t.rename(columns = {0: 'Year 1', 1: 'Year 2', 2: 'Year 3', 3: 'Year 4', 4: 'Year 5'}, inplace=True)

annual_projections_t.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/annual_emp_savings.csv')
