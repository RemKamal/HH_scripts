echo ""
echo ""
echo "THESE COMMANDS PRODUCE MaxLikelihoodFit WITH ASYMOV DATA AND expectSignal 0 !!!"
echo ""
echo ""

range='--rMin -1000 --rMax 1000'
range=''

algo='2' 
algo='0'

makeRed='-a -A'
makeRed=''

combine -M MaxLikelihoodFit -t -1 --expectSignal 0 $range --cminDefaultMinimizerStrategy $algo --X-rtd MINIMIZER_analytic comb_tot_nominalCombination_M300_mc.root 
mv fitDiagnostics.root fitDiagnostics_expectSignal0.root

echo ""
echo ""
echo "THESE COMMANDS PRODUCE HTML FOR diffNuisances AND COPY THAT TO THE WEB DIR CALLED 'april11' !!"
echo ""
echo ""

python diffNuisances_manual.py fitDiagnostics_expectSignal0.root -g plots_expectSignal0.root -f html > Comparison_of_nuisances_expectSignal0.html $makeRed
cp Comparison_of_nuisances*  ~/www/april11

echo ""
echo ""
echo "THESE COMMANDS PRODUCE MaxLikelihoodFit WITH ASYMOV DATA AND expectSignal 1 !!!"
echo ""
echo ""

combine -M MaxLikelihoodFit -t -1 --expectSignal 1 $range --cminDefaultMinimizerStrategy $algo --X-rtd MINIMIZER_analytic comb_tot_nominalCombination_M300_mc.root 
mv fitDiagnostics.root fitDiagnostics_expectSignal1.root

echo ""
echo ""
echo "THESE COMMANDS PRODUCE HTML FOR diffNuisances AND COPY THAT TO THE WEB DIR CALLED 'april11' !!"
echo ""
echo ""

python diffNuisances_manual.py fitDiagnostics_expectSignal1.root -g plots_expectSignal1.root -f html > Comparison_of_nuisances_expectSignal1.html $makeRed
cp Comparison_of_nuisances*  ~/www/april11

