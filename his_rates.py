import pandas as pd
import numpy as np

import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.options.mode.chained_assignment = None  # default='warn'

#run this after create demographic data and before costs to create incidence rates for each procedure
#then use those numbers to run tables

his_data = pd.read_csv('/Users/lauren/pre_sales/non_claims_presales/input/his_incidence_data.csv')
#amgen = pd.read_csv('/Users/lauren/non_claims_presales/output/employee_demographics.csv')
prospect = raw_input("Please enter the prospective client name: ")
prospect = str(prospect)

client_census = raw_input("Please enter path to client census data: ")
client_census = str(client_census)
census = pd.read_csv(client_census)
client_pop_size_total = len(census)
####FOR AA####
#client_pop_size_total = len(census) * 2.1
####
print "Client total population size: ", client_pop_size_total
print '\n'

client = pd.read_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/employee_demographics.csv')
adult_lives = client['Estimated Adult Lives'].sum()
print "Adult Population size: ", adult_lives
#think about whether to use the number of people 18 or over OR all people in the census (lower pop = higher incidences)
print '\n'

emp_census = census.loc[census['Relationship Code'] =='Employee'].copy()
employee_pop_size = len(emp_census)

####for AA####
#employee_pop_size = len(census)
####

print "Total employee population size: ", employee_pop_size
print '\n'
#scale_factor = 0.0005154417765559898*employee_pop_size #(the smaller the population, the larger the multiplier)
#scale_factor = 0.0003154417765559898*employee_pop_size # ulta (14570 adult pop, 4.6)
#scale_factor = 0.000284*employee_pop_size # alliant (18986 adult pop, 5.4)
#scale_factor = 0.0010356177709998308*employee_pop_size # alliant (5783 adult pop, 5.9)

scale_factor = 0.003154417765559898*employee_pop_size# 3677 (zayo, 11.5)

#scale_factor = 0.005154417765559898*employee_pop_size #abt (2174 total pop, 11.2)
####for AA####
#scale_factor = 0.0001154417765559898*employee_pop_size #AA (adult pop 90500, 10.5)

print 'Scale Factor: ', scale_factor

his_data['state_cat'] = his_data['state_abbrev'].astype(str) + '_' + his_data['patient_discharge_categories'].astype(str)

