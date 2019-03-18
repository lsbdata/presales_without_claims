import pandas as pd
import numpy as np
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.options.mode.chained_assignment = None  # default='warn'



#regions = pd.read_csv('non_claims_presales/input/state_regions.csv', header=0)
costs = pd.read_csv('pre_sales/non_claims_presales/output/his_cost_estimates.csv', header=[0, 1])
bhi_470 = pd.read_csv('pre_sales/non_claims_presales/input/bhi_470_costs.csv', header=0)
carrum_drgs = pd.read_csv('pre_sales/non_claims_presales/input/carrum_drg_prices.csv', header=0)

costs.columns = costs.columns.map('|'.join)

#region_costs = pd.merge(costs, regions, how='right', left_on='Unnamed: 0_level_0|drg_column', right_on='state_code')
#region_costs.to_csv('non_claims_presales/output/his_region_cost_estimates.csv')

bhi_470_costs = pd.merge(costs, bhi_470, how='right', left_on='Unnamed: 0_level_0|drg_column', right_on='state_code')
#bhi_470_costs.to_csv('non_claims_presales/output/bhi_470_costs.csv')


bhi_470_costs['min_470_cost'] = bhi_470_costs[['female_less_45|hip_knee_replace_469-470', 'male_less_45|hip_knee_replace_469-470', 'male_plus_45|hip_knee_replace_469-470', 'female_plus_45|hip_knee_replace_469-470']].min(axis=1)
bhi_470_costs['min_470_scaler'] = np.where(bhi_470_costs['min_470_cost'] <= 28200, (bhi_470_costs['470_bhi_cost']-bhi_470_costs['min_470_cost'])/bhi_470_costs['min_470_cost'], 0)
bhi_470_costs['min_470_scaler'] = np.where(bhi_470_costs['min_470_scaler'] < 0.0, 0, bhi_470_costs['min_470_scaler'])
bhi_470_costs.at[21, 'min_470_scaler'] = 0.5 #NY
bhi_470_costs.at[46, 'min_470_scaler'] = 0.4 #PA
bhi_470_costs.at[19, 'min_470_scaler'] = 0.9 #NJ


#bhi_470_costs[['min_470_scaler', 'state_code']]

