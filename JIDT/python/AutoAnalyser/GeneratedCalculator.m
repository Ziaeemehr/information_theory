% Add JIDT jar library to the path, and disable warnings that it's already there:
warning('off','MATLAB:Java:DuplicateClass');
javaaddpath('/home/abolfazl/prog/install-dir/MI_TE/infodynamics-dist-1.5/infodynamics.jar');
% Add utilities to the path
addpath('/home/abolfazl/prog/install-dir/MI_TE/infodynamics-dist-1.5/demos/octave');

% 0. Load/prepare the data:
data = load('/home/abolfazl/prog/install-dir/MI_TE/infodynamics-dist-1.5/demos/data/2coupledRandomCols-1.txt');
% Column indices start from 1 in Matlab:
variable = octaveToJavaDoubleArray(data(:,1));

% 1. Construct the calculator:
calc = javaObject('infodynamics.measures.continuous.kozachenko.EntropyCalculatorMultiVariateKozachenko');
% 2. Set any properties to non-default values:
% No properties were set to non-default values
% 3. Initialise the calculator for (re-)use:
calc.initialise();
% 4. Supply the sample data:
calc.setObservations(variable);
% 5. Compute the estimate:
result = calc.computeAverageLocalOfObservations();

fprintf('H_Kozachenko-Leonenko(col_0) = %.4f nats\n', ...
	result);
