#pragma once

#include "BarlowAnalysis.hpp"

#include <vector>
#include <limits>

using std::vector;

constexpr int EPSILON = std::numeric_limits<float>::epsilon();

struct SiorosParams {
	float R;
	float M;
	float P;
	int MaxSS;
	int numerator;
	int levels;
};

class SiorosAnalysis : BarlowAnalysis {
	vector<int> phi;
	vector<int> strats;	
	
	vector<float> weighted_phi;
	vector<float> stochastic_phi;
	vector<float> pattern;
	
	vector<float> sync_weights;
	vector<float> sync_counter_weights;
	
	float syncopationRamp(float sequentialShiftCount, float sequentialShiftMax, float currWeight);
	int signatureOrder(int x);
	vector<float> randomWeights(int n);
	void clarenceBarlow();
	void weightedBarlow();
	void stochasticBarlow();
	void syncopatedBarlow();
	
	enum SeverityLevels {
		NONE_LEVEL=0,
		SYNCHO_LEVEL=1,
		STOCHA_LEVEL=2,
		WEIGHT_LEVEL=3,
		BARLOW_LEVEL=4,
	};
	void update(int severity, bool newWeights);
	int getUpdateSeverity();
	void update(int severity);
	
	SiorosParams usedParams;
	std::vector<int> phiUp(int new_level);
	
public:
	SiorosParams queuedParams;
	vector<int> getPhi();
	vector<int> getStrats();
	vector<float> getWeightedPhi();
	vector<float> getStochasticPhi();
	vector<float> getPattern();
	
	void update(bool newWeights);
};