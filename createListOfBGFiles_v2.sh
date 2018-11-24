dbSamplesList=()
readarray -t dbSamplesList < logOfSamplesUnique.txt

#find . -type f \( -name "*Bulk*" -o -name "*GluHTo*" -o -name "*VBFHToBB*" -o -name "*bbHToBB*" -o -name "*ZHiggs0**" -o -name "*ToQQ*" \)  -print0 \| xargs -0 rm -f --

: <<'COMMENT'
dbSamplesList=(
"/store/group/phys_higgs/hbb/ntuples/V25/DYToLL_1J_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25/170206_153522/:0000,0001"
...
COMMENT


#)

declare -a array=()
readarray -t array < logOfSamplesNames.txt  # -t is extremely important as it removes damn trailing space
: <<'COMMENT'
"ggZH_HToBB_ZToLL_M125"
...
)
COMMENT



prefix='/store/user/arizzi/VHBBHeppyV24'

# usage:  sh createListOfBGFiles.sh
xrdLinePisa='xrdfs stormgf1.pi.infn.it ls -u '
xrdLineCern='xrdfs 188.184.38.46 ls -u '
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

    # Loop over databases
    for someDB in ${dbNamesList[@]}
    do
        
        #echo $prefix
	#echo $someDbSample
	#echo $someDB
        #echo "                "

	if [[ $someDbSample =~ .*user.* ]]
	then
	    echo "process Pisa sample"
	    xrdLine=$xrdLinePisa
	else
	    echo "process CERN sample"
	    xrdLine=$xrdLineCern
	fi
	echo $xrdLine
	echo 'someDB is '; echo $someDB
	echo 'array element is'; echo ${array[$i]}
	echo '"i" is'; echo $i
	echo $'\n'
	echo 'command line: '; echo $xrdLine$someDbSample$someDB 
	echo 'creating' log_${array[$i]}_$someDB.txt '...'
	$xrdLine$someDbSample$someDB > log_${array[$i]}_$someDB.txt

    done            

    cat log_${array[$i]}_*.txt > comb_listOf_${array[$i]}_trees.txt
    sed -i -e '/log/d' comb_listOf_${array[$i]}_trees.txt
    sed -i -e '/failed/d' comb_listOf_${array[$i]}_trees.txt
    let "i+=1"

done
printf "Overall processed %d samples." $i


# now remove logs if they contain 'failed' from the crab3 output
goodFile=0
declare -a samplesRemaining=()
ls comb_listOf_*.txt > samplesRemaining.txt

# remove several samples
#sed -i '/Bulk/d;/GluHTo/d;/VBFHToBB/d;/ZHiggs0/d;/bbHToBB/d;/ToQQ/d' samplesRemaining.txt

readarray -t samplesRemaining  < samplesRemaining.txt  # -t is extremely important as it removes damn trailing space


aLen=${#samplesRemaining[@]} # use for loop to read all samples
echo ' Number of samples is ' ; echo $aLen

for (( i=0; i<${aLen}; i++ ))
do
    
    echo $'\n'; echo 'Start checking sample: ';echo ${samplesRemaining[$i]}
    
    

    _file=${samplesRemaining[$i]}
    #[ $# -eq 0 ] && { echo "Checking file " "$_file" ; exit 1; }
    [ ! -f "$_file" ] && { echo "Error: $0 file not found."; exit 2; }
    
    if [ -s "$_file" ] 
    then
	let "goodFile+=1"
	echo "$_file has some data, 'comb' file is kept!!" 
	
    else
	echo "$_file is empty, removing combined file."
	rm "$_file"
	unset samplesRemaining[$i]
    fi
    
    
done

printf "%s\n" "${samplesRemaining[@]}" > samplesFinal.txt

#printf '%s\n' "${ar[@]}"

echo "Remove all intermediate logs...."
rm log_*_000*.txt 
printf "Overall %d samples." $goodFile