import pandas as pd
import numpy as np

#path_to_outpatient_data = 'path.csv'
#outpatient_data = pd.read_csv(path_to_outpatient_data)
outpatient_data = pd.read_csv('/Users/lauren/pre_sales/input_tables/outpatient_cpts_365.csv')
outpatient_data['proc_id'] = outpatient_data.index
outpatient_data = outpatient_data.replace(np.nan, -999)
for col in range(0, 7):
    outpatient_data[outpatient_data.columns[col]] = outpatient_data[outpatient_data.columns[col]].astype(int).astype(str)

hoag_prices_raw = pd.read_csv('/Users/lauren/pre_sales/input_tables/carrum_cpt_hoag_prices.csv')
hoag_prices_raw['CPT_2'] = hoag_prices_raw['CPT_2'].replace(np.nan, -999)
hoag_prices_raw['CPT_2'] = hoag_prices_raw['CPT_2'].astype(int).astype(str)
hoag_prices_raw['CPT_1'] = hoag_prices_raw['CPT_1'].astype(str)

#first select only distinct hoag procedures
hoag_prices_rev = hoag_prices_raw.loc[hoag_prices_raw['CPT_2'] == '-999']
hoag_prices = hoag_prices_rev[['CPT_1', 'carrum_price']]
hoag_prices = hoag_prices.drop_duplicates(keep='first')

out_cpt1 = pd.merge(outpatient_data, hoag_prices, how= 'left', left_on=['cpt_1'], right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt1.rename(columns = {'carrum_price':'carrum_price_1'}, inplace=True)
#out_cpt1.to_csv('/Users/lauren/pre_sales/32bj/output/out_cpt1.csv')

out_cpt2 = pd.merge(outpatient_data, hoag_prices, how= 'left', left_on='cpt_2', right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt2.rename(columns = {'carrum_price':'carrum_price_2'}, inplace=True)
out_cpt2 = out_cpt2[['proc_id','carrum_price_2']]
out12 = pd.merge(out_cpt1, out_cpt2, on='proc_id', how='outer')
#out12.to_csv('/Users/lauren/pre_sales/32bj/output/check.csv')

out_cpt3 = pd.merge(out12, hoag_prices, how= 'left', left_on='cpt_3', right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt3.rename(columns = {'carrum_price':'carrum_price_3'}, inplace=True)

#out123 = pd.merge(out, out_cpt2, on='proc_id', how='outer')

out_cpt4 = pd.merge(out_cpt3, hoag_prices, how= 'left', left_on='cpt_4', right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt4.rename(columns = {'carrum_price':'carrum_price_4'}, inplace=True)

out_cpt5 = pd.merge(out_cpt4, hoag_prices, how= 'left', left_on='cpt_5', right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt5.rename(columns = {'carrum_price':'carrum_price_5'}, inplace=True)

out_cpt6 = pd.merge(out_cpt5, hoag_prices, how= 'left', left_on='cpt_6', right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt6.rename(columns = {'carrum_price':'carrum_price_6'}, inplace=True)

out_cpt7 = pd.merge(out_cpt6, hoag_prices, how= 'left', left_on='cpt_7', right_on='CPT_1', suffixes=["_out", "_hoag"])
out_cpt7.rename(columns = {'carrum_price':'carrum_price_7'}, inplace=True)


out_cpt7 = out_cpt7[['proc_id', 'cpt_1','cpt_2', 'cpt_3', 'cpt_4', 'cpt_5', 'cpt_6', 'cpt_7','total_cost - mean', 'patient_cost - mean', 'Episode Count','carrum_price_1', 'carrum_price_2', 'carrum_price_3', 'carrum_price_4', 'carrum_price_5', 'carrum_price_6', 'carrum_price_7']]

out_cpt7['highest_cost'] = out_cpt7[['carrum_price_1', 'carrum_price_2', 'carrum_price_3', 'carrum_price_4', 'carrum_price_5', 'carrum_price_6', 'carrum_price_7']].max(axis=1)

costs = pd.DataFrame(np.sort(out_cpt7[['proc_id','carrum_price_1', 'carrum_price_2', 'carrum_price_3', 'carrum_price_4', 'carrum_price_5', 'carrum_price_6', 'carrum_price_7']].values)[:,-8:], columns=['id','7th-largest','6th-largest','5th-largest','4th-largest','3nd-largest', '2nd-largest','largest'])

costs['id'] = costs['id'].astype(int)

out_final_costs = pd.merge(out_cpt7, costs, left_on='proc_id', right_on='id')


out_final_costs.loc[(((out_final_costs['cpt_1'] == 29888) & (out_final_costs['cpt_2'] == 29882)) | ((out_final_costs['cpt_1'] == 29882) & (out_final_costs['cpt_2'] == 29888))), 'final_cost'] = 14700
out_final_costs.loc[(((out_final_costs['cpt_1'] == 29888) & (out_final_costs['cpt_2'] == 29883)) | ((out_final_costs['cpt_1'] == 29883) & (out_final_costs['cpt_2'] == 29888))), 'final_cost'] = 14700

out_final_costs.loc[(((out_final_costs['cpt_1'] == 22632) & (out_final_costs['cpt_2'] == 63048)) | ((out_final_costs['cpt_1'] == 63048) & (out_final_costs['cpt_2'] == 22632))), 'final_cost'] = 39000
out_final_costs.loc[(((out_final_costs['cpt_1'] == 63047) & (out_final_costs['cpt_2'] == 22630)) | ((out_final_costs['cpt_1'] == 22630) & (out_final_costs['cpt_2'] == 63047))), 'final_cost'] = 31800

out_final_costs['estimated_paid_amounts'] = out_final_costs['total_cost - mean'] - out_final_costs['patient_cost - mean']

out_final_costs.loc[out_final_costs['3nd-largest'].notnull(), 'final_cost'] = out_final_costs['3nd-largest'] + (.5 * out_final_costs['4th-largest']) + (.25 *  out_final_costs['5th-largest']) + (.25 *  out_final_costs['6th-largest']) + (.25 *  out_final_costs['7th-largest'])
out_final_costs.loc[(out_final_costs['3nd-largest'].isnull()) & (out_final_costs['4th-largest'].notnull()), 'final_cost'] = out_final_costs['4th-largest'] + (.5 * out_final_costs['5th-largest']) + (.25 *  out_final_costs['6th-largest']) + (.25 *  out_final_costs['7th-largest'])
out_final_costs.loc[(out_final_costs['4th-largest'].isnull()) & (out_final_costs['5th-largest'].notnull()), 'final_cost'] = out_final_costs['5th-largest'] + (.5 * out_final_costs['6th-largest']) + (.25 *  out_final_costs['7th-largest'])
out_final_costs.loc[(out_final_costs['5th-largest'].isnull()) & (out_final_costs['6th-largest'].notnull()), 'final_cost'] = out_final_costs['6th-largest']  + (.5 * out_final_costs['7th-largest'])
out_final_costs.loc[(out_final_costs['6th-largest'].isnull()) & (out_final_costs['7th-largest'].notnull()), 'final_cost'] = out_final_costs['7th-largest']

hoag_table = out_final_costs.loc[out_final_costs['final_cost'].notnull()]

hoag_table.to_csv('/Users/lauren/pre_sales/non_claims_presales/input/outpatient_annual_costs.csv')
