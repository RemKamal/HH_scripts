mass=300
blindOrNot="" #" -t -1 "

echo ""
echo "THESE COMMANDS PRODUCE WORKSPACES!!!"
echo ""

text2workspace.py comb_tot_nominalCombination_M${mass}_mc.txt

for range in 10 50 100 500 #for 900 GeV
# 500 1000 1500 for 300 GeV

#15 30 
#50 80 100 150 200 300 500 700 1000
#300 
#500 1000
# 10000 1 2
#1000 100 10 5 1
do

    region=""
    if [[ $range = "0" ]]; then
        region=""
        echo "region=${region}"
    else
	region=" --rMin -${range} --rMax ${range} "
        echo "region=${region}"
    fi
    for algo in " --cminDefaultMinimizerStrategy 2" 
#" --cminDefaultMinimizerStrategy 1 " " --cminDefaultMinimizerStrategy 0 "
    do
	region+=" --X-rtd MINIMIZER_analytic "
	region+=${algo}
#--cminDefaultMinimizerTolerance 0.05 "
	echo "FINAL region=${region}"

	echo ""
	echo "THESE COMMANDS PRODUCE INITIAL FITS!!!"
	echo ""
	cmdInit="combineTool.py -M Impacts -v 3 -d comb_tot_nominalCombination_M${mass}_mc.root  -m ${mass} $blindOrNot --doInitialFit --robustFit 1 ${region} #>& log_initFits_${range}.txt"
	echo $cmdInit; eval $cmdInit
	echo ""
	echo "THESE COMMANDS PRODUCE REAL LONG FITS!!!"
	echo ""
	cmdDoFit="combineTool.py -M Impacts -v 3 -d comb_tot_nominalCombination_M${mass}_mc.root $blindOrNot --robustFit 1 --doFits --parallel 20 ${region} -m ${mass} #>& log_doFits_${range}.txt"
	echo $cmdDoFit; eval $cmdDoFit;
	
	echo ""
	echo "THESE COMMANDS PRODUCE JSON FILE!!!"
	echo ""
	
	cmdImp="combineTool.py -M Impacts -v 3 -d comb_tot_nominalCombination_M${mass}_mc.root -m ${mass} $blindOrNot -o impacts_${range}.json"
	echo $cmdImp; eval $cmdImp;
	
	echo ""
	echo "THESE COMMANDS PLOT IMPACTS"
	echo ""
	
	cmdPlot="plotImpacts.py -i impacts_${range}.json -o impacts_${range}_strategy2"
	echo $cmdPlot; eval $cmdPlot;
    done
done
