import pandas as pd
import numpy as np

cost_data = pd.read_csv('non_claims_presales/input/his_costs.csv')
prof_rate = pd.read_csv('non_claims_presales/input/medicare_prof_rate.csv')
incidence_table = pd.read_csv('non_claims_presales/output/his_estimates.csv')

def build_cost_variables(df):

    df['idx'] = df.index
    df.set_index('idx', inplace=True)
    df_t = df.T
    df_t['cols'] = df_t.index

    df_t_prof = pd.merge(df_t, prof_rate, how='outer', left_on=['cols'], right_on=['drg_column'])
    df_t_prof['18-44_prof'] = df_t_prof[df_t_prof.columns[0]] + (df_t_prof[df_t_prof.columns[0]] * df_t_prof.prof_rate)
    df_t_prof['45-64_prof'] = df_t_prof[df_t_prof.columns[1]] + (df_t_prof[df_t_prof.columns[1]] * df_t_prof.prof_rate)
    df_t_prof['Male_prof'] = df_t_prof[df_t_prof.columns[2]] + (df_t_prof[df_t_prof.columns[2]] * df_t_prof.prof_rate)
    df_t_prof['Female_prof'] = df_t_prof[df_t_prof.columns[3]] + (df_t_prof[df_t_prof.columns[3]] * df_t_prof.prof_rate)

    df_t_prof['18-44_prof_cpim'] = df_t_prof['18-44_prof'] + (df_t_prof['18-44_prof'] * 0.146)
    df_t_prof['45-64_prof_cpim'] = df_t_prof['45-64_prof'] + ( df_t_prof['45-64_prof']* 0.146)
    df_t_prof['Male_prof_cpim'] = df_t_prof['Male_prof'] + (df_t_prof['Male_prof']* 0.146)
    df_t_prof['Female_prof_cpim'] = df_t_prof['Female_prof'] + (df_t_prof['Female_prof']* 0.146)

    df_t_prof['18-44_prof_adj'] = df_t_prof['18-44_prof_cpim'] + (df_t_prof['18-44_prof_cpim'] * .003) * 100
    df_t_prof['45-64_prof_adj'] = df_t_prof['45-64_prof_cpim'] + ( df_t_prof['45-64_prof_cpim']* .003)  * 100
    df_t_prof['Male_prof_adj'] = df_t_prof['Male_prof_cpim'] + (df_t_prof['Male_prof_cpim']* .003)  * 100
    df_t_prof['Female_prof_adj'] = df_t_prof['Female_prof_cpim'] + (df_t_prof['Female_prof_cpim']* .003)  * 100

    df_t_prof['male_less_45'] = (df_t_prof['18-44_prof_adj'] + df_t_prof['Male_prof_adj'])/2
    df_t_prof['female_less_45'] = (df_t_prof['18-44_prof_adj'] + df_t_prof['Female_prof_adj'])/2
    df_t_prof['male_plus_45'] = (df_t_prof['45-64_prof_adj'] + df_t_prof['Male_prof_adj'])/2
    df_t_prof['female_plus_45'] = (df_t_prof['45-64_prof_adj'] + df_t_prof['Female_prof_adj'])/2

    df_t_prof = df_t_prof.fillna(df_t_prof.mean())

    df_t_prof['abbrev'] = df_t_prof[df_t_prof.columns[0]][1]

    df_t_prof = df_t_prof[['abbrev', 'drg_column','male_less_45', 'female_less_45', 'male_plus_45', 'female_plus_45']]
    df_costs = df_t_prof.loc[df_t_prof['drg_column'].notnull()]
    #df_costs = df_costs.T

    return df_costs

states = list(cost_data.state_abbrev.unique())
dfs = []
for state in states:
    df = cost_data.loc[cost_data.state_abbrev == state]
    df_state_cost = build_cost_variables(df)
    df_state_cost_wide = df_state_cost.pivot('abbrev', 'drg_column')
    dfs.append(df_state_cost_wide)
d = pd.concat(dfs)

