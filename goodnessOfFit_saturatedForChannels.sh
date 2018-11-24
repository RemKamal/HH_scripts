# Base off ./HIG16006/input/mssm_protocol.txt



# We look at the Goodness of Fit for three different algorithms. 
# The saturated model (saturated), Anderson-Darling (AD) and 
# Kolmogorow-Smirnow (KS). For the AD and KS it is sufficient to 
# run the fits for the combined cards as the test-statitic for 
# the individual channels can be extracted from these results. 
# For the saturated model it is necessary to run them independtly 
# of each other.


###  THESE COMMANDS PRODUCE UNBLINDED RESULTS!!!  ###
echo ""
echo ""
echo "THESE COMMANDS PRODUCE UNBLINDED RESULTS!!!"
echo ""
echo ""




# # Do Anderson Darling first
# ALGO=AD
# combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 300 --there -d comb_tot_nominalCombination_M300_mc.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
# combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 300 --there -d comb_tot_nominalCombination_M300_mc.root -n ".$ALGO" --fixedSignalStrength=1

# combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH300.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH300.*.root -o collectGoodness_${ALGO}.json

# python /afs/cern.ch/work/r/rkamalie/private/CMSSW_8_1_0/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 300.0 collectGoodness_${ALGO}.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-AD'





# # Do KS test
# ALGO=KS
# combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 300 --there -d comb_tot_nominalCombination_M300_mc.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
# combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 300 --there -d comb_tot_nominalCombination_M300_mc.root -n ".$ALGO" --fixedSignalStrength=1

# combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH300.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH300.*.root -o collectGoodness_${ALGO}.json

# python /afs/cern.ch/work/r/rkamalie/private/CMSSW_8_1_0/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 300.0 collectGoodness_${ALGO}.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-KS'






# Do Saturated test
#ALGO=saturated

do_t2w=true


echo "before the loop over cards"
for card in "copy_dataCard_CRDY_hhMt.txt" "copy_dataCard_CRTT_hhMt.txt" "copy_dataCard_SR_hhMt.txt"
do
    

    if [ $do_t2w ]; then
	echo "This is done only once per card with the 1st algo, the other algos use the same ws!"
	echo "doing text2workspace.py"
	text2workspace.py $card
	card=${card/txt/root}
	echo "card ${card} is ready"
    fi

    echo "before the loop over algos"
    for ALGO in "KS" "AD" "saturated"
    do
    
	region=""
	if [[ $card = *"SR"* ]]; then
	    region="SR"
	    echo "region=${region}"
	    
	elif [[ $card = *"CRDY"* ]]; then
            region="CRDY"
	    echo "region=${region}"
	elif [[ $card = *"CRTT"* ]]; then
            region="CRTT"
	    echo "region=${region}"
	else
	    echo "CANNOT HAPPEN, exiting"
	    exit 1
	fi

    
	cmdToys="combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 300 --there -d $card -n \'.$ALGO.toys\' --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12"
	echo $cmdToys; eval $cmdToys;

	cmdData="combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 300 --there -d $card -n \'.$ALGO\' --fixedSignalStrength=1"
	echo $cmdData; eval $cmdData;
	
	cmdCollect="combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH300.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH300.*.root -o collectGoodness_${ALGO}_${region}.json"
	echo $cmdCollect; eval $cmdCollect;
	
	cmdPlot="python /afs/cern.ch/work/r/rkamalie/private/CMSSW_8_1_0/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 300.0 collectGoodness_${ALGO}_${region}.json --title-right='35.9 fb^{-1} (13 TeV)' --output='${ALGO}_${region}'"
	echo $cmdPlot; eval $cmdPlot;


    done
    do_t2w=false

done

