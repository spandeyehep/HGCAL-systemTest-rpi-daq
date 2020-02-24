import ROOT as rt
import os, sys
from optparse import OptionParser
import numpy as np



#rt.ROOT.EnableImplicitMT()

def getBin(chip,channel):
	toReturn = (chip*64) + channel
	if(toReturn > 256):
		print "Invalid bin = %d, for chip=%d, channel=%d"%(toReturn,chip,channel)
		sys.exit(0)
	
	return toReturn 


parser = OptionParser()
parser.add_option("-f", "--inFileName", dest="inFileName",action="store",
                      help="input File Name",default="inin.root")
parser.add_option("-a", "--chip", dest="chip",type="int",action="store",
                      help="select chip to plot",default=2)
parser.add_option("-b", "--channel", dest="channel",type="int",action="store",
                      help="select channel to plot",default=36)
parser.add_option("-c", "--maxTS", dest="maxTS",type="int",action="store",
                      help="maximum Time sample",default=3)
parser.add_option("-o", "--outFileName", dest="outFileName",action="store",
                      help="outPut File Name",default="outout.root")

(options, args) = parser.parse_args()
print(options)


inFileName = options.inFileName
outFileName = options.outFileName
chip = options.chip
channel = options.channel
maxTS = options.maxTS
inFile = rt.TFile.Open(inFileName)

if(not inFile):
	print "Could not open file : ",inFileName
	sys.exit()

inTree = inFile.Get("triggerhits")

if(not inTree):
	print "Could not find triggerhits in file :",inFileName
	sys.exit()

#array = inTree.AsMatrix(columns=["hg"])

# array = inTree.AsMatrix()
# print("Tree converted to a numpy array:\n{}\n".format(array))



# array = inTree.AsMatrix(columns=["x"])


outFile = rt.TFile.Open(outFileName,"recreate")

totslow_profile = rt.TProfile("totslow_profile","tot_slow vs event",1000,0,1000)
totslow_profile.GetXaxis().SetTitle("Event #")
totslow_profile.GetYaxis().SetTitle("Time-over-Threshold")
hg_profile = rt.TProfile("hg_profile","High Gain TS%d vs event"%(maxTS),1000,0,1000)
hg_profile.GetXaxis().SetTitle("Event #")
hg_profile.GetYaxis().SetTitle("High Gain TS %d"%(maxTS))

lg_profile = rt.TProfile("lg_profile","Low Gain TS%d vs event"%(maxTS),1000,0,1000)
lg_profile.GetXaxis().SetTitle("Event #")
lg_profile.GetYaxis().SetTitle("High Gain TS %d"%(maxTS))

pulseShapes = outFile.mkdir("pulseShapes")
pulseShapes.cd()
HG_pulseShapes = pulseShapes.mkdir("HighGain")
LG_pulseShapes = pulseShapes.mkdir("LowGain")


hg_pulseShape_profile = list()
lg_pulseShape_profile = list()
for i in range(1000):
	HG_pulseShapes.cd()
	prof_name = "hg_profile_chip%02dchan%02d_event_%04d"%(chip,channel,i+1)
	temp_prof = rt.TProfile(prof_name,prof_name,13,0,13)
	hg_pulseShape_profile.append(temp_prof)
	LG_pulseShapes.cd()
	prof_name = "lg_profile_chip%02dchan%02d_event_%04d"%(chip,channel,i+1)
	temp_prof = rt.TProfile(prof_name,prof_name,13,0,13)
	lg_pulseShape_profile.append(temp_prof)

rt.TProfile("totslow_profile","tot_slow vs event",1000,0,1000)

for i,event in enumerate(inTree):
	#print "################## Event %d #############"%(event.event)
	chip_ = event.chip
	channel_ = event.channel ## channel[256]/I
	hg = event.hg   ## hg[11][256]/I
	# print event.hg
	# print event.channel
	# print len(hg_)
	# for j in hg_:
	# 	print j
	# for ii,itr in enumerate(hg):
	# 	print ii,":",itr


	# sys.exit()
	lg = event.lg	## lg[11][256]/I
	tot_slow = event.totslow ## totslow[256]/I
	bin_ = getBin(chip,channel)
	totslow_profile.Fill(i+1,tot_slow[bin_],1)
	hg_profile.Fill(i+1,hg[bin_ + (maxTS*256)],1)
	lg_profile.Fill(i+1,lg[bin_ + (maxTS*256)],1)
	for j in range(11):
		if(i == 500):
			#print "timesamp:%d,hg:%d"%(j+1,hg[(bin_*11)+j])
			print "timesamp:%d,hg:%d"%(j+1,hg[bin_ + (j*256)])

		#hg_pulseShape_profile[i].Fill(j+1,hg[j][bin_],1)
		#hg_pulseShape_profile[i].Fill(j+1,hg[(bin_*11)+j],1)
		hg_pulseShape_profile[i].Fill(j+1,hg[bin_ + (j*256)],1)
		lg_pulseShape_profile[i].Fill(j+1,lg[bin_ + (j*256)],1)
	

# for i,j in enumerate(hg_pulseShape_profile):
# 	print "%d : %s"%(i,j.GetName())



outFile.cd()
# totslow_profile.Write()
# hg_pulseShape_profile.Write()
outFile.Write()
outFile.Close()


print "Done!!!"