d_filled = d.fillna(d.mean())
d_filled.to_csv('/Users/lauren/non_claims_presales/output/his_cost_estimates.csv')

d_filled.columns = ['_'.join(col).strip() for col in d_filled.columns.values]
d_filled['state_abbrev'] = d_filled.index
#need to merge with incidence_table
merged_costs = pd.merge(incidence_table, d_filled, how='left', left_on='State', right_on='state_abbrev')
merged_costs_filled = merged_costs.fillna(merged_costs.mean())

merged_costs_filled.set_index('State', inplace=True)

antpostfusion = merged_costs_filled.filter(regex='453-455')
antpostfusion['male_less_45_antpostfusion_453-455_cost'] = antpostfusion['male_less_45_antpostfusion_453-455_estimate'] * antpostfusion['male_less_45_antpostfusion_453-455']
antpostfusion['female_less_45_antpostfusion_453-455_cost'] = antpostfusion['female_less_45_antpostfusion_453-455_estimate'] * antpostfusion['female_less_45_antpostfusion_453-455']
antpostfusion['male_plus_45_antpostfusion_453-455_cost'] = antpostfusion['male_plus_45_antpostfusion_453-455_estimate'] * antpostfusion['male_plus_45_antpostfusion_453-455']
antpostfusion['female_plus_45_antpostfusion_453-455_cost'] = antpostfusion['female_less_45_antpostfusion_453-455_estimate'] * antpostfusion['female_plus_45_antpostfusion_453-455']
antpostfusion = antpostfusion[['male_less_45_antpostfusion_453-455_cost', 'female_less_45_antpostfusion_453-455_cost', 'male_plus_45_antpostfusion_453-455_cost', 'female_plus_45_antpostfusion_453-455_cost']]

backneck = merged_costs_filled.filter(regex='518-520')
backneck['male_less_45_backneck_518-520_cost'] = backneck['male_less_45_backneck_518-520_estimate'] * backneck['male_less_45_backneck_518-520']
backneck['female_less_45_backneck_518-520_cost'] = backneck['female_less_45_backneck_518-520_estimate'] * backneck['female_less_45_backneck_518-520']
backneck['male_plus_45_backneck_518-520_cost'] = backneck['male_plus_45_backneck_518-520_estimate'] * backneck['male_plus_45_backneck_518-520']
backneck['female_plus_45_backneck_518-520_cost'] = backneck['female_less_45_backneck_518-520_estimate'] * backneck['female_plus_45_backneck_518-520']
backneck = backneck[['male_less_45_backneck_518-520_cost', 'female_less_45_backneck_518-520_cost', 'male_plus_45_backneck_518-520_cost', 'female_plus_45_backneck_518-520_cost']]

bariatric = merged_costs_filled.filter(regex='619-621')
bariatric['male_less_45_bariatric_619-621_cost'] = bariatric['male_less_45_bariatric_619-621_estimate'] * bariatric['male_less_45_bariatric_619-621']
bariatric['female_less_45_bariatric_619-621_cost'] = bariatric['female_less_45_bariatric_619-621_estimate'] * bariatric['female_less_45_bariatric_619-621']
bariatric['male_plus_45_bariatric_619-621_cost'] = bariatric['male_plus_45_bariatric_619-621_estimate'] * bariatric['male_plus_45_bariatric_619-621']
bariatric['female_plus_45_bariatric_619-621_cost'] = bariatric['female_less_45_bariatric_619-621_estimate'] * bariatric['female_plus_45_bariatric_619-621']
bariatric = bariatric[['male_less_45_bariatric_619-621_cost', 'female_less_45_bariatric_619-621_cost', 'male_plus_45_bariatric_619-621_cost', 'female_plus_45_bariatric_619-621_cost']]

