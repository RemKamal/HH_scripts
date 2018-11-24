mass=350
blindOrNot="" #" -t -1 "

echo ""
echo "THESE COMMANDS PRODUCE WORKSPACES!!!"
echo ""

text2workspace.py comb_tot_nominalCombination_M${mass}_mc.txt

for range in 100 200 300 500 1000
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

    region+=" --cminDefaultMinimizerStrategy 0  --X-rtd MINIMIZER_analytic "
#--cminDefaultMinimizerTolerance 0.05 "
    echo "FINAL region=${region}"

    echo ""
    echo "THESE COMMANDS PRODUCE INITIAL FITS!!!"
    echo ""
    cmd="combineTool.py -M Impacts -v 3 -d comb_tot_nominalCombination_M${mass}_mc.root  -m ${mass} $blindOrNot --doInitialFit --robustFit 1 ${region} #>& log_initFits_${range}.txt"
    echo $cmd; eval $cmd
    echo ""
    echo "THESE COMMANDS PRODUCE REAL LONG FITS!!!"
    echo ""
    combineTool.py -M Impacts -v 3 -d comb_tot_nominalCombination_M${mass}_mc.root $blindOrNot --robustFit 1 --doFits --parallel 20 ${region} -m ${mass} #>& log_doFits_${range}.txt
    
    echo ""
    echo "THESE COMMANDS PRODUCE JSON FILE!!!"
    echo ""
    
    combineTool.py -M Impacts -v 3 -d comb_tot_nominalCombination_M${mass}_mc.root -m ${mass} $blindOrNot -o impacts_${range}.json
    
    echo ""
    echo "THESE COMMANDS PLOT IMPACTS"
    echo ""

    plotImpacts.py -i impacts_${range}.json -o impacts_${range}
done
