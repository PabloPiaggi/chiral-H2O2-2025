for temp in 300
do
for press in 1,10000
	
	
	do
		echo $temp $press
		folder="${temp}K_${press}atm"
		cp -r BASE $folder
	        cd $folder
		sed -i "s/TEMPERATURE/$temp/g" start.lmp 
		sed -i "s/TEMPERATURE/$temp/g" job.sh
		sed -i "s/PRESSURE/$press/g" start.lmp 
		sed -i "s/PRESSURE/$press/g" job.sh
		sbatch < job.sh
		cd ..	
	done
done
