# tpq2jpg2kml
Converts proprietary .TPQ files from National Geographic Topo & Trails Illustrated to "bit perfect" JPGs and writes the KML file to open them in Google Earth.

Tested on Ubuntu 20.04, for all "Trails Illustrated" sets, and majority of the "U.S. State" sets.

Dependendencies:

python3 & imagemagick  (apt install python3 imagemagick)


Setup:

Open the root directory of any CD-ROM or ISO of Nat-Geo Topo or Trails Illustrated Product, search for and copy all *.tpq or *.TPQ files from the disc into the cloned working directory.  You may need to do this for several discs in a multi-disc set.  If the files are *.tpq, use the rename.sh to change everything to *.TPQ files or change the doit.sh script appropriately.

Remove the small TPQ files for the overview maps (US_*, AK1_*, HI1_*, etc).

Run the code on one set of TPQ's at a time, with respect to the leading letter of the filenames  (all the F files, then all the Q files, etc).  Each set of files is a different map resolution (i.e. F files are the 100K map zoom level, Q files are the 24K map zoom level).


Run:

./doit.sh


The script will run the python program on each TPQ file, extracting the bit perfect JPGs from the TPQ file.  The multiple tiny JPGs in one TPQ file combine to form a maplet when stitched together using imagemagick.  Once all the maplets are created, a KML file is then written to reference all the image files.  Open the KML file in Google Earth to test that it works, in the left pane of GE rename it to whatever you want, and then use the "Save As" function to write it to a KMZ file that contains all the images.  I typically then use "Global Mapper" to convert the KMZ files to MBTILE.  Then I use MOBAC to stitch the various MBTILE files into one MBTILE file with all zoom levels.
