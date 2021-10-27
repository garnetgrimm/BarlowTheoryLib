#include "SiorosAnalysis.hpp"
#include <math.h>
#include <algorithm>

vector<float> SiorosAnalysis::randomWeights(int n) {
	vector<float> arr;
	for(int i = 0; i < n; i++) {
		float x = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
		arr.push_back(x);
	}
	return arr;
}

float SiorosAnalysis::syncopationRamp(float sequentialShiftCount, float sequentialShiftMax, float currWeight) {
	float a = 1.0 - (sequentialShiftCount/sequentialShiftMax);
	float b = 1.0 - currWeight;
	return 1.0 - std::max(0.0f, a*b);
}

void SiorosAnalysis::weightedBarlow() 
{
	//update(std::min(getUpdateSeverity(), SeverityLevels::WEIGHT_LEVEL - 1));
	weighted_phi.clear();
	weighted_phi.resize(phi.size(), 0);
	for(unsigned level = 0; level < strats.size(); level++) {
		float wiMax = pow(usedParams.R, level);
		float wiMin = pow(usedParams.R, level+1);
		std::vector<int> phi_level = phiUp(level);
		float weight_per_idx = (wiMax - wiMin) / (phi_level.size() + 1);
		float idx_per_idx = phi.size() / phi_level.size();
		for(unsigned i = 0; i < phi_level.size(); i++) {
			float weight = wiMax - weight_per_idx*i;
			int index = static_cast<int>(i*idx_per_idx);
			weighted_phi[index] += weight;
		}
	}
}

void SiorosAnalysis::stochasticBarlow() {
	//update(std::min(getUpdateSeverity(), SeverityLevels::STOCHA_LEVEL - 1));
	vector<float> stochastic_phi;
	stochastic_phi.resize(phi.size(), 0);
	float maxW = *std::max_element(weighted_phi.begin(), weighted_phi.end());
	float n = 1.0/maxW;
	for(unsigned l = 0; l < weighted_phi.size(); l++)
		stochastic_phi[l] = n*pow(weighted_phi[l], usedParams.M);
	this->stochastic_phi = stochastic_phi;
}

void SiorosAnalysis::syncopatedBarlow()
{
	//update(std::min(getUpdateSeverity(), SeverityLevels::SYNCHO_LEVEL - 1));
	vector<float> pattern;
	bool mute = false;
	int seq_shift = 0;
	for(unsigned i = 0; i < phi.size(); i++) {
		if(mute) {
			pattern.push_back(0.0);
			mute = false;
		} else {
			bool do_shift = usedParams.P > sync_weights[i];
			bool cancel_shift = syncopationRamp(seq_shift, usedParams.MaxSS, stochastic_phi[i]) > sync_counter_weights[i];
			do_shift = (do_shift && !cancel_shift);
			if(do_shift) {
				pattern.push_back(stochastic_phi[(i + 1) % stochastic_phi.size()]);
				mute = true;
				seq_shift++;
			} else {
				pattern.push_back(stochastic_phi[i]);
				seq_shift = 0;
			}
		}
	}
	if(pattern[pattern.size()-1] > 0.99) pattern[pattern.size()-1] = 0.0;
	this->pattern = pattern;
}

int SiorosAnalysis::getUpdateSeverity() {
	int updateSeverity = SeverityLevels::NONE_LEVEL;
	if(usedParams.MaxSS != queuedParams.MaxSS) updateSeverity = SeverityLevels::SYNCHO_LEVEL;
	if(fabs(usedParams.P - queuedParams.P) > EPSILON) updateSeverity = SeverityLevels::SYNCHO_LEVEL;
	if(fabs(usedParams.M - queuedParams.M) > EPSILON) updateSeverity = SeverityLevels::STOCHA_LEVEL;
	if(fabs(usedParams.R - queuedParams.R) > EPSILON) updateSeverity = SeverityLevels::WEIGHT_LEVEL;
	if(usedParams.numerator != queuedParams.numerator) updateSeverity = SeverityLevels::BARLOW_LEVEL;
	if(usedParams.levels != queuedParams.levels) updateSeverity = SeverityLevels::BARLOW_LEVEL;
	return updateSeverity;
}

void SiorosAnalysis::update(bool newWeights) {
	int severity = getUpdateSeverity();
	update(severity, newWeights);
}

void SiorosAnalysis::update(int severity) {
	update(severity, false);
}

void SiorosAnalysis::update(int severity, bool newWeights) {
	usedParams.MaxSS = queuedParams.MaxSS;
	usedParams.P = queuedParams.P;
	usedParams.M = queuedParams.M;
	usedParams.R = queuedParams.R;
	usedParams.numerator = queuedParams.numerator;
	usedParams.levels = queuedParams.levels;
	
	if(severity >= SeverityLevels::BARLOW_LEVEL) {
		strats = stratification(usedParams.numerator, usedParams.levels);
		clarenceBarlow();
		newWeights = true;
	}
	if(newWeights) {
		sync_weights = randomWeights(phi.size());
		sync_counter_weights = randomWeights(phi.size());
		severity = 3;
	}
	if(severity >= SeverityLevels::WEIGHT_LEVEL) weightedBarlow();
	if(severity >= SeverityLevels::STOCHA_LEVEL) stochasticBarlow();
	if(severity >= SeverityLevels::SYNCHO_LEVEL) syncopatedBarlow();
}

vector<int> SiorosAnalysis::getPhi() {
	return phi;
}
vector<int> SiorosAnalysis::getStrats() {
	return strats;
}
vector<float> SiorosAnalysis::getWeightedPhi() {
	return weighted_phi;
}
vector<float> SiorosAnalysis::getStochasticPhi() {
	return stochastic_phi;
}
vector<float> SiorosAnalysis::getPattern() {
	return pattern;
}


std::vector<int> SiorosAnalysis::phiUp(int new_level) {
	return BarlowAnalysis::phiUp(phi, strats, new_level);
}
void SiorosAnalysis::clarenceBarlow() {
	phi = BarlowAnalysis::calculateSequence(queuedParams.numerator, queuedParams.levels);
}