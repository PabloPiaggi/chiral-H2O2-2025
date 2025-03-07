for press in 0 1000 5000 6000
do
	for index in $(seq 41 60) 
	do
		echo $press $index
		folder="${press}atm_${index}"
		cp -r BASE $folder
	        cd $folder
		sed -i "s/PRESSURE/$press/g" start.lmp 
		sed -i "s/RANDOM/$RANDOM/g" start.lmp 
		sed -i "s/PRESSURE/$press/g" job.sh
		sed -i "s/INDEX/$index/g" job.sh
		sbatch < job.sh
		cd ..	
	done
done
