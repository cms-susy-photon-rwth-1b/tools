#Create List of Signal points
import numpy as np

out=open("GGM_M1_M2_scan.txt","w")

for m1 in np.arange(200,1550,50):
	for m2 in np.arange(200,1550,50):
		out.write("GGM_M1_M2_"+str(m1)+"_"+str(m2)+".root\n")

out.close()

out=open("GGM_M1_M3_scan.txt","w")

for m1 in np.arange(50,1550,50):
	for m2 in np.arange(1000,2550,50):
		out.write("GGM_M1_M3_"+str(m1)+"_"+str(m2)+".root\n")

out.close()
