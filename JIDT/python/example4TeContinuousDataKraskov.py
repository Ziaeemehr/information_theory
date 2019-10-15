##
# Java Information Dynamics Toolkit (JIDT)
# = Example 4 - Transfer entropy on continuous data using Kraskov estimators =
# Simple transfer entropy (TE) calculation on continuous-valued data using the Kraskov-estimator TE calculator.

from random import normalvariate as normal
import numpy as np
import pylab as pl
from jpype import *
import random
import math
import sys
import os

random.seed(1)

jarLocation = "./infodynamics.jar"
if (not(os.path.isfile(jarLocation))):
    exit("infodynamics.jar not found (expected at " +
         os.path.abspath(jarLocation) + ")")

# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# Generate some random normalised data.
nObv = 1000         # number of observations
covariance = 0.4
# Source array of random normals:
sourceArray = [normal(0, 1) for r in range(nObv)]
# Destination array of random normals with partial correlation to previous value of sourceArray
destArray = [0] + [sum(pair) for pair in zip([covariance*y for y in sourceArray[0:nObv-1]],
                                             [(1 - covariance) * y for y in [normal(0, 1) for r in range(nObv - 1)]])]

# Uncorrelated source array:
sourceArray2 = [normal(0, 1) for r in range(nObv)]

# Create a TE calculator and run it:
teCalcClass = JPackage(
    "infodynamics.measures.continuous.kraskov").TransferEntropyCalculatorKraskov
teCalc = teCalcClass()
teCalc.setProperty("NORMALISE", "true")  # Normalise the individual variables
teCalc.initialise(1)  # Use history length 1 (Schreiber k=1)
teCalc.setProperty("k", "4")  # Use Kraskov parameter K=4 for 4 nearest points

# Perform calculation with correlated source:
teCalc.setObservations(JArray(JDouble, 1)(sourceArray),
                       JArray(JDouble, 1)(destArray))
result = teCalc.computeAverageLocalOfObservations()

# Note that the calculation is a random variable (because the generated
# data is a set of random variables) - the result will be of the order
# of what we expect, but not exactly equal to it; in fact, there will
# be a large variance around it.
# Expected correlation is
# expected covariance / product of expected standard deviations:
# (where square of destArray standard dev is sum of squares of std devs of
# underlying distributions)
corr_expected = covariance / \
    (1 * math.sqrt(covariance ** 2 + (1 - covariance) ** 2))
d_nats = -0.5 * math.log(1 - corr_expected ** 2)
d_bits = d_nats/np.log(2.0)

print("TE result %.4f nats, %.4f bits; expected to be close to %.4f nats, %.4f bits for these correlated Gaussians" %
      (result, result/np.log(2.0), d_nats, d_bits))

# A = teCalc.computeLocalOfPreviousObservations()
# print(np.mean(A[1:]))

# Perform calculation with uncorrelated source:
teCalc.initialise()  # Initialise leaving the parameters the same
teCalc.setObservations(JArray(JDouble, 1)(sourceArray2),
                       JArray(JDouble, 1)(destArray))
result2 = teCalc.computeAverageLocalOfObservations()
print("TE result %.4f nats, %.4f bits; expected to be close to 0 nats for these uncorrelated Gaussians" % (
    result2, result2/np.log(2.0)))


# fig, ax = pl.subplots(ncols=2)
# ax[0].scatter(sourceArray, destArray, s=10)
# ax[1].scatter(sourceArray, sourceArray2, s=10)
# pl.show()
# sys.exit(0)
