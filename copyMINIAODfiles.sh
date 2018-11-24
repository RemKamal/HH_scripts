#source /afs/cern.ch/cms/cmsset_default.sh
#source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.sh
#cmsrel CMSSW_6_0_0
#cd CMSSW_6_0_0


#cmsenv
#dovoms2
#cpproxy

#!/usr/bin/bash
filename="$1"
while read -r line
do
    name="$line"
    name="xrdcp root://cms-xrd-global.cern.ch/"$name" ."
    echo "Name read from file: $name"
    eval $name
done < "$filename"

#xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/GluGluToBulkGravitonToHHTo2B2ZTo2L2Nu_M-900_narrow_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/C69265B1-515F-E711-A623-008CFAF2018E.root /some/local/path
