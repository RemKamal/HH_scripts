combineTool.py -M T2W -i mar27_for81X_rmBBB/eeem/125/htt_eeem_1_13TeV.txt -o workspace_eeem.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/eeet/125/htt_eeet_1_13TeV.txt -o workspace_eeet.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/eemt/125/htt_eemt_1_13TeV.txt -o workspace_eemt.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/eett/125/htt_eett_1_13TeV.txt -o workspace_eett.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/emmm/125/htt_emmm_1_13TeV.txt -o workspace_emmm.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/emmt/125/htt_emmt_1_13TeV.txt -o workspace_emmt.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/mmmt/125/htt_mmmt_1_13TeV.txt -o workspace_mmmt.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/mmtt/125/htt_mmtt_1_13TeV.txt -o workspace_mmtt.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/mmt/125/htt_mmt_1_13TeV.txt -o workspace_mmt.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/emt/125/htt_emt_1_13TeV.txt -o workspace_emt.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/ett/125/htt_ett_1_13TeV.txt -o workspace_ett.root --parallel 18 -m 125
combineTool.py -M T2W -i mar27_for81X_rmBBB/mtt/125/htt_mtt_1_13TeV.txt -o workspace_mtt.root --parallel 18 -m 125
cp mar27_for81X_rmBBB/eeem/125/workspace_eeem.root .
cp mar27_for81X_rmBBB/eeet/125/workspace_eeet.root .
cp mar27_for81X_rmBBB/eemt/125/workspace_eemt.root .
cp mar27_for81X_rmBBB/eett/125/workspace_eett.root .
cp mar27_for81X_rmBBB/emmm/125/workspace_emmm.root .
cp mar27_for81X_rmBBB/emmt/125/workspace_emmt.root .
cp mar27_for81X_rmBBB/mmmt/125/workspace_mmmt.root .
cp mar27_for81X_rmBBB/mmtt/125/workspace_mmtt.root .
cp mar27_for81X_rmBBB/mmt/125/workspace_mmt.root .
cp mar27_for81X_rmBBB/emt/125/workspace_emt.root .
cp mar27_for81X_rmBBB/ett/125/workspace_ett.root .
cp mar27_for81X_rmBBB/mtt/125/workspace_mtt.root .

###  THESE COMMANDS PRODUCE UNBLINDED RESULTS!!!  ###
echo ""
echo ""
echo "THESE COMMANDS PRODUCE UNBLINDED RESULTS!!!"
echo ""
echo ""


### Do Anderson Darling first
ALGO=AD
#for CHANNEL in eeem eeet eemt eett emmm emmt mmmt mmtt emt mmt ett mtt; do
for CHANNEL in emt mmt ett mtt; do
   combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d workspace_${CHANNEL}.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
   combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d workspace_${CHANNEL}.root -n ".$ALGO" --fixedSignalStrength=1
   combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH125.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH125.*.root -o collectGoodness_${ALGO}.json
   python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 collectGoodness_${ALGO}.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-AD'
done
###
###
###
###
###
#### Do KS test
ALGO=KS
#for CHANNEL in eeem eeet eemt eett emmm emmt mmmt mmtt ett emt mmt mtt; do
for CHANNEL in ett emt mmt mtt; do
   combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d workspace_${CHANNEL}.root -n ".$ALGO.toys" --fixedSignalStrength=1 -t 25 -s 0:19:1 --parallel 12
   combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d workspace_${CHANNEL}.root -n ".$ALGO" --fixedSignalStrength=1
   combineTool.py -M CollectGoodnessOfFit --input higgsCombine.${ALGO}.GoodnessOfFit.mH125.root higgsCombine.${ALGO}.toys.GoodnessOfFit.mH125.*.root -o collectGoodness_${ALGO}.json
   python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 collectGoodness_${ALGO}.json --title-right="35.9 fb^{-1} (13 TeV)" --output='-KS'
done
#
### Do Saturated
### For the saturated model run for each category seperatly
### We need to make indivual workspace_mtts for each channel/bin
ALGO=saturated

#for CHANNEL in eeem eeet eemt eett emmm emmt mmmt mmtt emt mmt ett mtt; do
for CHANNEL in emt mmt ett mtt; do
    for BIN in 1 ; do
        echo "Saturated for ${CHANNEL} ${BIN}"
        combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d workspace_${CHANNEL}.root -n ".$ALGO.toys"  -t 25 -s 0:19:1 --parallel 12 
        combineTool.py -M GoodnessOfFit --algorithm $ALGO -m 125 --there -d workspace_${CHANNEL}.root -n ".$ALGO" 
        combineTool.py -M CollectGoodnessOfFit --input higgsCombine.saturated.GoodnessOfFit.mH125.root higgsCombine.saturated.toys.GoodnessOfFit.mH125.*.root -o vh_${CHANNEL}_saturated.json
    done
done
##
##
### Do saturated plotting separately to properly label
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_eeem_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='eeem_1-Saturated' --title-left="eee#mu"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_eeet_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='eeet_1-Saturated' --title-left="eee#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_eemt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='eemt_1-Saturated' --title-left="ee#mu#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_eett_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='eett_1-Saturated' --title-left="ee#tau#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_emmm_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='emmm_1-Saturated' --title-left="e#mu#mu#mu"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_emmt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='emmt_1-Saturated' --title-left="e#mu#mu#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_mmmt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mmmt_1-Saturated' --title-left="#mu#mu#mu#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_mmtt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mmtt_1-Saturated' --title-left="#mu#mu#tau#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_mmt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mmt_1-Saturated' --title-left="#mu#mu#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_emt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='emt_1-Saturated' --title-left="e#mu#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_ett_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='ett_1-Saturated' --title-left="e#tau#tau"
python ../CombineHarvester/CombineTools/scripts/plotGof.py --statistic ${ALGO} --mass 125.0 vh_mtt_saturated.json --title-right="35.9 fb^{-1} (13 TeV)" --output='mtt_1-Saturated' --title-left="#mu#tau#tau"
#
