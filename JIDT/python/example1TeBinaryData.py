##
# Java Information Dynamics Toolkit (JIDT)
# = Example 1 - Transfer entropy on binary data =

# Simple transfer entropy (TE) calculation on binary data using
# the discrete TE calculator:


from time import time
import numpy as np
import jpype
import random
import numpy
import os

random.seed(124578)
start = time()

jarLocation = "./infodynamics.jar"
if (not(os.path.isfile(jarLocation))):
    exit("infodynamics.jar not found (expected at " +
         os.path.abspath(jarLocation) + ")")

# Start the JVM (add the "-Xmx" option with say 1024M if you get
# crashes due to not enough memory space)
jpype.startJVM(jpype.getDefaultJVMPath(), "-ea",
               "-Djava.class.path=" + jarLocation)

N = 100
# Generate some random binary data.
sourceArray = [random.randint(0, 1) for r in range(N)]
destArray = [0] + sourceArray[0:N-1]
sourceArray2 = [random.randint(0, 1) for r in range(N)]

# Create a TE calculator and run it:
teCalcClass = jpype.JPackage(
    "infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
teCalc = teCalcClass(2, 1)
teCalc.initialise()

# First use simple arrays of ints, which we can directly pass in:
teCalc.addObservations(sourceArray, destArray)
print("For copied source, result should be close to 1 bit : %.4f" %
      teCalc.computeAverageLocalOfObservations())
teCalc.initialise()
teCalc.addObservations(sourceArray2, destArray)
print("For random source, result should be close to 0 bits: %.4f" %
      teCalc.computeAverageLocalOfObservations())

# Next, demonstrate how to do this with a numpy array
teCalc.initialise()
# Create the numpy arrays:
sourceNumpy = np.array(sourceArray, dtype=np.int)
destNumpy = np.array(destArray, dtype=np.int)

# The above can be passed straight through to JIDT in python 2:
# teCalc.addObservations(sourceNumpy, destNumpy)
# But you need to do this in python 3:
sourceNumpyJArray = jpype.JArray(jpype.JInt, 1)(sourceNumpy.tolist())
destNumpyJArray = jpype.JArray(jpype.JInt, 1)(destNumpy.tolist())
teCalc.addObservations(sourceNumpyJArray, destNumpyJArray)
print("Using numpy array for copied source, result confirmed as: %.4f" %
      teCalc.computeAverageLocalOfObservations())

jpype.shutdownJVM()

print ("Done in %g seconds" % (time() - start))
