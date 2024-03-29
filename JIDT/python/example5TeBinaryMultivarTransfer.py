##
# Java Information Dynamics Toolkit (JIDT)
# = Example 5 - Multivariate transfer entropy on binary data =

# Multivariate transfer entropy (TE) calculation on binary data using the discrete TE calculator:

from jpype import *
import random
from operator import xor
import os

jarLocation = "./infodynamics.jar"
if (not(os.path.isfile(jarLocation))):
    exit("infodynamics.jar not found (expected at " +
         os.path.abspath(jarLocation) + ")")

# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# Generate some random binary data.
nObv = 20000
# for 10 rows (time-steps) for 2 variables
sourceArray = [[random.randint(0, 1) for y in range(2)] for x in range(nObv)]
# for 10 rows (time-steps) for 2 variables
sourceArray2 = [[random.randint(0, 1) for y in range(2)] for x in range(nObv)]

# Destination variable takes a copy of the first bit of the source in bit 1,
# and an XOR of the two bits of the source in bit 2:
destArray = [[0, 0]]
for j in range(1, nObv):
    destArray.append(
        [sourceArray[j-1][0], xor(sourceArray[j-1][0], sourceArray[j-1][1])])

# Create a TE calculator and run it:
teCalcClass = JPackage(
    "infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
teCalc = teCalcClass(4, 1)
teCalc.initialise()
# We need to construct the joint values of the dest and source before we pass them in,
# and need to use the matrix conversion routine when calling from Matlab/Octave:
mUtils = JPackage('infodynamics.utils').MatrixUtils
teCalc.addObservations(mUtils.computeCombinedValues(sourceArray, 2),
                       mUtils.computeCombinedValues(destArray, 2))
result = teCalc.computeAverageLocalOfObservations()
print('For source which the 2 bits are determined from, result should be close to 2 bits : %.3f' % result)
teCalc.initialise()
teCalc.addObservations(mUtils.computeCombinedValues(sourceArray2, 2),
                       mUtils.computeCombinedValues(destArray, 2))
result2 = teCalc.computeAverageLocalOfObservations()
print('For random source, result should be close to 0 bits in theory: %.3f' % result2)
print('The result for random source is inflated towards 0.3 due to finite\
 observation length (%d).\nOne can verify that the answer is consistent with\
 that from a random source by \nchecking: teCalc.computeSignificance(numberOfObservation); ans.pValue\n' % teCalc.getNumObservations())

sol = teCalc.computeSignificance(nObv)
print(sol.pValue)