bhi_470_costs['bhi_adj_unit_cost|male_less_45|antpostfusion|453-455'] = bhi_470_costs['male_less_45|antpostfusion_453-455'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|antpostfusion_453-455'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|backneck|518-520'] = bhi_470_costs['male_less_45|backneck_518-520'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|backneck_518-520'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|bariatric|619-621'] = bhi_470_costs['male_less_45|bariatric_619-621'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|bariatric_619-621'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|bilateral_major_lower_extremity|461-462'] = bhi_470_costs['male_less_45|bilateral_major_lower_extremity_461-462'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|bilateral_major_lower_extremity_461-462'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|cervical_spinal_fusion|471-473'] = bhi_470_costs['male_less_45|cervical_spinal_fusion_471-473'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|cervical_spinal_fusion_471-473'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|coronary_bypass|234-236'] = bhi_470_costs['male_less_45|coronary_bypass_234-236'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|coronary_bypass_234-236'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|hand_wrist|513-514'] = bhi_470_costs['male_less_45|hand_wrist_513-514'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|hand_wrist_513-514'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|hip_femur_not_joint|480-482'] = bhi_470_costs['male_less_45|hip_femur_not_joint_480-482'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|hip_femur_not_joint_480-482'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|hip_knee_replace|469-470'] = bhi_470_costs['male_less_45|hip_knee_replace_469-470'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|hip_knee_replace_469-470'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|hip_knee_revise|466-468'] = bhi_470_costs['male_less_45|hip_knee_revise_466-468'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|hip_knee_revise_466-468'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|knee_other|485-489'] = bhi_470_costs['male_less_45|knee_other_485-489'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|knee_other_485-489'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|lower_extremity_humer|492-494'] = bhi_470_costs['male_less_45|lower_extremity_humer_492-494'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|lower_extremity_humer_492-494'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|major_joint_shoulder_elbow|507-508'] = bhi_470_costs['male_less_45|major_joint_shoulder_elbow_507-508'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|major_joint_shoulder_elbow_507-508'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|other_musc|515-517'] = bhi_470_costs['male_less_45|other_musc_515-517'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|other_musc_515-517'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|shoulder_elbow_forearm|510-512'] = bhi_470_costs['male_less_45|shoulder_elbow_forearm_510-512'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|shoulder_elbow_forearm_510-512'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|spinal_fusion_curve_malig_infect|456-458'] = bhi_470_costs['male_less_45|spinal_fusion_curve_malig_infect_456-458'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|spinal_fusion_curve_malig_infect_456-458'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|spinal_fusion_except_cervical|459-460'] = bhi_470_costs['male_less_45|spinal_fusion_except_cervical_459-460'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|spinal_fusion_except_cervical_459-460'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|spinal_neuro|28-30'] = bhi_470_costs['male_less_45|spinal_neuro_28-30'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|spinal_neuro_28-30'])
bhi_470_costs['bhi_adj_unit_cost|male_less_45|upper_joint_limb_reattach|483-484'] = bhi_470_costs['male_less_45|upper_joint_limb_reattach_483-484'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_less_45|upper_joint_limb_reattach_483-484'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|antpostfusion|453-455'] = bhi_470_costs['female_less_45|antpostfusion_453-455'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|antpostfusion_453-455'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|backneck|518-520'] = bhi_470_costs['female_less_45|backneck_518-520'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|backneck_518-520'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|bariatric|619-621'] = bhi_470_costs['female_less_45|bariatric_619-621'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|bariatric_619-621'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|bilateral_major_lower_extremity|461-462'] = bhi_470_costs['female_less_45|bilateral_major_lower_extremity_461-462'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|bilateral_major_lower_extremity_461-462'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|cervical_spinal_fusion|471-473'] = bhi_470_costs['female_less_45|cervical_spinal_fusion_471-473'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|cervical_spinal_fusion_471-473'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|coronary_bypass|234-236'] = bhi_470_costs['female_less_45|coronary_bypass_234-236'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|coronary_bypass_234-236'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|hand_wrist|513-514'] = bhi_470_costs['female_less_45|hand_wrist_513-514'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|hand_wrist_513-514'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|hip_femur_not_joint|480-482'] = bhi_470_costs['female_less_45|hip_femur_not_joint_480-482'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|hip_femur_not_joint_480-482'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|hip_knee_replace|469-470'] = bhi_470_costs['female_less_45|hip_knee_replace_469-470'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|hip_knee_replace_469-470'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|hip_knee_revise|466-468'] = bhi_470_costs['female_less_45|hip_knee_revise_466-468'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|hip_knee_revise_466-468'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|knee_other|485-489'] = bhi_470_costs['female_less_45|knee_other_485-489'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|knee_other_485-489'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|lower_extremity_humer|492-494'] = bhi_470_costs['female_less_45|lower_extremity_humer_492-494'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|lower_extremity_humer_492-494'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|major_joint_shoulder_elbow|507-508'] = bhi_470_costs['female_less_45|major_joint_shoulder_elbow_507-508'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|major_joint_shoulder_elbow_507-508'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|other_musc|515-517'] = bhi_470_costs['female_less_45|other_musc_515-517'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|other_musc_515-517'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|shoulder_elbow_forearm|510-512'] = bhi_470_costs['female_less_45|shoulder_elbow_forearm_510-512'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|shoulder_elbow_forearm_510-512'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|spinal_fusion_curve_malig_infect|456-458'] = bhi_470_costs['female_less_45|spinal_fusion_curve_malig_infect_456-458'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|spinal_fusion_curve_malig_infect_456-458'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|spinal_fusion_except_cervical|459-460'] = bhi_470_costs['female_less_45|spinal_fusion_except_cervical_459-460'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|spinal_fusion_except_cervical_459-460'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|spinal_neuro|28-30'] = bhi_470_costs['female_less_45|spinal_neuro_28-30'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|spinal_neuro_28-30'])
bhi_470_costs['bhi_adj_unit_cost|female_less_45|upper_joint_limb_reattach|483-484'] = bhi_470_costs['female_less_45|upper_joint_limb_reattach_483-484'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_less_45|upper_joint_limb_reattach_483-484'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|antpostfusion|453-455'] = bhi_470_costs['male_plus_45|antpostfusion_453-455'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|antpostfusion_453-455'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|backneck|518-520'] = bhi_470_costs['male_plus_45|backneck_518-520'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|backneck_518-520'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|bariatric|619-621'] = bhi_470_costs['male_plus_45|bariatric_619-621'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|bariatric_619-621'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|bilateral_major_lower_extremity|461-462'] = bhi_470_costs['male_plus_45|bilateral_major_lower_extremity_461-462'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|bilateral_major_lower_extremity_461-462'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|cervical_spinal_fusion|471-473'] = bhi_470_costs['male_plus_45|cervical_spinal_fusion_471-473'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|cervical_spinal_fusion_471-473'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|coronary_bypass|234-236'] = bhi_470_costs['male_plus_45|coronary_bypass_234-236'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|coronary_bypass_234-236'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|hand_wrist|513-514'] = bhi_470_costs['male_plus_45|hand_wrist_513-514'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|hand_wrist_513-514'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|hip_femur_not_joint|480-482'] = bhi_470_costs['male_plus_45|hip_femur_not_joint_480-482'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|hip_femur_not_joint_480-482'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|hip_knee_replace|469-470'] = bhi_470_costs['male_plus_45|hip_knee_replace_469-470'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|hip_knee_replace_469-470'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|hip_knee_revise|466-468'] = bhi_470_costs['male_plus_45|hip_knee_revise_466-468'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|hip_knee_revise_466-468'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|knee_other|485-489'] = bhi_470_costs['male_plus_45|knee_other_485-489'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|knee_other_485-489'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|lower_extremity_humer|492-494'] = bhi_470_costs['male_plus_45|lower_extremity_humer_492-494'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|lower_extremity_humer_492-494'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|major_joint_shoulder_elbow|507-508'] = bhi_470_costs['male_plus_45|major_joint_shoulder_elbow_507-508'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|major_joint_shoulder_elbow_507-508'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|other_musc|515-517'] = bhi_470_costs['male_plus_45|other_musc_515-517'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|other_musc_515-517'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|shoulder_elbow_forearm|510-512'] = bhi_470_costs['male_plus_45|shoulder_elbow_forearm_510-512'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|shoulder_elbow_forearm_510-512'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|spinal_fusion_curve_malig_infect|456-458'] = bhi_470_costs['male_plus_45|spinal_fusion_curve_malig_infect_456-458'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|spinal_fusion_curve_malig_infect_456-458'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|spinal_fusion_except_cervical|459-460'] = bhi_470_costs['male_plus_45|spinal_fusion_except_cervical_459-460'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|spinal_fusion_except_cervical_459-460'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|spinal_neuro|28-30'] = bhi_470_costs['male_plus_45|spinal_neuro_28-30'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|spinal_neuro_28-30'])
bhi_470_costs['bhi_adj_unit_cost|male_plus_45|upper_joint_limb_reattach|483-484'] = bhi_470_costs['male_plus_45|upper_joint_limb_reattach_483-484'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['male_plus_45|upper_joint_limb_reattach_483-484'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|antpostfusion|453-455'] = bhi_470_costs['female_plus_45|antpostfusion_453-455'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|antpostfusion_453-455'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|backneck|518-520'] = bhi_470_costs['female_plus_45|backneck_518-520'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|backneck_518-520'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|bariatric|619-621'] = bhi_470_costs['female_plus_45|bariatric_619-621'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|bariatric_619-621'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|bilateral_major_lower_extremity|461-462'] = bhi_470_costs['female_plus_45|bilateral_major_lower_extremity_461-462'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|bilateral_major_lower_extremity_461-462'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|cervical_spinal_fusion|471-473'] = bhi_470_costs['female_plus_45|cervical_spinal_fusion_471-473'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|cervical_spinal_fusion_471-473'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|coronary_bypass|234-236'] = bhi_470_costs['female_plus_45|coronary_bypass_234-236'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|coronary_bypass_234-236'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|hand_wrist|513-514'] = bhi_470_costs['female_plus_45|hand_wrist_513-514'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|hand_wrist_513-514'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|hip_femur_not_joint|480-482'] = bhi_470_costs['female_plus_45|hip_femur_not_joint_480-482'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|hip_femur_not_joint_480-482'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|hip_knee_replace|469-470'] = bhi_470_costs['female_plus_45|hip_knee_replace_469-470'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|hip_knee_replace_469-470'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|hip_knee_revise|466-468'] = bhi_470_costs['female_plus_45|hip_knee_revise_466-468'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|hip_knee_revise_466-468'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|knee_other|485-489'] = bhi_470_costs['female_plus_45|knee_other_485-489'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|knee_other_485-489'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|lower_extremity_humer|492-494'] = bhi_470_costs['female_plus_45|lower_extremity_humer_492-494'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|lower_extremity_humer_492-494'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|major_joint_shoulder_elbow|507-508'] = bhi_470_costs['female_plus_45|major_joint_shoulder_elbow_507-508'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|major_joint_shoulder_elbow_507-508'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|other_musc|515-517'] = bhi_470_costs['female_plus_45|other_musc_515-517'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|other_musc_515-517'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|shoulder_elbow_forearm|510-512'] = bhi_470_costs['female_plus_45|shoulder_elbow_forearm_510-512'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|shoulder_elbow_forearm_510-512'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|spinal_fusion_curve_malig_infect|456-458'] = bhi_470_costs['female_plus_45|spinal_fusion_curve_malig_infect_456-458'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|spinal_fusion_curve_malig_infect_456-458'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|spinal_fusion_except_cervical|459-460'] = bhi_470_costs['female_plus_45|spinal_fusion_except_cervical_459-460'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|spinal_fusion_except_cervical_459-460'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|spinal_neuro|28-30'] = bhi_470_costs['female_plus_45|spinal_neuro_28-30'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|spinal_neuro_28-30'])
bhi_470_costs['bhi_adj_unit_cost|female_plus_45|upper_joint_limb_reattach|483-484'] = bhi_470_costs['female_plus_45|upper_joint_limb_reattach_483-484'] + (bhi_470_costs['min_470_scaler'] * bhi_470_costs['female_plus_45|upper_joint_limb_reattach_483-484'])


bhi_adj = bhi_470_costs[['state_code', 'min_470_scaler',
         'bhi_adj_unit_cost|male_less_45|antpostfusion|453-455',
         'bhi_adj_unit_cost|male_less_45|backneck|518-520',
         'bhi_adj_unit_cost|male_less_45|bariatric|619-621',
         'bhi_adj_unit_cost|male_less_45|bilateral_major_lower_extremity|461-462',
         'bhi_adj_unit_cost|male_less_45|cervical_spinal_fusion|471-473',
         'bhi_adj_unit_cost|male_less_45|coronary_bypass|234-236',
         'bhi_adj_unit_cost|male_less_45|hand_wrist|513-514',
         'bhi_adj_unit_cost|male_less_45|hip_femur_not_joint|480-482',
         'bhi_adj_unit_cost|male_less_45|hip_knee_replace|469-470',
         'bhi_adj_unit_cost|male_less_45|hip_knee_revise|466-468',
         'bhi_adj_unit_cost|male_less_45|knee_other|485-489',
         'bhi_adj_unit_cost|male_less_45|lower_extremity_humer|492-494',
         'bhi_adj_unit_cost|male_less_45|major_joint_shoulder_elbow|507-508',
         'bhi_adj_unit_cost|male_less_45|other_musc|515-517',
         'bhi_adj_unit_cost|male_less_45|shoulder_elbow_forearm|510-512',
         'bhi_adj_unit_cost|male_less_45|spinal_fusion_curve_malig_infect|456-458',
         'bhi_adj_unit_cost|male_less_45|spinal_fusion_except_cervical|459-460',
         'bhi_adj_unit_cost|male_less_45|spinal_neuro|28-30',
         'bhi_adj_unit_cost|male_less_45|upper_joint_limb_reattach|483-484',
         'bhi_adj_unit_cost|female_less_45|antpostfusion|453-455',
         'bhi_adj_unit_cost|female_less_45|backneck|518-520',
         'bhi_adj_unit_cost|female_less_45|bariatric|619-621',
         'bhi_adj_unit_cost|female_less_45|bilateral_major_lower_extremity|461-462',
         'bhi_adj_unit_cost|female_less_45|cervical_spinal_fusion|471-473',
         'bhi_adj_unit_cost|female_less_45|coronary_bypass|234-236',
         'bhi_adj_unit_cost|female_less_45|hand_wrist|513-514',
         'bhi_adj_unit_cost|female_less_45|hip_femur_not_joint|480-482',
         'bhi_adj_unit_cost|female_less_45|hip_knee_replace|469-470',
         'bhi_adj_unit_cost|female_less_45|hip_knee_revise|466-468',
         'bhi_adj_unit_cost|female_less_45|knee_other|485-489',
         'bhi_adj_unit_cost|female_less_45|lower_extremity_humer|492-494',
         'bhi_adj_unit_cost|female_less_45|major_joint_shoulder_elbow|507-508',
         'bhi_adj_unit_cost|female_less_45|other_musc|515-517',
         'bhi_adj_unit_cost|female_less_45|shoulder_elbow_forearm|510-512',
         'bhi_adj_unit_cost|female_less_45|spinal_fusion_curve_malig_infect|456-458',
         'bhi_adj_unit_cost|female_less_45|spinal_fusion_except_cervical|459-460',
         'bhi_adj_unit_cost|female_less_45|spinal_neuro|28-30',
         'bhi_adj_unit_cost|female_less_45|upper_joint_limb_reattach|483-484',
         'bhi_adj_unit_cost|male_plus_45|antpostfusion|453-455',
         'bhi_adj_unit_cost|male_plus_45|backneck|518-520',
         'bhi_adj_unit_cost|male_plus_45|bariatric|619-621',
         'bhi_adj_unit_cost|male_plus_45|bilateral_major_lower_extremity|461-462',
         'bhi_adj_unit_cost|male_plus_45|cervical_spinal_fusion|471-473',
         'bhi_adj_unit_cost|male_plus_45|coronary_bypass|234-236',
         'bhi_adj_unit_cost|male_plus_45|hand_wrist|513-514',
         'bhi_adj_unit_cost|male_plus_45|hip_femur_not_joint|480-482',
         'bhi_adj_unit_cost|male_plus_45|hip_knee_replace|469-470',
         'bhi_adj_unit_cost|male_plus_45|hip_knee_revise|466-468',
         'bhi_adj_unit_cost|male_plus_45|knee_other|485-489',
         'bhi_adj_unit_cost|male_plus_45|lower_extremity_humer|492-494',
         'bhi_adj_unit_cost|male_plus_45|major_joint_shoulder_elbow|507-508',
         'bhi_adj_unit_cost|male_plus_45|other_musc|515-517',
         'bhi_adj_unit_cost|male_plus_45|shoulder_elbow_forearm|510-512',
         'bhi_adj_unit_cost|male_plus_45|spinal_fusion_curve_malig_infect|456-458',
         'bhi_adj_unit_cost|male_plus_45|spinal_fusion_except_cervical|459-460',
         'bhi_adj_unit_cost|male_plus_45|spinal_neuro|28-30',
         'bhi_adj_unit_cost|male_plus_45|upper_joint_limb_reattach|483-484',
         'bhi_adj_unit_cost|female_plus_45|antpostfusion|453-455',
         'bhi_adj_unit_cost|female_plus_45|backneck|518-520',
         'bhi_adj_unit_cost|female_plus_45|bariatric|619-621',
         'bhi_adj_unit_cost|female_plus_45|bilateral_major_lower_extremity|461-462',
         'bhi_adj_unit_cost|female_plus_45|cervical_spinal_fusion|471-473',
         'bhi_adj_unit_cost|female_plus_45|coronary_bypass|234-236',
         'bhi_adj_unit_cost|female_plus_45|hand_wrist|513-514',
         'bhi_adj_unit_cost|female_plus_45|hip_femur_not_joint|480-482',
         'bhi_adj_unit_cost|female_plus_45|hip_knee_replace|469-470',
         'bhi_adj_unit_cost|female_plus_45|hip_knee_revise|466-468',
         'bhi_adj_unit_cost|female_plus_45|knee_other|485-489',
         'bhi_adj_unit_cost|female_plus_45|lower_extremity_humer|492-494',
         'bhi_adj_unit_cost|female_plus_45|major_joint_shoulder_elbow|507-508',
         'bhi_adj_unit_cost|female_plus_45|other_musc|515-517',
         'bhi_adj_unit_cost|female_plus_45|shoulder_elbow_forearm|510-512',
         'bhi_adj_unit_cost|female_plus_45|spinal_fusion_curve_malig_infect|456-458',
         'bhi_adj_unit_cost|female_plus_45|spinal_fusion_except_cervical|459-460',
         'bhi_adj_unit_cost|female_plus_45|spinal_neuro|28-30',
         'bhi_adj_unit_cost|female_plus_45|upper_joint_limb_reattach|483-484']]


bhi_adj_t = bhi_adj.T
bhi_adj_t.columns = bhi_adj_t.iloc[0]

bhi_adj_t['index'] = bhi_adj_t.index
bhi_adj_t[['unit_cost_variable', 'demographic_group', 'procedure', 'drg_group']] = bhi_adj_t['index'].str.split('|', expand=True)

#carrum_drgs_group = carrum_drgs.groupby('DRG_group').agg({'carrum_price_min':'mean'}).reset_index()
carrum_drgs_group = carrum_drgs.groupby('DRG_group').agg({'carrum_price_mean':'mean', 'carrum_price_min':'mean'}).reset_index()

prices_costs_carrum = pd.merge(bhi_adj_t, carrum_drgs_group, how='left', left_on='drg_group', right_on='DRG_group')

#prices_costs = prices_costs_carrum.loc[prices_costs_carrum['carrum_price_min'] >0]
prices_costs = prices_costs_carrum.loc[prices_costs_carrum['carrum_price_mean'] >0]

prices_costs['AZ|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['AR|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['CA|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['CO|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['FL|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['HI|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['IL|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['IN|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['IA|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['KS|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['KY|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['ME|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['MD|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['MA|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['MI|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['MI']/prices_costs['CA']) -1))
prices_costs['MN|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['MO|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['MO']/prices_costs['CA']) -1))
prices_costs['NE|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['NV|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['NJ|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['NJ']/prices_costs['CA']) -1))
prices_costs['NM|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['NY|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['NY']/prices_costs['CA']) -1))
prices_costs['NC|Carrum_Price'] = prices_costs['carrum_price_min'] #using min here because carrum price looks high for this state, even though scaling suggests should be higher
#prices_costs['NC|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['NC']/prices_costs['CA']) -1))
prices_costs['ND|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['OK|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['OR|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['RI|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['SC|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['SC']/prices_costs['CA']) -1))
prices_costs['TN|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['TN']/prices_costs['CA']) -1))
prices_costs['TX|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['UT|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['UT']/prices_costs['CA']) -1))
prices_costs['VT|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['VT']/prices_costs['CA']) -1))
prices_costs['WA|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['WA']/prices_costs['CA']) -1))
prices_costs['WV|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['WV']/prices_costs['CA']) -1))
prices_costs['WI|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['WY|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['WY']/prices_costs['CA']) -1))
prices_costs['VA|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['MS|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['MS']/prices_costs['CA']) -1))
prices_costs['LA|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['GA|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['GA']/prices_costs['CA']) -1))
prices_costs['AL|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['MT|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['MT']/prices_costs['CA']) -1))
prices_costs['ID|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['ID']/prices_costs['CA']) -1))
prices_costs['SD|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['NH|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['CT|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['PA|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['DE|Carrum_Price'] = prices_costs['carrum_price_mean']/(1 - ((prices_costs['DE']/prices_costs['CA']) -1))
prices_costs['DC|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['OH|Carrum_Price'] = prices_costs['carrum_price_min']
prices_costs['AK|Carrum_Price'] = prices_costs['carrum_price_min']

carrum_state_prices = prices_costs[['index',
             'demographic_group',
             'procedure',
             'drg_group',
             'AZ|Carrum_Price',
             'AR|Carrum_Price',
             'CA|Carrum_Price',
             'CO|Carrum_Price',
             'FL|Carrum_Price',
             'HI|Carrum_Price',
             'IL|Carrum_Price',
             'IN|Carrum_Price',
             'IA|Carrum_Price',
             'KS|Carrum_Price',
             'KY|Carrum_Price',
             'ME|Carrum_Price',
             'MD|Carrum_Price',
             'MA|Carrum_Price',
             'MI|Carrum_Price',
             'MN|Carrum_Price',
             'MO|Carrum_Price',
             'NE|Carrum_Price',
             'NV|Carrum_Price',
             'NJ|Carrum_Price',
             'NM|Carrum_Price',
             'NY|Carrum_Price',
             'NC|Carrum_Price',
             'ND|Carrum_Price',
             'OK|Carrum_Price',
             'OR|Carrum_Price',
             'RI|Carrum_Price',
             'SC|Carrum_Price',
             'TN|Carrum_Price',
             'TX|Carrum_Price',
             'UT|Carrum_Price',
             'VT|Carrum_Price',
             'WA|Carrum_Price',
             'WV|Carrum_Price',
             'WI|Carrum_Price',
             'WY|Carrum_Price',
             'VA|Carrum_Price',
             'MS|Carrum_Price',
             'LA|Carrum_Price',
             'GA|Carrum_Price',
             'AL|Carrum_Price',
             'MT|Carrum_Price',
             'ID|Carrum_Price',
             'SD|Carrum_Price',
             'NH|Carrum_Price',
             'CT|Carrum_Price',
             'PA|Carrum_Price',
             'DE|Carrum_Price',
             'DC|Carrum_Price',
             'OH|Carrum_Price',
             'AK|Carrum_Price']]

carrum_state_prices_t = carrum_state_prices.T
carrum_state_prices_t.columns = carrum_state_prices_t.iloc[1] + '_' + carrum_state_prices_t.iloc[2] + '_' + carrum_state_prices_t.iloc[3]

carrum_state_prices_t['state_info'] = carrum_state_prices_t.index
carrum_state_prices_t[['state', 'price_type']] = carrum_state_prices_t['state_info'].str.split('|', expand=True)

carrum_state_prices_t.drop(['price_type'], axis=1, inplace=True)
carrum_state_prices_t.index = carrum_state_prices_t['state']
carrum_state_prices_t.drop(['state_info', 'state'], axis=1, inplace=True)

carrum_state_prices_t.drop(['index','demographic_group', 'procedure', 'drg_group'])


carrum_state_prices_t.to_csv('pre_sales/non_claims_presales/output/estimated_carrum_prices.csv')

bhi_adj_costs =  prices_costs[['index',
             'demographic_group',
             'procedure',
             'drg_group',
             'AZ',
             'AR',
             'CA',
             'CO',
             'FL',
             'HI',
             'IL',
             'IN',
             'IA',
             'KS',
             'KY',
             'ME',
             'MD',
             'MA',
             'MI',
             'MN',
             'MO',
             'NE',
             'NV',
             'NJ',
             'NM',
             'NY',
             'NC',
             'ND',
             'OK',
             'OR',
             'RI',
             'SC',
             'TN',
             'TX',
             'UT',
             'VT',
             'WA',
             'WV',
             'WI',
             'WY',
             'VA',
             'MS',
             'LA',
             'GA',
             'AL',
             'MT',
             'ID',
             'SD',
             'NH',
             'CT',
             'PA',
             'DE',
             'DC',
             'OH',
             'AK']]


bhi_adj_costs_t = bhi_adj_costs.T
bhi_adj_costs_t['state_info'] = bhi_adj_costs_t.index

bhi_adj_costs_t.columns = bhi_adj_costs_t.iloc[1] + '_' + bhi_adj_costs_t.iloc[2] + '_' + bhi_adj_costs_t.iloc[3]
bhi_adj_costs_t.drop(['index','demographic_group', 'procedure', 'drg_group'])

bhi_adj_costs_t.drop(['demographic_group_procedure_drg_group'], axis=1, inplace=True)


bhi_adj_costs_t.to_csv('pre_sales/non_claims_presales/output/bhi_470_costs.csv')
