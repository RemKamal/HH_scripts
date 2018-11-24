mass=900

for M in $mass 
do
#110 120 125 130 140; do
    echo "Starting from mass = " $M
    #combine -M ProfileLikelihood --significance --pvalue -d comb_tot_nominalCombination_M${M}_mc.root -t -1 --toysFrequentist --expectSignal=1 -m $M -n _Exp -v 3
    cmdToys="combine -M ProfileLikelihood --significance -d comb_tot_nominalCombination_M${M}_mc.root -t -1 --toysFrequentist --expectSignal=1 -m $M -n _Exp -v 3 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 2 --cminDefaultMinimizerTolerance 0.01"

    echo $cmdToys; eval $cmdToys

    #combine -M ProfileLikelihood --significance --pvalue -d comb_tot_nominalCombination_M${M}_mc.root  -m $M -n _Obs -v 3
    cmdData="combine -M ProfileLikelihood --significance -d comb_tot_nominalCombination_M${M}_mc.root  -m $M -n _Obs -v 3 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 2 --cminDefaultMinimizerTolerance 0.01"
    echo $cmdData; eval $cmdData
done
hadd -f Tot_pvalue_Exp.root higgsCombine_Exp.ProfileLikelihood.mH*.root
hadd -f Tot_pvalue_Obs.root higgsCombine_Obs.ProfileLikelihood.mH*.root
python makeSignificancePlots.py -d Significance.dat



#Pre-fit expected[*]: combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there -t -1 --expectSignal 1
#Post-fit expected: combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there -t -1 --expectSignal 1 --toysFrequentist
#Observed : combineTool.py -M Significance --significance -d output/<output_folder>/cmb/ws.root --there


#combine -M Significance --signif -m 125 htt_tt.txt -t -1 --expectSignal=1 --toysFreq
#combine -M Significance --signif -m 125 htt_tt.txt

#Significance: combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --toysFreq     --expectSignal=1 card