bilateral_major_lower_extremity = merged_costs_filled.filter(regex='461-462')
bilateral_major_lower_extremity['male_less_45_bilateral_major_lower_extremity_461-462_cost'] = bilateral_major_lower_extremity['male_less_45_bilateral_major_lower_extremity_461-462_estimate'] * bilateral_major_lower_extremity['male_less_45_bilateral_major_lower_extremity_461-462']
bilateral_major_lower_extremity['female_less_45_bilateral_major_lower_extremity_461-462_cost'] = bilateral_major_lower_extremity['female_less_45_bilateral_major_lower_extremity_461-462_estimate'] * bilateral_major_lower_extremity['female_less_45_bilateral_major_lower_extremity_461-462']
bilateral_major_lower_extremity['male_plus_45_bilateral_major_lower_extremity_461-462_cost'] = bilateral_major_lower_extremity['male_plus_45_bilateral_major_lower_extremity_461-462_estimate'] * bilateral_major_lower_extremity['male_plus_45_bilateral_major_lower_extremity_461-462']
bilateral_major_lower_extremity['female_plus_45_bilateral_major_lower_extremity_461-462_cost'] = bilateral_major_lower_extremity['female_less_45_bilateral_major_lower_extremity_461-462_estimate'] * bilateral_major_lower_extremity['female_plus_45_bilateral_major_lower_extremity_461-462']
bilateral_major_lower_extremity = bilateral_major_lower_extremity[['male_less_45_bilateral_major_lower_extremity_461-462_cost', 'female_less_45_bilateral_major_lower_extremity_461-462_cost', 'male_plus_45_bilateral_major_lower_extremity_461-462_cost', 'female_plus_45_bilateral_major_lower_extremity_461-462_cost']]

hand_wrist = merged_costs_filled.filter(regex='513-514')
hand_wrist['male_less_45_hand_wrist_513-514_cost'] = hand_wrist['male_less_45_hand_wrist_513-514_estimate'] * hand_wrist['male_less_45_hand_wrist_513-514']
hand_wrist['female_less_45_hand_wrist_513-514_cost'] = hand_wrist['female_less_45_hand_wrist_513-514_estimate'] * hand_wrist['female_less_45_hand_wrist_513-514']
hand_wrist['male_plus_45_hand_wrist_513-514_cost'] = hand_wrist['male_plus_45_hand_wrist_513-514_estimate'] * hand_wrist['male_plus_45_hand_wrist_513-514']
hand_wrist['female_plus_45_hand_wrist_513-514_cost'] = hand_wrist['female_less_45_hand_wrist_513-514_estimate'] * hand_wrist['female_plus_45_hand_wrist_513-514']
hand_wrist = hand_wrist[['male_less_45_hand_wrist_513-514_cost', 'female_less_45_hand_wrist_513-514_cost', 'male_plus_45_hand_wrist_513-514_cost', 'female_plus_45_hand_wrist_513-514_cost']]

hip_femur_not_joint = merged_costs_filled.filter(regex='480-482')
hip_femur_not_joint['male_less_45_hip_femur_not_joint_480-482_cost'] = hip_femur_not_joint['male_less_45_hip_femur_not_joint_480-482_estimate'] * hip_femur_not_joint['male_less_45_hip_femur_not_joint_480-482']
hip_femur_not_joint['female_less_45_hip_femur_not_joint_480-482_cost'] = hip_femur_not_joint['female_less_45_hip_femur_not_joint_480-482_estimate'] * hip_femur_not_joint['female_less_45_hip_femur_not_joint_480-482']
hip_femur_not_joint['male_plus_45_hip_femur_not_joint_480-482_cost'] = hip_femur_not_joint['male_plus_45_hip_femur_not_joint_480-482_estimate'] * hip_femur_not_joint['male_plus_45_hip_femur_not_joint_480-482']
hip_femur_not_joint['female_plus_45_hip_femur_not_joint_480-482_cost'] = hip_femur_not_joint['female_less_45_hip_femur_not_joint_480-482_estimate'] * hip_femur_not_joint['female_plus_45_hip_femur_not_joint_480-482']
hip_femur_not_joint = hip_femur_not_joint[['male_less_45_hip_femur_not_joint_480-482_cost', 'female_less_45_hip_femur_not_joint_480-482_cost', 'male_plus_45_hip_femur_not_joint_480-482_cost', 'female_plus_45_hip_femur_not_joint_480-482_cost']]

