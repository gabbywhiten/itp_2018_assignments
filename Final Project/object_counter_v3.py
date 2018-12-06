#Import all necessary packages
from ij import IJ
from ij import ImagePlus
from ij import Executer
from ij import WindowManager
from ij.io import FileSaver
from ij.io import Opener
from ij.io import OpenDialog
from ij.io import DirectoryChooser
from ij.plugin import ChannelSplitter
from ij.plugin import TextWriter
from ij.plugin import Selection
from ij.measure import ResultsTable
import os
import _3D_objects_counter
import csv

#define function for choosing Directory
def choose_folder():
    dc = DirectoryChooser("Choose a folder.")
    folder = dc.getDirectory()

    if folder is None:
        print ("User canceled the dialog.")
    else:
        print("Selected folder:", folder)
        return folder
		
#define function that will split channels
def split_channels_red(imp):
	#Create red channel
	original_red = ChannelSplitter.getChannel(imp, 1)
	original_red_IP = ImagePlus(filename, original_red)
	fs = FileSaver(original_red_IP)
	folder = "/Users/gceleste/Desktop/test/channels"
	filepath = folder + "/" + "{}_redchannel.tif".format(filename)
	fs.saveAsTiff(filepath)
	#Open red channel image.
	red = IJ.open(filepath)
	#red_IP = ImagePlus(filename, red)
	IJ.run("3D Objects Counter", "threshold=130 slice=1 min.=50 max.=1447680 exclude_objects_on_edges objects summary")
	#Save red object map.
	red_map = IJ.getImage()
	fs = FileSaver(red_map)
	folder = "/Users/gceleste/Desktop/test/object maps"
	filepath = folder + "/" + "{}_objectmap(red).jpg".format(filename)
	fs.saveAsJpeg(filepath)
	#Close red channel images.
	red_map.close()
	red = IJ.getImage()
	red.close()
	
def split_channels_blue(imp):
	#Create blue channel
	original_blue = ChannelSplitter.getChannel(imp, 3)
	original_blue_IP = ImagePlus(filename, original_blue)
	fs = FileSaver(original_blue_IP)
	folder = "/Users/gceleste/Desktop/test/channels"
	filepath = folder + "/" + "{}_bluechannel.tif".format(filename)
	fs.saveAsTiff(filepath)
	#Open blue channel image.
	blue = IJ.open(filepath)
	#blue_IP = ImagePlus(filename, blue)
	IJ.run("3D Objects Counter", "threshold=100 slice=1 min.=50 max.=1447680 exclude_objects_on_edges objects summary")
	#Save blue object map
	blue_map = IJ.getImage()
	fs = FileSaver(blue_map)
	folder = "/Users/gceleste/Desktop/test/object maps"
	filepath = folder + "/" + "{}_objectmap(blue).jpg".format(filename)
	fs.saveAsJpeg(filepath)
	#Close blue channel image.
	blue_map.close()
	blue = IJ.getImage()
	blue.close()

def get_log_results(filepath):
	#Get log information.
	log_results = IJ.getLog()
	log_table = str(log_results).split("\n")
	log_final = log_ls + log_table

	with open(filepath, 'w') as f:
		for item in log_final:
			f.write("%s\n" % item)
		
#Code for processing program
folder = choose_folder()
                               
for filename in os.listdir(folder):
    if filename.endswith(".tif"):
        imp = IJ.openImage(os.path.join(folder, filename))
        if imp is None:
            print ("Image plus could not be generated from file:", filename)
            continue
        split_channels_red(imp)
        
        
for filename in os.listdir(folder):   
    if filename.endswith(".tif"):
       imp = IJ.openImage(os.path.join(folder, filename))
       if imp is None:
           print ("Image plus could not be generated from file:", filename)
           continue
       split_channels_blue(imp)


log_ls = ["Results"]
get_log_results("/Users/gceleste/Desktop/test/results.txt")

