#!/bin/bash
function DEBUG()
       {
           [ "$_DEBUG" == "on" ] && $@ || :
       }


_DEBUG=on

for min in "none"
# "all"
do
    for expSig in 1
# 0
    do
	for range in  5
# 1 2 10
	do
	    for algo in 1
#0 2 1 3
	    do
		echo ""; echo "expSig=${expSig}, range=${range}, algo=${algo}, minos=${min}"; echo "";
		cmdFit="combine -M MaxLikelihoodFit -t -1 --expectSignal $expSig --rMin -$range --rMax $range --cminDefaultMinimizerStrategy $algo --minos=${min} --X-rtd MINIMIZER_analytic comb_tot_nominalCombination_M300_mc.root"
		
		#DEBUG echo $cmdFit
		#set -x;
		echo $cmdFit;
		#set +x;
		eval $cmdFit
		

		cmdMove="mv fitDiagnostics.root fitDiagnostics_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.root"
		echo ""; echo $cmdMove; eval $cmdMove
		
		cmdDiffNuisance="python diffNuisances_manual.py fitDiagnostics_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.root -g plots_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.root -f html > Comparison_of_nuisances_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.html -a -A" 
                #>& log_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.txt"
		echo ""; echo $cmdDiffNuisance; eval $cmdDiffNuisance
		#echo "early exiting on purpose..."; exit
		
	    done
	done
    done
done
cp Comparison_of_nuisances_expectSignal1_range5_algo1_minosnone.html Comparison_of_nuisances_expectSignal1.html 
cp Comparison_of_nuisances*  ~/www/april11
          



for min in "none"
# "all"
do
    for expSig in 0
# 0
    do
	for range in  1
# 1 1000 10 100
	do
	    for algo in 2
#0 2 1 3
	    do
		echo ""; echo "expSig=${expSig}, range=${range}, algo=${algo}, minos=${min}"; echo "";
		cmdFit="combine -M MaxLikelihoodFit -t -1 --expectSignal $expSig --rMin -$range --rMax $range --cminDefaultMinimizerStrategy $algo --minos=${min} --X-rtd MINIMIZER_analytic comb_tot_nominalCombination_M300_mc.root"
		
		#DEBUG echo $cmdFit
		#set -x;
		echo $cmdFit;
		#set +x;
		eval $cmdFit
		

		cmdMove="mv fitDiagnostics.root fitDiagnostics_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.root"
		echo ""; echo $cmdMove; eval $cmdMove
		
		cmdDiffNuisance="python diffNuisances_manual.py fitDiagnostics_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.root -g plots_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.root -f html > Comparison_of_nuisances_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.html -a -A" 
                #>& log_expectSignal${expSig}_range${range}_algo${algo}_minos${min}.txt"
		echo ""; echo $cmdDiffNuisance; eval $cmdDiffNuisance
		#echo "early exiting on purpose..."; exit
		
	    done
	done
    done
done
cp Comparison_of_nuisances_expectSignal0_range1_algo2_minosnone.html Comparison_of_nuisances_expectSignal0.html
cp Comparison_of_nuisances*  ~/www/april11
          
