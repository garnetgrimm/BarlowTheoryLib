#include "BarlowAnalysis.hpp"
#include <math.h>

int BarlowAnalysis::pyMod(int a, int b)
{
	return ((a % b) + b) % b;
}

vector<int> BarlowAnalysis::primeFactors(int x) {
	vector<int> p;
	while(x % 2 == 0) {
		p.push_back(2);
		x = x / 2;
	}
	for(int i = 3; i < static_cast<int>(sqrt(x))+1; i += 2) {
		while(x % i == 0) {
			p.push_back(i);
			x = x / i;
		}
	}
	if(x > 2) {
		p.push_back(x);
	}
	return p;
}

std::vector<int> BarlowAnalysis::stratification(int x, int z) {
	std::vector<int> s;
	vector<int> factors = primeFactors(x);
	s.push_back(1);
	int valid_factor_count = std::min(z, static_cast<int>(factors.size()));
	for(int i = 0; i < valid_factor_count; i++) {
		s.push_back(factors[i]);
	}
	for(int i = 0; i < z - static_cast<int>(factors.size()); i++) {
		s.push_back(2);
	}
	s.push_back(1);
	return s;
}

int BarlowAnalysis::signatureOrder(int x) {
	std::vector<int> p = primeFactors(x);
	p.insert(p.begin(), 1);
	p.push_back(1);
	for(int i = p.size()-2; i > 0; i--) {
		if(p[i] != 2) return i;
	}
	return 0;
}

vector<int> BarlowAnalysis::phiUp(std::vector<int> const& phi, std::vector<int> const& strats, int new_level) {
	vector<int> new_phi;
	new_level += 1;
	int orig_pulse_count = phi.size();
	int new_pulse_count = 1;
	for(int level = 0; level < new_level; level++) {
		new_pulse_count *= strats[level];
	}
	for(unsigned i = 0; i < phi.size(); i++) {
		int new_e = phi[i] - (orig_pulse_count - new_pulse_count);
		if(new_e >= 0) new_phi.push_back(new_e);
	}
	return new_phi;
}

int BarlowAnalysis::phiNonPrime(std::vector<int> const& p, int n, int z) {
	int zeta = 1;
	for(int j = 1; j < z+1; j++) zeta *= p[j];
	
	int sum = 0;
	for(int r = 0; r < z; r++) {
		int kappa = 1;
		for(int k = 0; k < r+1; k++)
			kappa *= p[z+1-k];
		
		int prod = 1;
		for(int i = 0; i < z-r; i++)
			prod *= p[i];
		
		if(n < 2) n += zeta;
		
		int a = (n-2) % zeta;
		int b = (a / kappa) + 1;
		int c = b % p[z-r];
		int d = c + 1;
		int e = phiPrime(p[z-r], d);
		
		sum += prod*e;
	}
	return sum;
}

int BarlowAnalysis::omega(int x) {
	return ((x == 0) ? 0 : 1);
}

int BarlowAnalysis::phiPrime(int h, int n) {
	if(h <= 3) {
		return pyMod(h + n - 2, h);
	} else {
		int np = n - 1 + omega(h - n);
		vector<int> p = primeFactors(h - 1);
		p.insert(p.begin(), 1);
		p.push_back(1);
		int z = p.size() - 2;
		int a = phiNonPrime(p, np, z);
		int b = omega(a / (h / 4));
		int c = omega(h - n - 1);
		int d = (h/4)*(1-omega(h - n - 1));
		return (a+b)*c + d;
	}
}

vector<int> BarlowAnalysis::calculateSequence(int numerator, int stratLevel) {
	vector<int> phi;
	std::vector<int> p = stratification(numerator, stratLevel);
	
	int zeta = 1;
	for(int j = 1; j < stratLevel+1; j++) zeta *= p[j];

	for(int i = 0; i < zeta; i++) {
		int indisp = phiNonPrime(p, i+1, stratLevel);
		phi.push_back(indisp);
	}
	return phi;
}