For easy evaluation of the results use the Python script generate_plots.py and specify the desired parameters
The filename is required, all other parameters are optional:
-r 	Filter for a list of reg groups. 
	A ref group contains all datapoints for a specific waveform configuration 
	(including the different sweeps over channel parameters)
-g 	Filter for a list of group ids. 
	A group is a specific configuration which contains 
	all T_P datapoints for this configuration
-m 	Can be used if only certain metrics are of interest
	Highly recommended to use only up to 5 metrics, otherwise the plots become to small, 
	and I was not able to implement a scrollbar unitl now.
	The older simulations (c17_slack: 01, 02, 03 and inv_tree: 01, 02) do not contain some of the metrics (4, 5, 7, 8, 10, 11)
	 0 ... power deviation
	 1 ... max. trans. count dev.
	 2 ... avg. trans. count dev.
	 3 ... area under dev. trace
	 4 ... pos. area under dev. trace
	 5 ... neg. area under dev. trace
	 6 ... induced glitches
	 7 ... orig. induced glitches
	 8 ... inverted. induced glitches
	 9 ... suppressed glitches
	10 ... orig. suppressed glitches
	11 ... inverted. suppressed glitches
	12 ... leading against spice per transition
	13 ... trailing against spice per transition
	14 ... leading against actual transition
	15 ... trailing against actual transition
	16 ... leading against actual transition w.o. glitches
	17 ... trailing against actual transition w.o. glitches
	18 ... induced glitch percentage
	19 ... induced orig. glitch percentage
	20 ... induced inverted glitch percentage
	21 ... suppressed glitch percentage
	22 ... suppressed orig. glitch percentage
	23 ... suppressed inverted glitch percentage
	
It is always a good idea to start with option -r 0, so that all results for a certain waveform configuration are shown.
If these yields to much traces, one could filter the groups (-g), but therefore one has to look into the evaluation.csv file
to find out which group uses which parameters
	
--------------------------------------------------------
	
Post-processing of the values.csv file (currently still manually with Excel):
> Sort by me_config_id
> Data -> Subtotal -> Use function average, select all numeric columns (all columns except me_config_id and folder_name)
> Minimize all groupings (on the left hand side, by clicking on "2", all groups can be minimized
> Select table -> Home - find & select -> Go To Special -> Visible cells only -> Ctrl-C
> Copy in new xlsx file and save
> Remove column folder name in xlsx file
> Add columns: reference_group, group, T_P, trans_mode, mu, sigma, n_up, n_do in xlsx file
> Add caluclated columns in xlsx File 
> Save as evaluation.csv file for use with the generate_plots script

> TODO Conversion: 
This process should be made with a script:
> Starting from the values.csv file of the multi_execution: 
> the rows should be ordered by the me_config_id, 
> average values calculated, 
> calculated columns should be calculated (use a configuration file for this)
> additional columns like T_P, ... should be added, according to the multi_exec.json File
> saved as evaluation.csv which is then read by the generate_plots script

> TODO generate_plots.py
> Instead of adding each new metric, a configuration file should be used, where a triple is saved for each metric (involution_column_name, modelsim_column_name, y_label)