hip_knee_replace = merged_costs_filled.filter(regex='469-470')
hip_knee_replace['male_less_45_hip_knee_replace_469-470_cost'] = hip_knee_replace['male_less_45_hip_knee_replace_469-470_estimate'] * hip_knee_replace['male_less_45_hip_knee_replace_469-470']
hip_knee_replace['female_less_45_hip_knee_replace_469-470_cost'] = hip_knee_replace['female_less_45_hip_knee_replace_469-470_estimate'] * hip_knee_replace['female_less_45_hip_knee_replace_469-470']
hip_knee_replace['male_plus_45_hip_knee_replace_469-470_cost'] = hip_knee_replace['male_plus_45_hip_knee_replace_469-470_estimate'] * hip_knee_replace['male_plus_45_hip_knee_replace_469-470']
hip_knee_replace['female_plus_45_hip_knee_replace_469-470_cost'] = hip_knee_replace['female_less_45_hip_knee_replace_469-470_estimate'] * hip_knee_replace['female_plus_45_hip_knee_replace_469-470']
hip_knee_replace = hip_knee_replace[['male_less_45_hip_knee_replace_469-470_cost', 'female_less_45_hip_knee_replace_469-470_cost', 'male_plus_45_hip_knee_replace_469-470_cost', 'female_plus_45_hip_knee_replace_469-470_cost']]

hip_knee_revise = merged_costs_filled.filter(regex='466-468')
hip_knee_revise['male_less_45_hip_knee_revise_466-468_cost'] = hip_knee_revise['male_less_45_hip_knee_revise_466-468_estimate'] * hip_knee_revise['male_less_45_hip_knee_revise_466-468']
hip_knee_revise['female_less_45_hip_knee_revise_466-468_cost'] = hip_knee_revise['female_less_45_hip_knee_revise_466-468_estimate'] * hip_knee_revise['female_less_45_hip_knee_revise_466-468']
hip_knee_revise['male_plus_45_hip_knee_revise_466-468_cost'] = hip_knee_revise['male_plus_45_hip_knee_revise_466-468_estimate'] * hip_knee_revise['male_plus_45_hip_knee_revise_466-468']
hip_knee_revise['female_plus_45_hip_knee_revise_466-468_cost'] = hip_knee_revise['female_less_45_hip_knee_revise_466-468_estimate'] * hip_knee_revise['female_plus_45_hip_knee_revise_466-468']
hip_knee_revise = hip_knee_revise[['male_less_45_hip_knee_revise_466-468_cost', 'female_less_45_hip_knee_revise_466-468_cost', 'male_plus_45_hip_knee_revise_466-468_cost', 'female_plus_45_hip_knee_revise_466-468_cost']]

upper_joint_limb_reattach = merged_costs_filled.filter(regex='483-484')
upper_joint_limb_reattach['male_less_45_upper_joint_limb_reattach_483-484_cost'] = upper_joint_limb_reattach['male_less_45_upper_joint_limb_reattach_483-484_estimate'] * upper_joint_limb_reattach['male_less_45_upper_joint_limb_reattach_483-484']
upper_joint_limb_reattach['female_less_45_upper_joint_limb_reattach_483-484_cost'] = upper_joint_limb_reattach['female_less_45_upper_joint_limb_reattach_483-484_estimate'] * upper_joint_limb_reattach['female_less_45_upper_joint_limb_reattach_483-484']
upper_joint_limb_reattach['male_plus_45_upper_joint_limb_reattach_483-484_cost'] = upper_joint_limb_reattach['male_plus_45_upper_joint_limb_reattach_483-484_estimate'] * upper_joint_limb_reattach['male_plus_45_upper_joint_limb_reattach_483-484']
upper_joint_limb_reattach['female_plus_45_upper_joint_limb_reattach_483-484_cost'] = upper_joint_limb_reattach['female_less_45_upper_joint_limb_reattach_483-484_estimate'] * upper_joint_limb_reattach['female_plus_45_upper_joint_limb_reattach_483-484']
upper_joint_limb_reattach = upper_joint_limb_reattach[['male_less_45_upper_joint_limb_reattach_483-484_cost', 'female_less_45_upper_joint_limb_reattach_483-484_cost', 'male_plus_45_upper_joint_limb_reattach_483-484_cost', 'female_plus_45_upper_joint_limb_reattach_483-484_cost']]

