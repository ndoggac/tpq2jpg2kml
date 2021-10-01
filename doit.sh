#!/usr/bin/env bash

home=`pwd`
echo "Home= "$home
cd $home
mkdir -p output

echo " ";echo "----------------";echo " ";
echo "Entering Python Loop"
echo " ";echo "----------------";echo " ";
sleep 2

#for filename in [a-z]*.tpq; do 
#for filename in n40103h2.tpq; do
#for filename in AZ*.TPQ; do 
for filename in *.TPQ; do 
#for filename in *.tpq; do 
#for filename in [f-q]*.tpq; do 
  echo $filename;
  timeout 9 python3 tpq2jpg.py $filename;
  sleep 0.1
done

cd $home/output

echo " ";echo "----------------";echo " ";
echo "Entering Image Magick Loop"
echo " ";echo "----------------";echo " ";
sleep 2

counter=0

for quadname in *; do

  cd $home/output/$quadname/

  for contour in *; do

    cd $home/output/$quadname/$contour/

	  for directory in *; do 
	    echo $directory;
	    cd $home/output/$quadname/$contour/$directory;

	    for filename in *.jpg; do 
	      finalfilename="$filename";
	      #echo $finalfilename;
	    done

	    for rowdir in r*; do
	      cd $home/output/$quadname/$contour/$directory/$rowdir
              rm -f $rowdir.jpg
	      convert *.jpg +append -colorspace RGB $rowdir.jpg
	      counter=counter+1
	    done


	    for job in `jobs -p`; do
	      #echo $job
	      wait $job || let "FAIL+=1"
	    done
    
	   
	    cd $home/output/$quadname/$contour/$directory;
            rm -f final.jpg
	    convert row*/r*.jpg -colorspace RGB -append final.jpg &

	    for job in `jobs -p`; do
	      #echo $job
	      wait $job || let "FAIL+=1"
	    done

	    mv final.jpg $finalfilename

	  done

	done
wait

done


echo " ";echo "----------------";echo " ";
echo "Collecting All JPEGs and Sorting into directory by N. Latitude"
echo " ";echo "----------------";echo " ";
sleep 2

cd $home/output/

for quadname2 in *; do

  cd $home/output/$quadname2/

  for contour2 in *; do
	  cd $home/output/$quadname2/$contour2/
	  mkdir -p jpgs
	  mv --backup=numbered */*.jpg jpgs
	  #mv --backup=numbered */*.png jpgs
	  rm -r $(ls -I "jpgs" )
	  mv jpgs/* .
	  rm -r jpgs

	  for filename in [0-9]*.jpg; do
	    #echo "Filename: "$filename;
	    finalfilename="$filename";
	    latitude=`echo $filename | cut -d '_' -f 1`
	    echo "Latitude: "$latitude
	    mkdir -p $latitude
	    mv --backup=numbered $latitude*.jpg $latitude
	    #mv --backup=numbered $latitude*.png $latitude
	  done

  done
done


echo " ";echo "----------------";echo " ";
echo "Creating KML File"
echo " ";echo "----------------";echo " ";
sleep 2

cd $home
./kmlcreate.sh

#echo " ";echo "----------------";echo " ";
#echo "Creating PNG KML File"
#echo " ";echo "----------------";echo " ";
#sleep 2
#./kmlcreate_png.sh

echo " ";echo "Done, Exiting!";echo " ";

exit

