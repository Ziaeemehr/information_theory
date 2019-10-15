# runHeartBreathRateKraskov.py kHistory lHistory knns numSurrogates
#
# runHeartBreathRateKraskov.py
# Used to explore information transfer in the heart rate / breath rate example of Schreiber --
#  but estimates TE using Kraskov-Stoegbauer-Grassberger estimation.
#
#
# Inputs
# - kHistory - destination embedding length
# - lHistory - source embedding length
# - knns - a scalar specifying a single, or vector specifying a comma separated list, for values of K nearest neighbours to evaluate TE (Kraskov) with.
# - numSurrogates - a scalar specifying the number of surrogates to evaluate TE from null distribution
#
# Run e.g. python runHeartBreathRateKraskov.py 2 2 1,2,3,4,5,6,7,8,9,10

import readFloatsFile
from jpype import *
import sys
import os
import random
import math
import string
import numpy
# Import our readFloatsFile utility in the above directory:
sys.path.append(os.path.relpath(".."))

# Change location of jar to match yours:
jarLocation = "../../../infodynamics.jar"
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# Read in the command line arguments and assign default if required.
# first argument in argv is the filename, so program arguments start from index 1.
if (len(sys.argv) < 2):
    kHistory = 1
else:
    kHistory = int(sys.argv[1])
if (len(sys.argv) < 3):
    lHistory = 1
else:
    lHistory = int(sys.argv[2])
if (len(sys.argv) < 4):
    knns = [4]
else:
    knnsStrings = sys.argv[3].split(",")
    knns = [int(i) for i in knnsStrings]
if (len(sys.argv) < 5):
    numSurrogates = 0
else:
    numSurrogates = int(sys.argv[4])

# Read in the data
datafile = '../../data/SFI-heartRate_breathVol_bloodOx.txt'
rawData = readFloatsFile.readFloatsFile(datafile)
# As numpy array:
data = numpy.array(rawData)
# Heart rate is first column, and we restrict to the samples that Schreiber mentions (2350:3550)
# Extracts what Matlab does with 2350:3550 argument there.
heart = data[2349:3550, 0]
# Chest vol is second column
chestVol = data[2349:3550, 1]
# bloodOx = data[2349:3550,2];

timeSteps = len(heart)

print("TE for heart rate <-> breath rate for Kraskov estimation with %d samples:" % timeSteps)

# Using a KSG estimator for TE is the least biased way to run this:
teCalcClass = JPackage(
    "infodynamics.measures.continuous.kraskov").TransferEntropyCalculatorKraskov
teCalc = teCalcClass()

teHeartToBreath = []
teBreathToHeart = []

for knnIndex in range(len(knns)):
    knn = knns[knnIndex]
    # Compute a TE value for knn nearest neighbours

    # Perform calculation for heart -> breath (lag 1)
    teCalc.initialise(kHistory, 1, lHistory, 1, 1)
    teCalc.setProperty("k", str(knn))
    teCalc.setObservations(JArray(JDouble, 1)(heart),
                           JArray(JDouble, 1)(chestVol))
    teHeartToBreath.append(teCalc.computeAverageLocalOfObservations())
    if (numSurrogates > 0):
        teHeartToBreathNullDist = teCalc.computeSignificance(numSurrogates)
        teHeartToBreathNullMean = teHeartToBreathNullDist.getMeanOfDistribution()
        teHeartToBreathNullStd = teHeartToBreathNullDist.getStdOfDistribution()

    # Perform calculation for breath -> heart (lag 1)
    teCalc.initialise(kHistory, 1, lHistory, 1, 1)
    teCalc.setProperty("k", str(knn))
    teCalc.setObservations(JArray(JDouble, 1)(chestVol),
                           JArray(JDouble, 1)(heart))
    teBreathToHeart.append(teCalc.computeAverageLocalOfObservations())
    if (numSurrogates > 0):
        teBreathToHeartNullDist = teCalc.computeSignificance(numSurrogates)
        teBreathToHeartNullMean = teBreathToHeartNullDist.getMeanOfDistribution()
        teBreathToHeartNullStd = teBreathToHeartNullDist.getStdOfDistribution()

    print("TE(k=%d,l=%d,knn=%d): h->b = %.3f" % (kHistory, lHistory,
                                                 knn, teHeartToBreath[knnIndex])),  # , for no newline
    if (numSurrogates > 0):
        print(" (null = %.3f +/- %.3f)" %
              (teHeartToBreathNullMean, teHeartToBreathNullStd)),
    print(", b->h = %.3f nats" % teBreathToHeart[knnIndex]),
    if (numSurrogates > 0):
        print("(null = %.3f +/- %.3f)" %
              (teBreathToHeartNullMean, teBreathToHeartNullStd)),
    print

# Exercise: plot the results