knee_other = merged_costs_filled.filter(regex='485-489')
knee_other['male_less_45_knee_other_485-489_cost'] = knee_other['male_less_45_knee_other_485-489_estimate'] * knee_other['male_less_45_knee_other_485-489']
knee_other['female_less_45_knee_other_485-489_cost'] = knee_other['female_less_45_knee_other_485-489_estimate'] * knee_other['female_less_45_knee_other_485-489']
knee_other['male_plus_45_knee_other_485-489_cost'] = knee_other['male_plus_45_knee_other_485-489_estimate'] * knee_other['male_plus_45_knee_other_485-489']
knee_other['female_plus_45_knee_other_485-489_cost'] = knee_other['female_less_45_knee_other_485-489_estimate'] * knee_other['female_plus_45_knee_other_485-489']
knee_other = knee_other[['male_less_45_knee_other_485-489_cost', 'female_less_45_knee_other_485-489_cost', 'male_plus_45_knee_other_485-489_cost', 'female_plus_45_knee_other_485-489_cost']]

lower_extremity_humer = merged_costs_filled.filter(regex='492-494')
lower_extremity_humer['male_less_45_lower_extremity_humer_492-494_cost'] = lower_extremity_humer['male_less_45_lower_extremity_humer_492-494_estimate'] * lower_extremity_humer['male_less_45_lower_extremity_humer_492-494']
lower_extremity_humer['female_less_45_lower_extremity_humer_492-494_cost'] = lower_extremity_humer['female_less_45_lower_extremity_humer_492-494_estimate'] * lower_extremity_humer['female_less_45_lower_extremity_humer_492-494']
lower_extremity_humer['male_plus_45_lower_extremity_humer_492-494_cost'] = lower_extremity_humer['male_plus_45_lower_extremity_humer_492-494_estimate'] * lower_extremity_humer['male_plus_45_lower_extremity_humer_492-494']
lower_extremity_humer['female_plus_45_lower_extremity_humer_492-494_cost'] = lower_extremity_humer['female_less_45_lower_extremity_humer_492-494_estimate'] * lower_extremity_humer['female_plus_45_lower_extremity_humer_492-494']
lower_extremity_humer = lower_extremity_humer[['male_less_45_lower_extremity_humer_492-494_cost', 'female_less_45_lower_extremity_humer_492-494_cost', 'male_plus_45_lower_extremity_humer_492-494_cost', 'female_plus_45_lower_extremity_humer_492-494_cost']]

other_musc = merged_costs_filled.filter(regex='515-517')
other_musc['male_less_45_other_musc_515-517_cost'] = other_musc['male_less_45_other_musc_515-517_estimate'] * other_musc['male_less_45_other_musc_515-517']
other_musc['female_less_45_other_musc_515-517_cost'] = other_musc['female_less_45_other_musc_515-517_estimate'] * other_musc['female_less_45_other_musc_515-517']
other_musc['male_plus_45_other_musc_515-517_cost'] = other_musc['male_plus_45_other_musc_515-517_estimate'] * other_musc['male_plus_45_other_musc_515-517']
other_musc['female_plus_45_other_musc_515-517_cost'] = other_musc['female_less_45_other_musc_515-517_estimate'] * other_musc['female_plus_45_other_musc_515-517']
other_musc = other_musc[['male_less_45_other_musc_515-517_cost', 'female_less_45_other_musc_515-517_cost', 'male_plus_45_other_musc_515-517_cost', 'female_plus_45_other_musc_515-517_cost']]

