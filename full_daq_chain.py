
###		Script to run full DAQ chain for 6" sensor test stand
###		1. DAQ
###		2. Analysis
###		3. Pedestal/noise plotter in for HG/LG
###
###		Author : Shubham Pandey
###		Email  : shubham.pandey@cern.ch
###
###		Change directories accordingly before running the script
###		run "python full_daq_chain.py -h" to see available options


import os,sys
from optparse import OptionParser
import glob

run_command = True


print "\n\nIMPORTANT : Run Command is ",run_command
print"\n\n"
parser = OptionParser()
parser.add_option("-a", "--moduleNumber", dest="moduleNumber",action="store",
                      help="module number",default="0")
choices_m=["standard","sweep","fixed","const_inj","instrumental_trigger","external_trigger"]
parser.add_option("-b", "--acquisitionType", dest="acquisitionType",choices=choices_m,
                  help="acquisition method, valid choices are:\t%s"%(choices_m), default="standard")
parser.add_option("-c", "--nEvent", dest="nEvent",type="int",action="store",
                  help="number of events",default=1000)
parser.add_option("-d", "--HVOff", dest="HVOff",action="store_true",
                      help="set this to precise when bias voltage is off",default=False)
parser.add_option("-e", "--ground", dest="ground",action="store_true",
                      help="set True if module is grounded",default=True)
(options, args) = parser.parse_args()
print(options)

MODULENUMBER=options.moduleNumber
ACQUISITIONTYPE=options.acquisitionType
NEVENTS=options.nEvent
HV_FLAG=options.HVOff
GROUND=options.ground

if(HV_FLAG):
	HV_string = "HVOn"
else:
	HV_string = "HVOff"

if(GROUND):
	ground_string = "withGround"
else:
	ground_string = "withOutGround"


###############################
#######     rpi-daq     #######
###############################

print "\n\n"
print "###############################"
print "#######     rpi-daq     #######"
print "###############################"
print "\n\n"

dir_ = "/home/shubham/work/cern_lab/rpi-daq/"

if(run_command):
	os.chdir(dir_)
	print os.getcwd()

cmd = "python daq-zmq-client.py -b %s -g %d -i %s_%s_%s"%(ACQUISITIONTYPE,NEVENTS,MODULENUMBER,HV_string,ground_string)
print cmd
if(run_command):
	os.system(cmd)



########################################
#######     rpi-daq-analyzer     #######
########################################

print "\n\n"
print "########################################"
print "#######     rpi-daq-analyzer     #######"
print "########################################"
print "\n\n"
list_of_files = glob.glob('/home/shubham/work/cern_lab/rpi-daq/data/*.raw') 
latest_file = max(list_of_files, key=os.path.getctime)
#print latest_file

if(ACQUISITIONTYPE=="standard"):
	TYPE="pedestal"
else:
	sys.exit()

dir_ = "/home/shubham/work/cern_lab/rpi-daq-analyzer"

if(run_command):
	os.chdir(dir_)
	print os.getcwd()


root_output_fileName = (latest_file.split("/")[-1:][0]).strip(".raw")


cmd = "./bin/hexaboardAnalyzer -f %s -a %s -O output_files -o %s -m chanID_to_pad.txt --hexaboardType=6inch -s 1"%(latest_file,TYPE,root_output_fileName)
print cmd
if(run_command):
	os.system(cmd)
# cmd = "./bin/hexaboardAnalyzer -f Module132_BVOFF_withground_13-2-2020_19-36.raw  -a pedestal -O rawout -o Module132_BVOFF_withground_13-2-2020_19-36 --maxTS=5 -m chanID_to_pad.txt  --hexaboardType=6inch -s 1"



###########################################
#######     rpi-daq-hex_plotter     #######
###########################################
print "\n\n"
print "###########################################"
print "#######     rpi-daq-hex_plotter     #######"
print "###########################################"
print "\n\n"

run_command = True
list_of_files = glob.glob('/home/shubham/work/cern_lab/rpi-daq-analyzer/output_files/*.txt') 
latest_file = max(list_of_files, key=os.path.getctime)
#print latest_file

dir_ = "/home/shubham/work/cern_lab/hex_plot/HGCAL_sensor_analysis/"
os.chdir(dir_)
print os.getcwd()
# if(run_command):
# 	os.system(cmd)

text_output_fileName = "/home/shubham/work/cern_lab/rpi-daq-analyzer/output_files/"+(latest_file.split("/")[-1:][0])
png_fileName = (latest_file.split("/")[-1:][0]).strip(".txt")

cmd = "./bin/HexPlot -i %s -g geo/hex_positions_HPK_128ch_6inch.txt -o output_plots/PedestalLG_%s.png --noinfo --vn current:LG_pedestal:\"ADC counts\" -z 180:320 --select 0"%(text_output_fileName,png_fileName)
print cmd
if(run_command):
	os.system(cmd)

cmd = "./bin/HexPlot -i %s -g geo/hex_positions_HPK_128ch_6inch.txt -o output_plots/PedestalHG_%s.png --noinfo --vn current:HG_pedestal:\"ADC counts\" -z 180:320 --select 100"%(text_output_fileName,png_fileName)
print cmd
if(run_command):
	os.system(cmd)

cmd = "./bin/HexPlot -i %s -g geo/hex_positions_HPK_128ch_6inch.txt -o output_plots/NoiseLG_%s.png --noinfo --vn current:LG_noise:\"ADC counts\" -z 0:10 --select 200"%(text_output_fileName,png_fileName)
print cmd
if(run_command):
	os.system(cmd)

cmd = "./bin/HexPlot -i %s -g geo/hex_positions_HPK_128ch_6inch.txt -o output_plots/NoiseHG_%s.png --noinfo --vn current:HG_noise:\"ADC counts\" -z 0:20 --select 300"%(text_output_fileName,png_fileName)
print cmd
if(run_command):
	os.system(cmd)


