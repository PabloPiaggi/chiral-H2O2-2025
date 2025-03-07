for press in 7000
do
	echo $press 
	folder="${press}atm"
	cp -r BASE $folder
	cd $folder
	sed -i "s/PRESSURE/$press/g" start.lmp 
	sed -i "s/RANDOM/$RANDOM/g" start.lmp 
	sed -i "s/PRESSURE/$press/g" job.sh
	sbatch < job.sh
	cd ..	
done