shoulder_elbow_forearm = merged_costs_filled.filter(regex='510-512')
shoulder_elbow_forearm['male_less_45_shoulder_elbow_forearm_510-512_cost'] = shoulder_elbow_forearm['male_less_45_shoulder_elbow_forearm_510-512_estimate'] * shoulder_elbow_forearm['male_less_45_shoulder_elbow_forearm_510-512']
shoulder_elbow_forearm['female_less_45_shoulder_elbow_forearm_510-512_cost'] = shoulder_elbow_forearm['female_less_45_shoulder_elbow_forearm_510-512_estimate'] * shoulder_elbow_forearm['female_less_45_shoulder_elbow_forearm_510-512']
shoulder_elbow_forearm['male_plus_45_shoulder_elbow_forearm_510-512_cost'] = shoulder_elbow_forearm['male_plus_45_shoulder_elbow_forearm_510-512_estimate'] * shoulder_elbow_forearm['male_plus_45_shoulder_elbow_forearm_510-512']
shoulder_elbow_forearm['female_plus_45_shoulder_elbow_forearm_510-512_cost'] = shoulder_elbow_forearm['female_less_45_shoulder_elbow_forearm_510-512_estimate'] * shoulder_elbow_forearm['female_plus_45_shoulder_elbow_forearm_510-512']
shoulder_elbow_forearm = shoulder_elbow_forearm[['male_less_45_shoulder_elbow_forearm_510-512_cost', 'female_less_45_shoulder_elbow_forearm_510-512_cost', 'male_plus_45_shoulder_elbow_forearm_510-512_cost', 'female_plus_45_shoulder_elbow_forearm_510-512_cost']]

major_joint_shoulder_elbow = merged_costs_filled.filter(regex='507-508')
major_joint_shoulder_elbow['male_less_45_major_joint_shoulder_elbow_507-508_cost'] = major_joint_shoulder_elbow['male_less_45_major_joint_shoulder_elbow_507-508_estimate'] * major_joint_shoulder_elbow['male_less_45_major_joint_shoulder_elbow_507-508']
major_joint_shoulder_elbow['female_less_45_major_joint_shoulder_elbow_507-508_cost'] = major_joint_shoulder_elbow['female_less_45_major_joint_shoulder_elbow_507-508_estimate'] * major_joint_shoulder_elbow['female_less_45_major_joint_shoulder_elbow_507-508']
major_joint_shoulder_elbow['male_plus_45_major_joint_shoulder_elbow_507-508_cost'] = major_joint_shoulder_elbow['male_plus_45_major_joint_shoulder_elbow_507-508_estimate'] * major_joint_shoulder_elbow['male_plus_45_major_joint_shoulder_elbow_507-508']
major_joint_shoulder_elbow['female_plus_45_major_joint_shoulder_elbow_507-508_cost'] = major_joint_shoulder_elbow['female_less_45_major_joint_shoulder_elbow_507-508_estimate'] * major_joint_shoulder_elbow['female_plus_45_major_joint_shoulder_elbow_507-508']
major_joint_shoulder_elbow = major_joint_shoulder_elbow[['male_less_45_major_joint_shoulder_elbow_507-508_cost', 'female_less_45_major_joint_shoulder_elbow_507-508_cost', 'male_plus_45_major_joint_shoulder_elbow_507-508_cost', 'female_plus_45_major_joint_shoulder_elbow_507-508_cost']]

