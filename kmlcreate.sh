#!/usr/bin/env bash

home=`pwd`

cd $home/output/

pwd

for quadname in *; do

  cd $home/output/$quadname/

  pwd

  outputfilename=$home/output/$quadname/$quadname".kml"
  echo "Output File Name: "$outputfilename

  rm $outputfilename

  echo "<?xml version="\""1.0"\"" encoding="\""UTF-8"\""?>" >> $outputfilename
  echo "<kml xmlns="\""http://www.opengis.net/kml/2.2"\"" xmlns:gx="\""http://www.google.com/kml/ext/2.2"\"" xmlns:kml="\""http://www.opengis.net/kml/2.2"\"" xmlns:atom="\""http://www.w3.org/2005/Atom"\"">" >> $outputfilename
  echo "<Folder>" >> $outputfilename
  echo "<name>"$quadname"</name>" >> $outputfilename
  echo "<open>0</open>" >> $outputfilename
 
  for contour in */;do

    cd $home/output/$quadname/$contour

    pwd

    echo "<Folder>" >> $outputfilename
    echo "<name>"$contour"</name>" >> $outputfilename
    echo "<open>0</open>" >> $outputfilename

	  for directory in [0-9]*; do

	    for filename in $directory/[0-9]*.jpg; do
	      echo "Filename: "$filename;
	      finalfilename=`echo $filename | cut -d '/' -f 2`
	      echo "Final Filename: "$finalfilename;
	      nlat=`echo $finalfilename | cut -d '_' -f 1`
	      slat=`echo $finalfilename | cut -d '_' -f 2`
	      elong=`echo $filename | cut -d '_' -f 3`
	      wlong=`echo $filename | cut -d '_' -f 4 | cut -d '.' -f 1-2`
	      echo "NLat: "$nlat
	      echo "SLat: "$slat
	      echo "WLong: "$wlong
	      echo "ELong: "$elong
	      echo "<GroundOverlay>" >> $outputfilename
	      echo "<name>"$nlat"N-"$wlong"W</name>" >> $outputfilename
	      echo "<Icon>" >> $outputfilename
	      echo "<href>"$contour"/"$nlat"/"$finalfilename"</href>" >> $outputfilename
	      echo "<viewBoundScale>0.75</viewBoundScale>" >> $outputfilename
	      echo "</Icon>" >> $outputfilename
	      echo "<LatLonBox>" >> $outputfilename
	      echo "<north>"$nlat"</north>" >> $outputfilename
	      echo "<south>"$slat"</south>" >> $outputfilename
	      echo "<east>"$elong"</east>" >> $outputfilename
	      echo "<west>"$wlong"</west>" >> $outputfilename
	      echo "</LatLonBox>" >> $outputfilename
	      echo "</GroundOverlay>" >> $outputfilename
	    done

	  done

    echo "</Folder>" >> $outputfilename
  done

  echo "</Folder>" >> $outputfilename
  echo "</kml>" >> $outputfilename

done
