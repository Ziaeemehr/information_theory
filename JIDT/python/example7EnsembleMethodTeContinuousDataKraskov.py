##
# Java Information Dynamics Toolkit (JIDT)
# = Example 7 - Ensemble method with transfer entropy on continuous data using Kraskov estimators =

#  Calculation of transfer entropy (TE) by supplying an ensemble of samples from multiple time series.
# We use continuous-valued data using the Kraskov-estimator TE calculator here.

from jpype import *
import random
import math
import os

jarLocation = "./infodynamics.jar"
if (not(os.path.isfile(jarLocation))):
    exit("infodynamics.jar not found (expected at " +
         os.path.abspath(jarLocation) + ")")

# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# Generate some random normalised data.
nObv = 1000
covariance = 0.4
numTrials = 10
kHistoryLength = 1

# Create a TE calculator and run it:
teCalcClass = JPackage(
    "infodynamics.measures.continuous.kraskov").TransferEntropyCalculatorKraskov
teCalc = teCalcClass()
teCalc.setProperty("k", "4")  # Use Kraskov parameter K=4 for 4 nearest points
teCalc.setProperty("NUM_THREADS", "1")

# Use target history length of kHistoryLength (Schreiber k)
teCalc.initialise(kHistoryLength)
teCalc.startAddObservations()

for trial in range(0, numTrials):
    # Create a new trial, with destArray correlated to
    #  previous value of sourceArray:
    sourceArray = [random.normalvariate(0, 1) for r in range(nObv)]
    destArray = [0] + [sum(pair) for pair in zip([covariance*y for y in sourceArray[0:nObv-1]],
                                                 [(1-covariance)*y for y in [random.normalvariate(0, 1) for r in range(nObv-1)]])]

    # Add observations for this trial:
    print("Adding samples from trial %d ..." % trial)
    teCalc.addObservations(JArray(JDouble, 1)(
        sourceArray), JArray(JDouble, 1)(destArray))

# We've finished adding trials:
print("Finished adding trials")
teCalc.finaliseAddObservations()

# Compute the result:
print("Computing TE ...")
result = teCalc.computeAverageLocalOfObservations()

# Note that the calculation is a random variable (because the generated
# data is a set of random variables) - the result will be of the order
# of what we expect, but not exactly equal to it; in fact, there will
# be some variance around it (smaller than example 4 since we have more samples).
print("TE result %.4f nats; expected to be close to %.4f nats for these correlated Gaussians " %
      (result, math.log(1.0/(1-math.pow(covariance, 2)))))

# And here's how to pull the local TEs out corresponding to each input time
# series under the ensemble method (i.e. for multiple trials).
localTEs = teCalc.computeLocalOfPreviousObservations()
# Need to convert to int for indices later
localValuesPerTrial = teCalc.getSeparateNumObservations()
startIndex = 0
for localValuesInThisTrial in localValuesPerTrial:
    endIndex = startIndex + localValuesInThisTrial - 1
    print("Local TEs for trial %d go from array index %d to %d" %
          (trial, startIndex, endIndex))
    print("  corresponding to time points %d:%d (indexed from 0) of that trial" % (
        kHistoryLength, nObv-1))
    # Access the local TEs for this trial as:
    localTEForThisTrial = localTEs[startIndex:endIndex]
    # Now update the startIndex before we go to the next trial
    startIndex = endIndex + 1
# And make a sanity check that we've looked at all of the local values here:
print("We've looked at %d local values in total, matching the number of samples we have (%d)" %
      (startIndex, teCalc.getNumObservations()))