spinal_fusion_curve_malig_infect = merged_costs_filled.filter(regex='456-458')
spinal_fusion_curve_malig_infect['male_less_45_spinal_fusion_curve_malig_infect_456-458_cost'] = spinal_fusion_curve_malig_infect['male_less_45_spinal_fusion_curve_malig_infect_456-458_estimate'] * spinal_fusion_curve_malig_infect['male_less_45_spinal_fusion_curve_malig_infect_456-458']
spinal_fusion_curve_malig_infect['female_less_45_spinal_fusion_curve_malig_infect_456-458_cost'] = spinal_fusion_curve_malig_infect['female_less_45_spinal_fusion_curve_malig_infect_456-458_estimate'] * spinal_fusion_curve_malig_infect['female_less_45_spinal_fusion_curve_malig_infect_456-458']
spinal_fusion_curve_malig_infect['male_plus_45_spinal_fusion_curve_malig_infect_456-458_cost'] = spinal_fusion_curve_malig_infect['male_plus_45_spinal_fusion_curve_malig_infect_456-458_estimate'] * spinal_fusion_curve_malig_infect['male_plus_45_spinal_fusion_curve_malig_infect_456-458']
spinal_fusion_curve_malig_infect['female_plus_45_spinal_fusion_curve_malig_infect_456-458_cost'] = spinal_fusion_curve_malig_infect['female_less_45_spinal_fusion_curve_malig_infect_456-458_estimate'] * spinal_fusion_curve_malig_infect['female_plus_45_spinal_fusion_curve_malig_infect_456-458']
spinal_fusion_curve_malig_infect = spinal_fusion_curve_malig_infect[['male_less_45_spinal_fusion_curve_malig_infect_456-458_cost', 'female_less_45_spinal_fusion_curve_malig_infect_456-458_cost', 'male_plus_45_spinal_fusion_curve_malig_infect_456-458_cost', 'female_plus_45_spinal_fusion_curve_malig_infect_456-458_cost']]

spinal_fusion_except_cervical = merged_costs_filled.filter(regex='459-460')
spinal_fusion_except_cervical['male_less_45_spinal_fusion_except_cervical_459-460_cost'] = spinal_fusion_except_cervical['male_less_45_spinal_fusion_except_cervical_459-460_estimate'] * spinal_fusion_except_cervical['male_less_45_spinal_fusion_except_cervical_459-460']
spinal_fusion_except_cervical['female_less_45_spinal_fusion_except_cervical_459-460_cost'] = spinal_fusion_except_cervical['female_less_45_spinal_fusion_except_cervical_459-460_estimate'] * spinal_fusion_except_cervical['female_less_45_spinal_fusion_except_cervical_459-460']
spinal_fusion_except_cervical['male_plus_45_spinal_fusion_except_cervical_459-460_cost'] = spinal_fusion_except_cervical['male_plus_45_spinal_fusion_except_cervical_459-460_estimate'] * spinal_fusion_except_cervical['male_plus_45_spinal_fusion_except_cervical_459-460']
spinal_fusion_except_cervical['female_plus_45_spinal_fusion_except_cervical_459-460_cost'] = spinal_fusion_except_cervical['female_less_45_spinal_fusion_except_cervical_459-460_estimate'] * spinal_fusion_except_cervical['female_plus_45_spinal_fusion_except_cervical_459-460']
spinal_fusion_except_cervical = spinal_fusion_except_cervical[['male_less_45_spinal_fusion_except_cervical_459-460_cost', 'female_less_45_spinal_fusion_except_cervical_459-460_cost', 'male_plus_45_spinal_fusion_except_cervical_459-460_cost', 'female_plus_45_spinal_fusion_except_cervical_459-460_cost']]

spinal_neuro = merged_costs_filled.filter(regex='28-30')
spinal_neuro['male_less_45_spinal_neuro_28-30_cost'] = spinal_neuro['male_less_45_spinal_neuro_28-30_estimate'] * spinal_neuro['male_less_45_spinal_neuro_28-30']
spinal_neuro['female_less_45_spinal_neuro_28-30_cost'] = spinal_neuro['female_less_45_spinal_neuro_28-30_estimate'] * spinal_neuro['female_less_45_spinal_neuro_28-30']
spinal_neuro['male_plus_45_spinal_neuro_28-30_cost'] = spinal_neuro['male_plus_45_spinal_neuro_28-30_estimate'] * spinal_neuro['male_plus_45_spinal_neuro_28-30']
spinal_neuro['female_plus_45_spinal_neuro_28-30_cost'] = spinal_neuro['female_less_45_spinal_neuro_28-30_estimate'] * spinal_neuro['female_plus_45_spinal_neuro_28-30']
spinal_neuro = spinal_neuro[['male_less_45_spinal_neuro_28-30_cost', 'female_less_45_spinal_neuro_28-30_cost', 'male_plus_45_spinal_neuro_28-30_cost', 'female_plus_45_spinal_neuro_28-30_cost']]

