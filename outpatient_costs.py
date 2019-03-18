import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

data = pd.read_csv('non_claims_presales/output/Tripoint/outpatient_estimates.csv')
hoag_prices_raw = pd.read_csv('/Users/lauren/pre_sales/carrum_cpt_hoag_prices.csv')

data['proc_id'] = data.index

hoag_prices_rev = hoag_prices_raw.loc[hoag_prices_raw['CPT_2'].isnull()]
hoag_prices = hoag_prices_rev[['CPT_1', 'carrum_price']]
hoag_prices = hoag_prices.drop_duplicates(keep='first')

out_cpt1 = pd.merge(data, hoag_prices, how= 'left', left_on=['cpt_1'], right_on='CPT_1', suffixes=["_client", "_hoag"])
out_cpt1.rename(columns = {'carrum_price':'carrum_price_1'}, inplace=True)
out_cpt1.to_csv('non_claims_presales/output/Tripoint/out_cpt1.csv')

out_cpt2 = pd.merge(data, hoag_prices, how= 'left', left_on='cpt_2', right_on='CPT_1', suffixes=["_client", "_hoag"])
out_cpt2.rename(columns = {'carrum_price':'carrum_price_2'}, inplace=True)
out_cpt2 = out_cpt2[['proc_id','carrum_price_2']]
out12 = pd.merge(out_cpt1, out_cpt2, on='proc_id', how='outer')
#out12.to_csv('/Users/lauren/pre_sales/32bj/output/check.csv')

out_cpt3 = pd.merge(out12, hoag_prices, how= 'left', left_on='cpt_3', right_on='CPT_1', suffixes=["_client", "_hoag"])
out_cpt3.rename(columns = {'carrum_price':'carrum_price_3'}, inplace=True)

#out123 = pd.merge(out, out_cpt2, on='proc_id', how='outer')

out_cpt4 = pd.merge(out_cpt3, hoag_prices, how= 'left', left_on='cpt_4', right_on='CPT_1', suffixes=["_client", "_hoag"])
out_cpt4.rename(columns = {'carrum_price':'carrum_price_4'}, inplace=True)

out_cpt5 = pd.merge(out_cpt4, hoag_prices, how= 'left', left_on='cpt_5', right_on='CPT_1', suffixes=["_client", "_hoag"])
out_cpt5.rename(columns = {'carrum_price':'carrum_price_5'}, inplace=True)

out_cpt5.to_csv('non_claims_presales/output/Tripoint/check.csv')

out_cpt5 = out_cpt5[['proc_id', 'Focal_CPT _codes', 'cpt_1','cpt_2', 'cpt_3', 'cpt_4', 'cpt_5', 'cpt_desc_list', 'Procedure Category', 'Episode Count', 'Estimated Episode Count', 'Total Episode Cost (mean)', 'Total Episode Cost (median)', 'carrum_price_1', 'carrum_price_2', 'carrum_price_3', 'carrum_price_4', 'carrum_price_5']]

out_cpt5['highest_cost'] = out_cpt5[['carrum_price_1', 'carrum_price_2', 'carrum_price_3', 'carrum_price_4', 'carrum_price_5']].max(axis=1)

costs = pd.DataFrame(np.sort(out_cpt5[['proc_id','carrum_price_1', 'carrum_price_2', 'carrum_price_3', 'carrum_price_4', 'carrum_price_5']].values)[:,-6:], columns=['id', '5th-largest','4th-largest','3nd-largest', '2nd-largest','largest'])

costs['id'] = costs['id'].astype(int)

out_final_costs = pd.merge(out_cpt5, costs, left_on='proc_id', right_on='id')
out_final_costs.to_csv('non_claims_presales/output/Tripoint/outpatient_costs.csv')
