# tpq2jpg2kml
Converts proprietary .TPQ files from National Geographic Topo & Trails Illustrated to "bit perfect" JPGs and writes the KML file to open them in Google Earth.

Tested on Ubuntu 20.04, for all "Trails Illustrated" sets, and majority of the "U.S. State" sets.

Dependendencies:

python3 & imagemagick  (apt install python3 imagemagick)


Setup:

Open the root directory of any CD-ROM or ISO of Nat-Geo Topo or Trails Illustrated Product, search for and copy all *.tpq or *.TPQ files from the disc into the cloned working directory.  You may need to do this for up to 10 or more discs in a multi-disc set for an entire U.S. State.  If the files are *.tpq, use the rename.sh to change everything to *.TPQ files or change the doit.sh script appropriately.

Remove the small TPQ files for the overview maps (US, AK1, HI1, etc).  The first time you process a data set, you can also run the code on these files, but I believe they are the same overview maps on every data set.  One data set had the entire USA down to roughly a zoom level of 12 (1:100K scale), if I remember correctly it was the "National Parks" set.

Run the code on one set of TPQ's at a time, with respect to the leading letter of the filenames.  (i.e. all the F files, then all the Q files, etc -- typical letters are A, F, K, Q).  Each set of files is a different map resolution (i.e. A files are the 250K map zoom level, F files are the 100k, K files are 64k, Q files are 24K).  The higher the resolution of the data, the more files, Q at 24k being the most.  After each run, clean out the "output" directory.


Run:

./doit.sh


The script will run the python program on each TPQ file, extracting the bit perfect JPGs from the TPQ file.  The multiple tiny JPGs in one TPQ file combine to form a maplet when stitched together using imagemagick.  Once all the maplets are created, a KML file is then written to reference all the image files.  Open the KML file in Google Earth to test that it works, in the left pane of GE rename the sub-folder to whatever you want, then right click and then use the "Save As" function to write it to a KMZ file that contains all the images.  I typically then use "Global Mapper" to convert the KMZ files to MBTILE.  Then I use MOBAC to stitch the various MBTILE files into one MBTILE file with all zoom levels.
