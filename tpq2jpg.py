import os
import sys
import struct
import binascii
import math
import argparse
import time
import datetime
import re


# Get the total number of args passed
total = len(sys.argv)

if total != 2:
   print("")
   print("Converts Nat GEO TPQ files to JPG's")
   print("")
   print("Usage: python3 tpq2jpg.py <inputFileName.TPQ>")
   print("")
   sys.exit()
 
# Get the arguments list 
cmdargs = str(sys.argv)
filename=str(sys.argv[1])
outputname=os.path.splitext(filename)[0]
firstletter=outputname[0]
#print("Filename : ", filename)
#print("FirstLetter : ", firstletter)
#print("Output:   ", outputname)
#print("Output2:  ", outputname2)


JPEG_BIN_START = binascii.unhexlify("ffd8")
PNG_BIN_START = binascii.unhexlify("89504E470D0A1A0A")
PNG_BIN_END = binascii.unhexlify("49454e44")

if firstletter!='Q' and firstletter!='q':
  #print("Found non-Q file")
  #JPEG_BIN_END = binascii.unhexlify("ffd9ffd8")
  JPEG_BIN_END_ALT = binascii.unhexlify("ffd9")
  JPEG_BIN_END = binascii.unhexlify("ffd9")
else:
  #print("Found Q file")
  JPEG_BIN_END = binascii.unhexlify("ffd9")
  #JPEG_BIN_END = binascii.unhexlify("ffd9ffd8")
  JPEG_BIN_END_ALT = binascii.unhexlify("ffd9")


TPQ_HEADER_SIZE=1024

f = open(filename, 'rb')
size=os.stat(filename).st_size

