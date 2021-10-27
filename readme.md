# Barlow & Sioros
This repository contains source code for many of the algorithms outlined by music theorist Clarence Barlow in his paper Two Essays on Theory. I can't seem to find a public link for the Barlow paper, as I was only able to access it using a college login. 

I also included some of the algorithms described Sioros & Guedes in their 2011 paper [A Formal Approach for High-Level Automatic Rhythm Generation](https://archive.bridgesmathart.org/2011/bridges2011-233.pdf)

## "gotchas"
Please note that the denominator of a time signature only scales time and thus is not included in any of the calculations. 

### C++ Implementation Specific "gotchas"
The Barlow algorithm is a relatively straight forward computation and thus I have chosen to make all the methods static. The Sioros algorithm however contains many different moving parts, so I have chosen to go for a state based design for this library. In order to use the Sioros library, you have to instantiate a Sioros object, set the parameters, and then update. 
##### Barlow Example (bar of 4/4 subdivided to 16th note level)
`vector<int> phi = BarlowAnalysis::calculateSequence(4, 3);`
##### Sioros Example  (bar of 4/4 subdivided to 16th note level)
```
SiorosAnalysis analysis;
analysis.queuedParams.R = 0.1;
analysis.queuedParams.M = 0.1;
analysis.queuedParams.P = 0.1;
analysis.queuedParams.MaxSS = 3;
analysis.queuedParams.numerator = 4;
analysis.queuedParams.levels = 3;
//RUN ALL CALCULATIONS
analysis.update(false);
```
The library is smart enough to only run updates on the parts of the code that need to be updated, so it would be smart to save this SiorosAnalysis object somewhere safe ;)

### Python Gotchas
None, python is beautiful and easy.
```
#BARLOW
phi = stochasticBarlow(n, z, R, M)
#SIOROS
syncopatedBarlow(phi, 0, ssMax, sync_weights, sync_counter_weights)
```