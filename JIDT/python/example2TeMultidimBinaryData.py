##
# Java Information Dynamics Toolkit (JIDT)

# = Example 2 - Transfer entropy on multidimensional binary data =

# Simple transfer entropy (TE) calculation on multidimensional binary data
# using the discrete TE calculator.

# This example is important for Python users using JPype, because it shows
# how to handle multidimensional arrays from Python to Java.

from jpype import *
import random
import os
import sys

jarLocation = "./infodynamics.jar"
if (not(os.path.isfile(jarLocation))):
    exit("infodynamics.jar not found (expected at " +
         os.path.abspath(jarLocation) + ")")

# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# Create many columns in a multidimensional array, e.g.
# for fully random values:
# for 10 rows (time-steps) for 2 variables
# twoDTimeSeriesOctave = [[random.randint(0, 1) for y in range(2)]
#                         for x in range(10)]

# However here we want 2 rows by 100 columns where the next time step
# (row 2) is to copy the
# value of the column on the left from the previous time step (row 1):
nObv = 100
row1 = [random.randint(0, 1) for r in range(nObv)]

# Copy the previous row, offset one column to the right
row2 = [row1[nObv-1]] + row1[0:nObv-1]
TimeSeries = []
TimeSeries.append(row1)
TimeSeries.append(row2)
# 2 indicating 2D array
twoDTimeSeriesJavaInt = JArray(JInt, 2)(TimeSeries)

# Create a TE calculator and run it:
teCalcClass = JPackage(
    "infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
teCalc = teCalcClass(2, 1)
teCalc.initialise()

# Add observations of transfer across one cell to the right per time step:
teCalc.addObservations(twoDTimeSeriesJavaInt, 1)
result2D = teCalc.computeAverageLocalOfObservations()
print \
    ((' The result should be close to 1 bit here, \
since we are executing copy operations of \
what is effectively a random bit to each cell\
here: %.3f bits from %d observations') % (
        result2D, teCalc.getNumObservations()))
