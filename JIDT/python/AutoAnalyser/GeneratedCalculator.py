from jpype import *
import numpy
# Our python data file readers are a bit of a hack, python users will do better on this:
sys.path.append("/home/abolfazl/prog/install-dir/MI_TE/infodynamics-dist-1.5/demos/python")
import readFloatsFile

# Add JIDT jar library to the path
jarLocation = "/home/abolfazl/prog/install-dir/MI_TE/infodynamics-dist-1.5/infodynamics.jar"
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

# 0. Load/prepare the data:
dataRaw = readFloatsFile.readFloatsFile("/home/abolfazl/prog/install-dir/MI_TE/infodynamics-dist-1.5/demos/data/2coupledRandomCols-1.txt")
# As numpy array:
data = numpy.array(dataRaw)
variable = data[:,0]

# 1. Construct the calculator:
calcClass = JPackage("infodynamics.measures.continuous.kozachenko").EntropyCalculatorMultiVariateKozachenko
calc = calcClass()
# 2. Set any properties to non-default values:
# No properties were set to non-default values
# 3. Initialise the calculator for (re-)use:
calc.initialise()
# 4. Supply the sample data:
calc.setObservations(variable)
# 5. Compute the estimate:
result = calc.computeAverageLocalOfObservations()

print("H_Kozachenko-Leonenko(col_0) = %.4f nats" %
    (result))
