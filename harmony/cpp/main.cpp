#include "json.h"
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <sstream>

using namespace std;

template <typename T>
ostream& operator<<(ostream& os, const vector<T>& v)
{
    os << "[";
    for (int i = 0; i < v.size(); ++i) {
        os << v[i];
        if (i != v.size() - 1)
            os << ", ";
    }
    os << "]";
    return os;
}


struct Ratio {
	float numerator;
	float denominator;
	
	float toFloat(bool inc) {
		if(!inc) return numerator / denominator;
		else return denominator / numerator;
	}
};

class BarlowGenerator {

	Json::Value intervalMap;

public:
	
	float minF;
	float baseF;
	float maxF;
	int minHarm; 
	
	BarlowGenerator(string filename, float minF, float maxF, float baseF, int minHarm) {
		this->minHarm = minHarm;
		this->minF = minF;
		this->maxF = maxF;
		this->baseF = baseF;
		std::ifstream interval_file(filename, std::ifstream::binary);
		interval_file >> intervalMap;
	}

	Ratio getRandomInterval() {
		if(minHarm < 3 || minHarm > 10) return {0, 0};
		string key = to_string(static_cast<float>(minHarm)*0.01).substr(0,4);		
		float sum = 0.0f;
		float randomSelection = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
		string selectedRatio;
		for (auto const& id : intervalMap[key].getMemberNames()) {
			sum += intervalMap[key][id].asFloat();
			if(sum > randomSelection) {
				selectedRatio = id;
				break;
			}
		}
		std::stringstream test(selectedRatio);
		string segment;
		std::getline(test, segment, '/');
		float bottomRatio = stof(segment);
		std::getline(test, segment, '/');
		float topRatio = stof(segment);
		return {topRatio, bottomRatio};
	}
	
	vector<float> genPhrase(int phraseLen) {
		vector<float> res;
		float currF = baseF;
		for(int note = 0; note < phraseLen; note++) {
			res.push_back(currF);
			float height = ((currF-minF)/(maxF-minF));
			float incWeight = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
			bool doInc = incWeight > height;
			Ratio ratio = getRandomInterval();
			currF *= ratio.toFloat(doInc);
		}
		return res;
	}

};

int main() {
	srand(time(0));
	
	BarlowGenerator bg("intervals.json", 100.0f, 450.0f, 250.0f, 10);
	
	for(int bar = 0; bar < 4; bar++) {
		std::cout << bg.genPhrase(4) << std::endl;
	}
}