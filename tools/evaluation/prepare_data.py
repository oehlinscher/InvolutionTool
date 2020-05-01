import pandas as pd 
import os
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", metavar='path')
    parser.add_argument("-f", "--file", metavar='filename')

    args = parser.parse_args()

    data = None
    if args.path is not None:
        data = pd.read_csv(os.path.join(args.path, 'values.csv'), sep=';')
    else:
        raise Exception("No path supplied!")


    # CHECK] multiExec.py -> results.json
    add_column_if_not_exists(data, 0, 'ENVME_reference_group')
    add_column_if_not_exists(data, 1, 'ENVME_group')          

    # [OK] generate.json -> results.json
    add_column_if_not_exists(data, 2, 'CWGn')                         
    add_column_if_not_exists(data, 3, 'CWGmue')                        
    add_column_if_not_exists(data, 4, 'CWGsigma')                     
    add_column_if_not_exists(data, 5, 'CWGcalcnexttransitionmodename')  

    # gate_config.json --> results.json
    add_column_if_not_exists(data, 6, 'GATEST_P')                 
    add_column_if_not_exists(data, 7, 'GATESname')     
    add_column_if_not_exists(data, 8, 'GATESchannel_type')               
    add_column_if_not_exists(data, 9, 'GATESchannel_location')    
    add_column_if_not_exists(data, 10, 'GATESn_up')                
    add_column_if_not_exists(data, 11, 'GATESn_do')               
    add_column_if_not_exists(data, 12, 'GATESx_1_up')      
    add_column_if_not_exists(data, 13, 'GATESx_1_do')                       
    add_column_if_not_exists(data, 14, 'GATEStau_1_up')                    
    add_column_if_not_exists(data, 15, 'GATEStau_1_do')              
    add_column_if_not_exists(data, 16, 'GATEStau_2_up')                 
    add_column_if_not_exists(data, 17, 'GATEStau_2_do')       

    # multiExec.py -> results.json:         This data needs to be written into the results.json file during the multi-execution
    # generate.json -> results.json:        This data need to be written into the results.json file during each-execution 
    # gate_config.json --> results.json:    This is (in general) a list of the values for the specified property. 
    #                                       If we have two relevant gates with say T_P = 1 and T_P = 2 we get a list [1,2]
    
    data = data.groupby(['me_config_id', 'ENVME_reference_group', 'ENVME_group', 'CWGn', 'CWGmue',
        'CWGsigma', 'CWGcalcnexttransitionmodename', 'GATEST_P',  'GATESname', 'GATESchannel_type',
        'GATESchannel_location', 'GATESn_up', 'GATESn_do', 'GATESx_1_up', 'GATESx_1_do', 'GATEStau_1_up', 
        'GATEStau_1_do', 'GATEStau_2_up', 'GATEStau_2_do']).mean()
    
    # Now calculate all the metrics...
    data['total_pos_area_under_dev_trace_inv_per_spice_transition'] = data.apply (lambda row: row['total_pos_area_under_dev_trace_inv']/row['total_tc_spice']*1000, axis=1)
    data['total_neg_area_under_dev_trace_inv_per_spice_transition'] = data.apply (lambda row: row['total_neg_area_under_dev_trace_inv']/row['total_tc_spice']*1000, axis=1)
    data['total_pos_area_under_dev_trace_msim_per_spice_transition'] = data.apply (lambda row: row['total_pos_area_under_dev_trace_msim']/row['total_tc_spice']*1000, axis=1)
    data['total_neg_area_under_dev_trace_msim_per_spice_transition'] = data.apply (lambda row: row['total_neg_area_under_dev_trace_msim']/row['total_tc_spice']*1000, axis=1)
    data['total_pos_area_under_dev_trace_inv_per_actual_transition'] = data.apply (lambda row: row['total_pos_area_under_dev_trace_inv']/row['total_pos_area_under_dev_trace_inv_transitions']*1000, axis=1)
    data['total_neg_area_under_dev_trace_inv_per_actual_transition'] = data.apply (lambda row: row['total_neg_area_under_dev_trace_inv']/row['total_neg_area_under_dev_trace_inv_transitions']*1000, axis=1)
    data['total_pos_area_under_dev_trace_msim_per_actual_transition'] = data.apply (lambda row: row['total_pos_area_under_dev_trace_msim']/row['total_pos_area_under_dev_trace_msim_transitions']*1000, axis=1)
    data['total_neg_area_under_dev_trace_msim_per_actual_transition'] = data.apply (lambda row: row['total_neg_area_under_dev_trace_msim']/row['total_neg_area_under_dev_trace_msim_transitions']*1000, axis=1)
    data['total_pos_area_under_dev_trace_inv_per_actual_transition_wo_glitches'] = data.apply (lambda row: row['total_pos_area_under_dev_trace_inv_wo_glitches']/row['total_pos_area_under_dev_trace_inv_transitions_wo_glitches']*1000, axis=1)
    data['total_neg_area_under_dev_trace_inv_per_actual_transition_wo_glitches'] = data.apply (lambda row: row['total_neg_area_under_dev_trace_inv_wo_glitches']/row['total_neg_area_under_dev_trace_inv_transitions_wo_glitches']*1000, axis=1)	
    data['total_pos_area_under_dev_trace_msim_per_actual_transition_wo_glitches'] = data.apply (lambda row: row['total_pos_area_under_dev_trace_msim_wo_glitches']/row['total_pos_area_under_dev_trace_msim_transitions_wo_glitches']*1000, axis=1)	
    data['total_neg_area_under_dev_trace_msim_per_actual_transition_wo_glitches'] = data.apply (lambda row: row['total_neg_area_under_dev_trace_msim_wo_glitches']/row['total_neg_area_under_dev_trace_msim_transitions_wo_glitches']*1000, axis=1)
    data['total_sum_glitches_inv_per_transition'] = data.apply (lambda row: row['total_sum_glitches_inv']/row['total_tc_inv']*100, axis=1)
    data['total_sum_glitches_orig_inv_per_transition'] = data.apply (lambda row: row['total_sum_glitches_orig_inv']/row['total_tc_inv']*100, axis=1)	
    data['total_sum_glitches_inverted_inv_per_transition'] = data.apply (lambda row: row['total_sum_glitches_inverted_inv']/row['total_tc_inv']*100, axis=1)	
    data['total_sum_glitches_msim_per_transition'] = data.apply (lambda row: row['total_sum_glitches_msim']/row['total_tc_msim']*100, axis=1)	
    data['total_sum_glitches_orig_msim_per_transition'] = data.apply (lambda row: row['total_sum_glitches_orig_msim']/row['total_tc_msim']*100, axis=1)	
    data['total_sum_glitches_inverted_msim_per_transition'] = data.apply (lambda row: row['total_sum_glitches_inverted_msim']/row['total_tc_msim']*100, axis=1)	
    data['total_sum_glitches_spice_inv_per_transition'] = data.apply (lambda row: row['total_sum_glitches_spice_inv']/row['total_tc_spice']*100, axis=1)	
    data['total_sum_glitches_orig_spice_inv_per_transition'] = data.apply (lambda row: row['total_sum_glitches_orig_spice_inv']/row['total_tc_spice']*100, axis=1)
    data['total_sum_glitches_inverted_spice_inv_per_transition'] = data.apply (lambda row: row['total_sum_glitches_inverted_spice_inv']/row['total_tc_spice']*100, axis=1)	
    data['total_sum_glitches_spice_msim_per_transition'] = data.apply (lambda row: row['total_sum_glitches_spice_msim']/row['total_tc_spice']*100, axis=1)
    data['total_sum_glitches_orig_spice_msim_per_transition'] = data.apply (lambda row: row['total_sum_glitches_orig_spice_msim']/row['total_tc_spice']*100, axis=1)
    data['total_sum_glitches_inverted_spice_msim_per_transition'] = data.apply (lambda row: row['total_sum_glitches_inverted_spice_msim']/row['total_tc_spice']*100, axis=1)
    
    # Deviation between SPICE and SPICE trace power estimation
    data['dev_power_spice_vs_spice_dc'] = data.apply (lambda row: relative_change(row['SPICE_DCTotal_Total'], row['SPICEpwr_avg']), axis=1)
    data['dev_power_spice_vs_spice_pt_avg'] = data.apply (lambda row: relative_change(row['SPICE_PT_AVG_total power'], row['SPICEpwr_avg']), axis=1)
    data['dev_power_spice_vs_spice_pt_tim'] = data.apply (lambda row: relative_change(row['SPICE_PT_TIM_total power'], row['SPICEpwr_avg']), axis=1)
    
    # # Deviation between SPICE trace for different tools
    data['dev_power_spice_dc_spice_pt_avg'] = data.apply (lambda row: relative_change(row['SPICE_PT_AVG_total power'], row['SPICE_DCTotal_Total']), axis=1)
    data['dev_power_spice_dc_spice_pt_tim'] = data.apply (lambda row: relative_change(row['SPICE_PT_TIM_total power'], row['SPICE_DCTotal_Total']), axis=1)
    data['dev_power_spice_spice_pt_avg_dc'] = data.apply (lambda row: relative_change(row['SPICE_DCTotal_Total'], row['SPICE_PT_AVG_total power']), axis=1)
    data['dev_power_spice_spice_pt_avg_pt_tim'] = data.apply (lambda row: relative_change(row['SPICE_PT_TIM_total power'], row['SPICE_PT_AVG_total power']), axis=1)
    data['dev_power_spice_pt_tim_dc'] = data.apply (lambda row: relative_change(row['SPICE_DCTotal_Total'], row['SPICE_PT_TIM_total power']), axis=1)
    data['dev_power_spice_pt_tim_pt_avg'] = data.apply (lambda row: relative_change(row['SPICE_PT_AVG_total power'], row['SPICE_PT_TIM_total power']), axis=1)

    data['dev_power_max_spice_trace'] = data.apply (lambda row: max(abs(row['dev_power_spice_dc_spice_pt_avg']), abs(row['dev_power_spice_dc_spice_pt_tim']), 
        abs(row['dev_power_spice_spice_pt_avg_dc']), abs(row['dev_power_spice_spice_pt_avg_pt_tim']), abs(row['dev_power_spice_pt_tim_dc']), 
        abs(row['dev_power_spice_pt_tim_pt_avg'])), axis=1)


    data.to_csv(os.path.join(args.path, 'evaluation.csv'), sep=';')

def add_column_if_not_exists(data, idx, column_name):    
    if not column_name in data:
        data.insert(idx, column_name, '')    


def relative_change(x, x_reference):
    return (x-x_reference)/x_reference*100


if __name__ == "__main__":
    main()