#df = his_data.loc[his_data.state_abbrev == 'ca']
def create_procedure_rates(df):
    df['total_number_discharges_private_adj'] = (df['percent_discharges_private']/100) * df['total_number_discharges']

    #working_state_pop = df.loc[(df.patient_discharge_categories == '18-44') | (df.patient_discharge_categories == '45-64'), 'state_pop_numbers'].sum()
    #df['discharge_percent_pop'] = (df['total_number_discharges']/working_state_pop) * 100

    total_num_discharges = df.loc[(df.patient_discharge_categories == 'Male') | (df.patient_discharge_categories == 'Female'), 'total_number_discharges'].sum()
    procs = list(df.columns[10:-2])

    for index, row in df.iterrows():
        df['his_rates_antpostfusion_453-455'] = (df['discharges_antpostfusion_453-455']/total_num_discharges) *100
        df['his_rates_backneck_518-520'] = (df['discharges_backneck_518-520']/total_num_discharges) *100
        df['his_rates_bariatric_619-621'] = (df['discharges_bariatric_619-621']/total_num_discharges) *100
        df['his_rates_bilateral_major_lower_extremity_461-462'] = (df['discharges_bilateral_major_lower_extremity_461-462']/total_num_discharges) *100
        df['his_rates_hand_wrist_513-514'] = (df['discharges_hand_wrist_513-514']/total_num_discharges) *100
        df['his_rates_hip_femur_not_joint_480-482'] = (df['discharges_hip_femur_not_joint_480-482']/total_num_discharges) *100
        df['his_rates_hip_knee_replace_469-470'] = (df['discharges_hip_knee_replace_469-470']/total_num_discharges) *100
        df['his_rates_hip_knee_revise_466-468'] = (df['discharges_hip_knee_revise_466-468']/total_num_discharges) *100
        df['his_rates_upper_joint_limb_reattach_483-484'] = (df['discharges_upper_joint_limb_reattach_483-484']/total_num_discharges) *100
        df['his_rates_knee_other_485-489'] = (df['discharges_knee_other_485-489']/total_num_discharges) *100
        df['his_rates_lower_extremity_humer_492-494'] = (df['discharges_lower_extremity_humer_492-494']/total_num_discharges) *100
        df['his_rates_other_musc_515-517'] = (df['discharges_other_musc_515-517']/total_num_discharges) *100
        df['his_rates_shoulder_elbow_forearm_510-512'] = (df['discharges_shoulder_elbow_forearm_510-512']/total_num_discharges) *100
        df['his_rates_major_joint_shoulder_elbow_507-508'] = (df['discharges_major_joint_shoulder_elbow_507-508']/total_num_discharges) *100
        df['his_rates_spinal_fusion_curve_malig_infect_456-458'] = (df['discharges_spinal_fusion_curve_malig_infect_456-458']/total_num_discharges) *100
        df['his_rates_spinal_fusion_except_cervical_459-460'] = (df['discharges_spinal_fusion_except_cervical_459-460']/total_num_discharges) *100
        df['his_rates_spinal_neuro_28-30'] = (df['discharges_spinal_neuro_28-30']/total_num_discharges) *100
        df['his_rates_coronary_bypass_234-236'] = (df['discharges_coronary_bypass_234-236']/total_num_discharges) *100
        df['his_rates_cervical_spinal_fusion_471-473'] = (df['discharges_cervical_spinal_fusion_471-473']/total_num_discharges) *100

    for index, row in df.iterrows():
        df['pop_adj_rates_antpostfusion_453-455'] = df['his_rates_antpostfusion_453-455'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*(scale_factor-1)))
        df['pop_adj_rates_backneck_518-520'] = df['his_rates_backneck_518-520'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*(scale_factor-1)))
        df['pop_adj_rates_bariatric_619-621'] = df['his_rates_bariatric_619-621'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_bilateral_major_lower_extremity_461-462'] = df['his_rates_bilateral_major_lower_extremity_461-462'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_hand_wrist_513-514'] = df['his_rates_hand_wrist_513-514'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_hip_femur_not_joint_480-482'] = df['his_rates_hip_femur_not_joint_480-482'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_hip_knee_replace_469-470'] = df['his_rates_hip_knee_replace_469-470'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*(scale_factor*3)))
        df['pop_adj_rates_hip_knee_revise_466-468'] = df['his_rates_hip_knee_revise_466-468'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_upper_joint_limb_reattach_483-484'] = df['his_rates_upper_joint_limb_reattach_483-484'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_knee_other_485-489'] = df['his_rates_knee_other_485-489'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_lower_extremity_humer_492-494'] = df['his_rates_lower_extremity_humer_492-494'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_other_musc_515-517'] = df['his_rates_other_musc_515-517'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_shoulder_elbow_forearm_510-512'] = df['his_rates_shoulder_elbow_forearm_510-512'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_major_joint_shoulder_elbow_507-508'] = df['his_rates_major_joint_shoulder_elbow_507-508'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_spinal_fusion_curve_malig_infect_456-458'] = df['his_rates_spinal_fusion_curve_malig_infect_456-458'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_spinal_fusion_except_cervical_459-460'] = df['his_rates_spinal_fusion_except_cervical_459-460'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_spinal_neuro_28-30'] = df['his_rates_spinal_neuro_28-30'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        df['pop_adj_rates_coronary_bypass_234-236'] = df['his_rates_coronary_bypass_234-236'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*(scale_factor-1)))
        df['pop_adj_rates_cervical_spinal_fusion_471-473'] = df['his_rates_cervical_spinal_fusion_471-473'] / (df['percent_discharges'] + (df['percent_discharges_priv_of_ins_pop']*scale_factor))
        #12 scaling factor for Amgen (0.00052*23281.00)
        #Tripoint 0.00052*3379

    gender_age = ['male_less_45', 'female_less_45', 'male_plus_45', 'female_plus_45']

    for p in procs:
        for g in gender_age:
            if g == 'male_less_45':
                df[g + p[10:]] = df.loc[(df.patient_discharge_categories == '18-44') | (df.patient_discharge_categories == 'Male'), 'pop_adj_rates'+ p[10:]].mean()
            if g == 'female_less_45':
                df[g + p[10:]] = df.loc[(df.patient_discharge_categories == '18-44') | (df.patient_discharge_categories == 'Female'), 'pop_adj_rates'+ p[10:]].mean()
            if g == 'male_plus_45':
                df[g + p[10:]] = df.loc[(df.patient_discharge_categories == '45-64') | (df.patient_discharge_categories == 'Male'), 'pop_adj_rates'+ p[10:]].mean()
            if g == 'female_plus_45':
                df[g + p[10:]] = df.loc[(df.patient_discharge_categories == '45-64') | (df.patient_discharge_categories == 'Female'), 'pop_adj_rates'+ p[10:]].mean()
    return df

his_grouped = his_data.groupby(['state'], as_index=False)
dfs = []
for name, group in his_grouped:
    create_procedure_rates(group)
    dfs.append(group)
d = pd.concat(dfs)

his_state = d.groupby(['state'], as_index=False).first()
his_state_rates = his_state[['state',
     'state_abbrev','male_less_45_antpostfusion_453-455',
     'female_less_45_antpostfusion_453-455',
     'male_plus_45_antpostfusion_453-455',
     'female_plus_45_antpostfusion_453-455',
     'male_less_45_backneck_518-520',
     'female_less_45_backneck_518-520',
     'male_plus_45_backneck_518-520',
     'female_plus_45_backneck_518-520',
     'male_less_45_bariatric_619-621',
     'female_less_45_bariatric_619-621',
     'male_plus_45_bariatric_619-621',
     'female_plus_45_bariatric_619-621',
     'male_less_45_bilateral_major_lower_extremity_461-462',
     'female_less_45_bilateral_major_lower_extremity_461-462',
     'male_plus_45_bilateral_major_lower_extremity_461-462',
     'female_plus_45_bilateral_major_lower_extremity_461-462',
     'male_less_45_hand_wrist_513-514',
     'female_less_45_hand_wrist_513-514',
     'male_plus_45_hand_wrist_513-514',
     'female_plus_45_hand_wrist_513-514',
     'male_less_45_hip_femur_not_joint_480-482',
     'female_less_45_hip_femur_not_joint_480-482',
     'male_plus_45_hip_femur_not_joint_480-482',
     'female_plus_45_hip_femur_not_joint_480-482',
     'male_less_45_hip_knee_replace_469-470',
     'female_less_45_hip_knee_replace_469-470',
     'male_plus_45_hip_knee_replace_469-470',
     'female_plus_45_hip_knee_replace_469-470',
     'male_less_45_hip_knee_revise_466-468',
     'female_less_45_hip_knee_revise_466-468',
     'male_plus_45_hip_knee_revise_466-468',
     'female_plus_45_hip_knee_revise_466-468',
     'male_less_45_upper_joint_limb_reattach_483-484',
     'female_less_45_upper_joint_limb_reattach_483-484',
     'male_plus_45_upper_joint_limb_reattach_483-484',
     'female_plus_45_upper_joint_limb_reattach_483-484',
     'male_less_45_knee_other_485-489',
     'female_less_45_knee_other_485-489',
     'male_plus_45_knee_other_485-489',
     'female_plus_45_knee_other_485-489',
     'male_less_45_lower_extremity_humer_492-494',
     'female_less_45_lower_extremity_humer_492-494',
     'male_plus_45_lower_extremity_humer_492-494',
     'female_plus_45_lower_extremity_humer_492-494',
     'male_less_45_other_musc_515-517',
     'female_less_45_other_musc_515-517',
     'male_plus_45_other_musc_515-517',
     'female_plus_45_other_musc_515-517',
     'male_less_45_shoulder_elbow_forearm_510-512',
     'female_less_45_shoulder_elbow_forearm_510-512',
     'male_plus_45_shoulder_elbow_forearm_510-512',
     'female_plus_45_shoulder_elbow_forearm_510-512',
     'male_less_45_major_joint_shoulder_elbow_507-508',
     'female_less_45_major_joint_shoulder_elbow_507-508',
     'male_plus_45_major_joint_shoulder_elbow_507-508',
     'female_plus_45_major_joint_shoulder_elbow_507-508',
     'male_less_45_spinal_fusion_curve_malig_infect_456-458',
     'female_less_45_spinal_fusion_curve_malig_infect_456-458',
     'male_plus_45_spinal_fusion_curve_malig_infect_456-458',
     'female_plus_45_spinal_fusion_curve_malig_infect_456-458',
     'male_less_45_spinal_fusion_except_cervical_459-460',
     'female_less_45_spinal_fusion_except_cervical_459-460',
     'male_plus_45_spinal_fusion_except_cervical_459-460',
     'female_plus_45_spinal_fusion_except_cervical_459-460',
     'male_less_45_spinal_neuro_28-30',
     'female_less_45_spinal_neuro_28-30',
     'male_plus_45_spinal_neuro_28-30',
     'female_plus_45_spinal_neuro_28-30',
     'male_less_45_coronary_bypass_234-236',
     'female_less_45_coronary_bypass_234-236',
     'male_plus_45_coronary_bypass_234-236',
     'female_plus_45_coronary_bypass_234-236',
     'male_less_45_cervical_spinal_fusion_471-473',
     'female_less_45_cervical_spinal_fusion_471-473',
     'male_plus_45_cervical_spinal_fusion_471-473',
     'female_plus_45_cervical_spinal_fusion_471-473']]


client_rates = pd.merge(his_state_rates, client, how='outer', left_on=['state_abbrev'], right_on=['State'])

#drop hawaii
client_rates_not_hi = client_rates.loc[~(client_rates['state_abbrev'] == 'HI')]

client_rates_filled = client_rates_not_hi.fillna(client_rates_not_hi.mean())
#FILL IN Missing with average
proc_list = ['male_less_45_antpostfusion_453-455',
    'female_less_45_antpostfusion_453-455',
    'male_plus_45_antpostfusion_453-455',
    'female_plus_45_antpostfusion_453-455',
    'male_less_45_backneck_518-520',
    'female_less_45_backneck_518-520',
    'male_plus_45_backneck_518-520',
    'female_plus_45_backneck_518-520',
    'male_less_45_bariatric_619-621',
    'female_less_45_bariatric_619-621',
    'male_plus_45_bariatric_619-621',
    'female_plus_45_bariatric_619-621',
    'male_less_45_bilateral_major_lower_extremity_461-462',
    'female_less_45_bilateral_major_lower_extremity_461-462',
    'male_plus_45_bilateral_major_lower_extremity_461-462',
    'female_plus_45_bilateral_major_lower_extremity_461-462',
    'male_less_45_hand_wrist_513-514',
    'female_less_45_hand_wrist_513-514',
    'male_plus_45_hand_wrist_513-514',
    'female_plus_45_hand_wrist_513-514',
    'male_less_45_hip_femur_not_joint_480-482',
    'female_less_45_hip_femur_not_joint_480-482',
    'male_plus_45_hip_femur_not_joint_480-482',
    'female_plus_45_hip_femur_not_joint_480-482',
    'male_less_45_hip_knee_replace_469-470',
    'female_less_45_hip_knee_replace_469-470',
    'male_plus_45_hip_knee_replace_469-470',
    'female_plus_45_hip_knee_replace_469-470',
    'male_less_45_hip_knee_revise_466-468',
    'female_less_45_hip_knee_revise_466-468',
    'male_plus_45_hip_knee_revise_466-468',
    'female_plus_45_hip_knee_revise_466-468',
    'male_less_45_upper_joint_limb_reattach_483-484',
    'female_less_45_upper_joint_limb_reattach_483-484',
    'male_plus_45_upper_joint_limb_reattach_483-484',
    'female_plus_45_upper_joint_limb_reattach_483-484',
    'male_less_45_knee_other_485-489',
    'female_less_45_knee_other_485-489',
    'male_plus_45_knee_other_485-489',
    'female_plus_45_knee_other_485-489',
    'male_less_45_lower_extremity_humer_492-494',
    'female_less_45_lower_extremity_humer_492-494',
    'male_plus_45_lower_extremity_humer_492-494',
    'female_plus_45_lower_extremity_humer_492-494',
    'male_less_45_other_musc_515-517',
    'female_less_45_other_musc_515-517',
    'male_plus_45_other_musc_515-517',
    'female_plus_45_other_musc_515-517',
    'male_less_45_shoulder_elbow_forearm_510-512',
    'female_less_45_shoulder_elbow_forearm_510-512',
    'male_plus_45_shoulder_elbow_forearm_510-512',
    'female_plus_45_shoulder_elbow_forearm_510-512',
    'male_less_45_major_joint_shoulder_elbow_507-508',
    'female_less_45_major_joint_shoulder_elbow_507-508',
    'male_plus_45_major_joint_shoulder_elbow_507-508',
    'female_plus_45_major_joint_shoulder_elbow_507-508',
    'male_less_45_spinal_fusion_curve_malig_infect_456-458',
    'female_less_45_spinal_fusion_curve_malig_infect_456-458',
    'male_plus_45_spinal_fusion_curve_malig_infect_456-458',
    'female_plus_45_spinal_fusion_curve_malig_infect_456-458',
    'male_less_45_spinal_fusion_except_cervical_459-460',
    'female_less_45_spinal_fusion_except_cervical_459-460',
    'male_plus_45_spinal_fusion_except_cervical_459-460',
    'female_plus_45_spinal_fusion_except_cervical_459-460',
    'male_less_45_spinal_neuro_28-30',
    'female_less_45_spinal_neuro_28-30',
    'male_plus_45_spinal_neuro_28-30',
    'female_plus_45_spinal_neuro_28-30',
    'male_less_45_coronary_bypass_234-236',
    'female_less_45_coronary_bypass_234-236',
    'male_plus_45_coronary_bypass_234-236',
    'female_plus_45_coronary_bypass_234-236',
    'male_less_45_cervical_spinal_fusion_471-473',
    'female_less_45_cervical_spinal_fusion_471-473',
    'male_plus_45_cervical_spinal_fusion_471-473',
    'female_plus_45_cervical_spinal_fusion_471-473']

for p_ in proc_list:
    if 'female_plus_45' in p_:
        client_rates_filled[p_ + '_estimate'] = client_rates_filled[p_] * client_rates_filled['total_female_plus_45']
    if 'male_plus_45' in p_:
        client_rates_filled[p_ + '_estimate'] = client_rates_filled[p_] * client_rates_filled['total_male_plus_45']
    if 'female_less_45' in p_:
        client_rates_filled[p_ + '_estimate'] = client_rates_filled[p_] * client_rates_filled['total_female_less_45']
    if 'male_less_45' in p_:
        client_rates_filled[p_ + '_estimate'] = client_rates_filled[p_] * client_rates_filled['total_male_less_45']


incidence_table = client_rates_filled[['State','Estimated Adult Lives','male_less_45_antpostfusion_453-455_estimate',
     'female_less_45_antpostfusion_453-455_estimate',
     'male_plus_45_antpostfusion_453-455_estimate',
     'female_plus_45_antpostfusion_453-455_estimate',
     'male_less_45_backneck_518-520_estimate',
     'female_less_45_backneck_518-520_estimate',
     'male_plus_45_backneck_518-520_estimate',
     'female_plus_45_backneck_518-520_estimate',
     'male_less_45_bariatric_619-621_estimate',
     'female_less_45_bariatric_619-621_estimate',
     'male_plus_45_bariatric_619-621_estimate',
     'female_plus_45_bariatric_619-621_estimate',
     'male_less_45_bilateral_major_lower_extremity_461-462_estimate',
     'female_less_45_bilateral_major_lower_extremity_461-462_estimate',
     'male_plus_45_bilateral_major_lower_extremity_461-462_estimate',
     'female_plus_45_bilateral_major_lower_extremity_461-462_estimate',
     'male_less_45_hand_wrist_513-514_estimate',
     'female_less_45_hand_wrist_513-514_estimate',
     'male_plus_45_hand_wrist_513-514_estimate',
     'female_plus_45_hand_wrist_513-514_estimate',
     'male_less_45_hip_femur_not_joint_480-482_estimate',
     'female_less_45_hip_femur_not_joint_480-482_estimate',
     'male_plus_45_hip_femur_not_joint_480-482_estimate',
     'female_plus_45_hip_femur_not_joint_480-482_estimate',
     'male_less_45_hip_knee_replace_469-470_estimate',
     'female_less_45_hip_knee_replace_469-470_estimate',
     'male_plus_45_hip_knee_replace_469-470_estimate',
     'female_plus_45_hip_knee_replace_469-470_estimate',
     'male_less_45_hip_knee_revise_466-468_estimate',
     'female_less_45_hip_knee_revise_466-468_estimate',
     'male_plus_45_hip_knee_revise_466-468_estimate',
     'female_plus_45_hip_knee_revise_466-468_estimate',
     'male_less_45_upper_joint_limb_reattach_483-484_estimate',
     'female_less_45_upper_joint_limb_reattach_483-484_estimate',
     'male_plus_45_upper_joint_limb_reattach_483-484_estimate',
     'female_plus_45_upper_joint_limb_reattach_483-484_estimate',
     'male_less_45_knee_other_485-489_estimate',
     'female_less_45_knee_other_485-489_estimate',
     'male_plus_45_knee_other_485-489_estimate',
     'female_plus_45_knee_other_485-489_estimate',
     'male_less_45_lower_extremity_humer_492-494_estimate',
     'female_less_45_lower_extremity_humer_492-494_estimate',
     'male_plus_45_lower_extremity_humer_492-494_estimate',
     'female_plus_45_lower_extremity_humer_492-494_estimate',
     'male_less_45_other_musc_515-517_estimate',
     'female_less_45_other_musc_515-517_estimate',
     'male_plus_45_other_musc_515-517_estimate',
     'female_plus_45_other_musc_515-517_estimate',
     'male_less_45_shoulder_elbow_forearm_510-512_estimate',
     'female_less_45_shoulder_elbow_forearm_510-512_estimate',
     'male_plus_45_shoulder_elbow_forearm_510-512_estimate',
     'female_plus_45_shoulder_elbow_forearm_510-512_estimate',
     'male_less_45_major_joint_shoulder_elbow_507-508_estimate',
     'female_less_45_major_joint_shoulder_elbow_507-508_estimate',
     'male_plus_45_major_joint_shoulder_elbow_507-508_estimate',
     'female_plus_45_major_joint_shoulder_elbow_507-508_estimate',
     'male_less_45_spinal_fusion_curve_malig_infect_456-458_estimate',
     'female_less_45_spinal_fusion_curve_malig_infect_456-458_estimate',
     'male_plus_45_spinal_fusion_curve_malig_infect_456-458_estimate',
     'female_plus_45_spinal_fusion_curve_malig_infect_456-458_estimate',
     'male_less_45_spinal_fusion_except_cervical_459-460_estimate',
     'female_less_45_spinal_fusion_except_cervical_459-460_estimate',
     'male_plus_45_spinal_fusion_except_cervical_459-460_estimate',
     'female_plus_45_spinal_fusion_except_cervical_459-460_estimate',
     'male_less_45_spinal_neuro_28-30_estimate',
     'female_less_45_spinal_neuro_28-30_estimate',
     'male_plus_45_spinal_neuro_28-30_estimate',
     'female_plus_45_spinal_neuro_28-30_estimate',
     'male_less_45_coronary_bypass_234-236_estimate',
     'female_less_45_coronary_bypass_234-236_estimate',
     'male_plus_45_coronary_bypass_234-236_estimate',
     'female_plus_45_coronary_bypass_234-236_estimate',
     'male_less_45_cervical_spinal_fusion_471-473_estimate',
     'female_less_45_cervical_spinal_fusion_471-473_estimate',
     'male_plus_45_cervical_spinal_fusion_471-473_estimate',
     'female_plus_45_cervical_spinal_fusion_471-473_estimate']]

incidence_table = np.round(incidence_table, decimals=1)

incidence_table = incidence_table.astype({c: int for c in incidence_table.iloc[:,1:]})

incidence_table.to_csv('/Users/lauren/pre_sales/non_claims_presales/output/' + prospect + '/his_estimates.csv')
