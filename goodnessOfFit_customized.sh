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



mass=900
nToys=3
nParallJobs=10

for signalStrength in " --fixedSignalStrength=1 " " --fixedSignalStrength=0 " ""
do

    strength=""
    if [[ $signalStrength = *"1"* ]]; then
        strength="1"
        echo "strength=${strength}"

    elif [[ $signalStrength = *"0"* ]]; then
        strength="0"
        echo "strength=${strength}"
    elif [[ $signalStrength = *""* ]]; then
        strength=""
        echo "strength=${strength}"
    else
        echo "CANNOT HAPPEN, exiting"
        exit 1
    fi


    for ALGO in "AD" "KS" "saturated"
    do
	combineTool.py -M GoodnessOfFit --algorithm $ALGO -m ${mass} --there -d comb_tot_nominalCombination_M${mass}_mc.root -n ".$ALGO.toys" ${signalStrength} -t ${nToys} -s 0:19:1 --parallel ${nParallJobs}
	combineTool.py -M GoodnessOfFit --algorithm $ALGO -m ${mass} --there -d comb_tot_nominalCombination_M${mass}_mc.root -n ".$ALGO" ${signalStrength}
	combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH${mass}.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH${mass}.*.root -o collectGoodness_${ALGO}_${strength}.json
	python /afs/cern.ch/work/r/rkamalie/private/CMSSW_8_1_0/src/CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass ${mass}.0 collectGoodness_${ALGO}_${strength}.json --title-right="35.9 fb^{-1} (13 TeV)" --output="-${ALGO}_${strength}"
    done
done

