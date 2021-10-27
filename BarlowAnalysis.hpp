#pragma once

#include <vector>

using std::vector;

class BarlowAnalysis {
	static int pyMod(int a, int b);
	static int omega(int x);
	static int phiNonPrime(vector<int> const& p, int n, int z);
	static int phiPrime(int h, int n);
public:
	static int signatureOrder(int x);
	static vector<int> primeFactors(int x);
	static vector<int> stratification(int x, int z);
	static vector<int> phiUp(std::vector<int> const& phi, std::vector<int> const& strats, int new_level);
	static vector<int> calculateSequence(int numerator, int stratLevel);
};