try:
# Read Header        

    version=int.from_bytes(f.read(4), byteorder='little')
    west_long=struct.unpack('d', f.read(8))[0]
    north_lat=struct.unpack('d', f.read(8))[0]
    east_long=struct.unpack('d', f.read(8))[0]
    south_lat=struct.unpack('d', f.read(8))[0]
    topo_name=f.read(12).decode('utf-8')
    topo_name=topo_name.rstrip(' \t\r\n\0')
    pad1=f.read(208)
    #quad_name=f.read(128).decode('utf-8')
    #quad_name=f.read(128).decode('unicode_escape').encode('utf-8')
    quad_name=f.read(128)
    #print("Quad Name: ", quad_name)
    #quad_name=quad_name.replace(" ", "")
    #quad_name=quad_name.replace(",", "")
    #quad_name=quad_name.rstrip(' \t\r\n\0')
    #print("Quad Name: ", quad_name)

    ##Manual Override of Quad Name
    ##Comment All for National Park T-Z.tpq
    #quad_name="AdirondackPark"
    #quad_name="SouthernApalachianMountains"
    #quad_name="NationalParksOverview"
    quad_name="Images"

    #state=f.read(32).decode('utf-8')
    state=f.read(32)
    state="MY"
    #state=state.rstrip(' \t\r\n\0')
    #state=state.replace("^@", "")
    #source=f.read(32).decode('utf-8')
    #source=source.rstrip(' \t\r\n\0')
    source=f.read(32)
    source="Huh"
    year1=f.read(4).decode('utf-8')
    year2=f.read(4).decode('utf-8')
    contour=f.read(8)
    #contour=f.read(8).decode('utf-8')
    #contour=contour.rstrip(' \t\r\n\0')
    #contour=(contour.split(" ",1)[0])
    contour=firstletter
    #int_contour=int(contour)
    #if int_contour < 10:
    #   contour="0"+contour
    
    pad2=f.read(16)

    #32-byte combo
    extension=f.read(4).decode('utf-8')
    xxx=f.read(8)
    nlong=int.from_bytes(f.read(4), byteorder='little')
    nlat=int.from_bytes(f.read(4), byteorder='little')
    xx=f.read(12)

    info=f.read(88)
    png1=f.read(32)
    pad3=f.read(28)
    png2=f.read(32)
    pad4=f.read(332)

    ### HAVE READ 1024 BYTE HEADER AT THIS POINT ###

    #dummy=f.read(70)
    
    #data=f.read()

    #International Dateline Fix for Alaska
    if west_long < -180.0:
      west_long=west_long+360

    if east_long < -180.0:
      east_long=east_long+360
    

    #offset=int.from_bytes(f.read(4), byteorder='little')
    #print("offset   : ", offset)
    #f.seek(-4, 1)
    #num_index=int((offset-TPQ_HEADER_SIZE)/4)

    #print("Size  : ", size)
    #print("Version  : ", version)
    #print("West Long: ", west_long)
    #print("North Lat: ", north_lat)
    #print("East Long: ", east_long)
    #print("South Lat: ", south_lat)
    #print("Topo Name: ", topo_name)
    #print("Quad Name: ", quad_name)
    #print("State    : ", state)
    #print("Source   : ", source)
    #print("Year1    : ", year1)
    #print("Year2    : ", year2)
    #print("Contour  : ", contour)
    #print("Extension: ", extension)
    #print("nLong    : ", nlong)
    #print("nLat     : ", nlat)
    #print("png1     : ", png1)
    #print("png2     : ", png2)
    #print("JPEG_BIN_START: ", JPEG_BIN_START)
    #print("JPEG_BIN_END: ", JPEG_BIN_END)
    #print("offset   : ", offset)
    #print("num_index: ", num_index)

    #print("North Lat,South Lat,East Long,West Long")
    #print(north_lat,",",south_lat,",",east_long,",",west_long)

    path="output/"+quad_name+"/"+contour+"/"+outputname+"/"
    #print("path: ", path)
    try:  
       os.makedirs(path)
    except OSError:  
       print ("Creation of the directory %s failed" % path)


    outputname2= path + ((str)(north_lat)) + "_" + ((str)(south_lat)) + "_" + ((str)(east_long)) + "_" + ((str)(west_long)) + ".jpg"
    i = open(outputname2, 'w')

    #outputnamepng1= path + ((str)(north_lat)) + "_" + ((str)(south_lat)) + "_" + ((str)(east_long)) + "_" + ((str)(west_long)) + "_1.png"
    #outputnamepng2= path + ((str)(north_lat)) + "_" + ((str)(south_lat)) + "_" + ((str)(east_long)) + "_" + ((str)(west_long)) + "_2.png"
    #i = open(outputnamepng1, 'w')
    #i = open(outputnamepng2, 'w')

    mybyte=1024
    counter=0
    bytesparsed=0
    myrange=nlong*nlat
    #print("myRange     : ", myrange)
   
    for i in range(nlat):
       if i < 10:
          mypath=path+"row0"+((str)(i))+"/"
       else:
          mypath=path+"row"+((str)(i))+"/"
       try:
          os.makedirs(mypath)
       except OSError:
          print ("Creation of the row directory %s failed" % path)

       #print("mypath: ", mypath)

       for j in range(nlong):
          #print("Image #: ", counter)
          f.seek(0)
          f.seek(mybyte)
          data=f.read()
          #print("Data:\n\n")
          #print(binascii.hexlify(data))
          start=(data.find(JPEG_BIN_START))
          if counter==myrange-1:
             JPEG_BIN_END=JPEG_BIN_END_ALT
          end=(data.find(JPEG_BIN_END))
          imgsize=end-start+2
          bytesparsed=bytesparsed+imgsize
          size=size-imgsize
          #print("Start: ", start)
          #print("End: ", end)
          #print("imgsize: ", imgsize)
          #print("bytesparsed: ", bytesparsed)
          #print("bytesleft: ", size)
          #print("byte: ", mybyte)
          newbyte=mybyte+start
          #print("newbyte: ", newbyte)
          f.seek(0)
          f.seek((newbyte))
          myjpeg=f.read(imgsize) 
          #print("MyJpeg:\n\n")
          #print(binascii.hexlify(myjpeg))
          mybyte=mybyte+start+imgsize
          if counter < 10:
             outputname=mypath + "000" + str(counter) + ".jpg"
          elif counter < 100:
             outputname=mypath + "00" + str(counter) + ".jpg"
          elif counter < 1000:
             outputname=mypath + "0" + str(counter) + ".jpg"
          else:
             outputname=mypath + str(counter) + ".jpg"
          fwr = open(outputname, 'wb')
          fwr.write(myjpeg)
          counter=counter+1
          fwr.close()
          #print("\n")

    #print(" ")
    #print(" ")

    #fwrpng1 = open(outputnamepng1, 'wb') 
    #fwrpng2 = open(outputnamepng2, 'wb') 
    #mychunktype=""
    #mypng1=bytearray()
    #mypng2=bytearray()

    #start=(data.find(PNG_BIN_START))
    #mypng1=f.read(8)

    #while mychunktype != "IEND":
    #   length=f.read(4)
    #   mylength=int.from_bytes(length, byteorder='big', signed=False) 
    #   #print("mylength: ", mylength)
    #   chunktype=f.read(4)
    #   mychunktype=chunktype.decode('utf-8')
    #   #print("mychunktype: ", mychunktype)
    #   chunkdata=f.read(mylength)
    #   crc=f.read(4)
    #   mypng1=mypng1+length+chunktype+chunkdata+crc


    #print("Done with 1st while loop!")

    #mychunktype=""
    #start=(data.find(PNG_BIN_START))
    #mypng2=f.read(8)

    #while mychunktype != "IEND":
    #   length=f.read(4)
    #   mylength=int.from_bytes(length, byteorder='big', signed=False)
    #   #print("mylength: ", mylength)
    #   chunktype=f.read(4)
    #   mychunktype=chunktype.decode('utf-8')
    #   #print("mychunktype: ", mychunktype)
    #   chunkdata=f.read(mylength)
    #   crc=f.read(4)
    #   mypng2=mypng2+length+chunktype+chunkdata+crc


    #print("Done with 2nd while loop!")


    #print("mypng1: ", mypng1)
    #print("mypng2: ", mypng2)
    
    #fwrpng1.write(mypng1)
    #fwrpng2.write(mypng2)
 
    #fwrpng1.close()
    #fwrpng2.close()


finally:
    f.close()
    #fwr.close()
