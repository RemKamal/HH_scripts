dbSamplesList=('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V24_TT_TuneCUETP8M1_13TeV-powheg-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext3-v1/160909_063406/:0000,0001,0002' '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V24_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext1-v1/160909_070517/:0000' 

'/DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V24_DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160909_071126/:0000' 

'/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/VHBB_HEPPY_V24_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v2/160909_063526/:0000' 

'/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/VHBB_HEPPY_V24_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160909_063328/:0000' 

'/ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V24_ggZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__spr16MAv2-puspr16_HLT_80r2as_v14-v1/160909_073854/:0000')

declare -a array=("TT_Tune" "DYJetsToLL_M-50" "DYJetsToLL_M-5to50" "ST_tW_top_5f" "ST_tW_antitop_5f" "ggZH_HToBB_ZToLL_M125")

prefix='/store/user/arizzi/VHBBHeppyV24'

# usage:  sh createListOfBGFiles.sh

i=0
# Loop over DB samples
for someDbSample in ${dbSamplesList[@]}
do
    # delete previous array/list (this is crucial!)
    unset dbNamesList
    # split sub-list if available
    if [[ $someDbSample == *":"* ]]
    then
        # split sample name from sub-list
        tmpSampleArray=(${someDbSample//:/ })
        someDbSample=${tmpSampleArray[0]}
        dbNamesList=${tmpSampleArray[1]}
        # make array from simple string
        dbNamesList=(${dbNamesList//,/ })
    fi

    # Info
    #echo -e "\n----\n$someDbSample\n--"
    
    # Loop over databases
    for someDB in ${dbNamesList[@]}
    do
        
        #echo $prefix$someDbSample$someDB
        #echo $someDbSample and $someDB
        #touch log_$someDB.txt
        #echo $someDB
        #echo "$prefix$someDbSample$someDB" | sed -r 's/[/]+/_/g'
        #echo logName
        xrdfs stormgf1.pi.infn.it ls -u $prefix$someDbSample$someDB > log_${array[$i]}_$someDB.txt
        #temp=$prefix$someDbSample$someDB
        #echo $temp
        #mod=${temp//[\/]/_}
        #echo $mod
        echo 'creating' log_${array[$i]}_$someDB '...'
    
        
        #echo $prefix$someDbSample$someDB
        #echo $i
        #echo ${array[$i]}, "inner"
        #var=$((var + 1))



    done            
    #echo ${array[$i]}, "outer"
    cat log_${array[$i]}_*.txt > comb_listOf_${array[$i]}_trees.txt
    sed -i -e '/log/d' comb_listOf_${array[$i]}_trees.txt
    sed -i -e '/failed/d' comb_listOf_${array[$i]}_trees.txt
    let "i+=1"

done