coronary_bypass = merged_costs_filled.filter(regex='234-236')
coronary_bypass['male_less_45_coronary_bypass_234-236_cost'] = coronary_bypass['male_less_45_coronary_bypass_234-236_estimate'] * coronary_bypass['male_less_45_coronary_bypass_234-236']
coronary_bypass['female_less_45_coronary_bypass_234-236_cost'] = coronary_bypass['female_less_45_coronary_bypass_234-236_estimate'] * coronary_bypass['female_less_45_coronary_bypass_234-236']
coronary_bypass['male_plus_45_coronary_bypass_234-236_cost'] = coronary_bypass['male_plus_45_coronary_bypass_234-236_estimate'] * coronary_bypass['male_plus_45_coronary_bypass_234-236']
coronary_bypass['female_plus_45_coronary_bypass_234-236_cost'] = coronary_bypass['female_less_45_coronary_bypass_234-236_estimate'] * coronary_bypass['female_plus_45_coronary_bypass_234-236']
coronary_bypass = coronary_bypass[['male_less_45_coronary_bypass_234-236_cost', 'female_less_45_coronary_bypass_234-236_cost', 'male_plus_45_coronary_bypass_234-236_cost', 'female_plus_45_coronary_bypass_234-236_cost']]

cervical_spinal_fusion = merged_costs_filled.filter(regex='471-473')
cervical_spinal_fusion['male_less_45_cervical_spinal_fusion_471-473_cost'] = cervical_spinal_fusion['male_less_45_cervical_spinal_fusion_471-473_estimate'] * cervical_spinal_fusion['male_less_45_cervical_spinal_fusion_471-473']
cervical_spinal_fusion['female_less_45_cervical_spinal_fusion_471-473_cost'] = cervical_spinal_fusion['female_less_45_cervical_spinal_fusion_471-473_estimate'] * cervical_spinal_fusion['female_less_45_cervical_spinal_fusion_471-473']
cervical_spinal_fusion['male_plus_45_cervical_spinal_fusion_471-473_cost'] = cervical_spinal_fusion['male_plus_45_cervical_spinal_fusion_471-473_estimate'] * cervical_spinal_fusion['male_plus_45_cervical_spinal_fusion_471-473']
cervical_spinal_fusion['female_plus_45_cervical_spinal_fusion_471-473_cost'] = cervical_spinal_fusion['female_less_45_cervical_spinal_fusion_471-473_estimate'] * cervical_spinal_fusion['female_plus_45_cervical_spinal_fusion_471-473']
cervical_spinal_fusion = cervical_spinal_fusion[['male_less_45_cervical_spinal_fusion_471-473_cost', 'female_less_45_cervical_spinal_fusion_471-473_cost', 'male_plus_45_cervical_spinal_fusion_471-473_cost', 'female_plus_45_cervical_spinal_fusion_471-473_cost']]

df_list = [cervical_spinal_fusion, coronary_bypass, spinal_neuro, spinal_fusion_except_cervical, spinal_fusion_curve_malig_infect, major_joint_shoulder_elbow, shoulder_elbow_forearm, other_musc, lower_extremity_humer, knee_other, upper_joint_limb_reattach, hip_knee_revise, hip_knee_replace, hip_femur_not_joint, hand_wrist, bilateral_major_lower_extremity, bariatric, backneck, antpostfusion]
cost_df = pd.concat(df_list, axis=1)

cost_df.to_csv('/Users/lauren/non_claims_presales/output/amgen_total_cost_estimates.csv')
