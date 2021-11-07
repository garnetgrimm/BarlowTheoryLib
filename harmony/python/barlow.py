import math
import sys

def hcf(a,b):
    if(b==0):
        return a
    else:
        return hcf(b,a%b)

def isPrime(n):
    if(n <= 1): return False
    if(n <= 3): return True
    if(n % 2 == 0 or n % 3 == 0): return False
    for i in range(5,int(math.sqrt(n) + 1), 6):
        if(n % i == 0 or n % (i + 2) == 0):
            return False
    return True

def primeFactors(x):
    p = []
    while x % 2 == 0:
        p.append(2)
        x = x // 2
    for i in range(3,int(math.sqrt(x))+1,2):
        while x % i == 0:
            p.append(i)
            x = x // i
    if x > 2:
        p.append(x)
    return p
    
def nextPrime(N):
    if (N <= 1):
        return 2
    prime = N
    found = False
    while(not found):
        prime = prime + 1
        if(isPrime(prime) == True):
            found = True
    return prime

def genPrimeArray(N):
    res = []
    prime = 1
    for i in range(N):
        res.append(prime)
        prime = nextPrime(prime)
    return res

def indigestibility(N):
    p = primeFactors(N) + [1]
    #if prime
    if(len(p) > 2):
        sum = 0
        for i in range(len(p)):
           sum += indigestibility(p[i])
        return sum
    else:
        sum = 0
        for r in range(0, len(p)):
            sum += (r+1)*((p[r]-1)**2)/p[r]
        return 2*sum

def harmonicity(P, Q):
    ip = indigestibility(P)
    iq = indigestibility(Q)
    igcf = indigestibility(math.gcd(P,Q))
    if(iq - ip > 0): sgn = 1
    else: sgn = -1
    denom = (ip + iq - 2*igcf)
    if(denom == 0): return sys.maxsize
    return sgn / denom

def ratioToCents(P, Q):
    return 1200*math.log2(P/Q)

def maxPrimePower(N, octaves, minHarmonicity):
    p = primeFactors(N)
    
    if(len(p) > 2):
        return -1
    else:
        numerator = octaves + 1/minHarmonicity
        if(N == 2):
            denominator = 1 + (math.log(256)/math.log(27))
        else:
            denominator = indigestibility(N) + math.log2(N)
        return int(numerator//denominator)

def calcMaxPowerSequence(minHarmonicity):
    prime = 2
    maxPower = 1
    maxPowers = []
    while maxPower > 0:
        maxPower = maxPrimePower(prime, 1, minHarmonicity)
        if(maxPower > 0):
            maxPowers.append(maxPower)
        prime = nextPrime(prime)
    return maxPowers

def genTruthTable(bits):
    table = []
    for i in range(pow(2, bits)):
        currEntry = []
        bitStr = ("{0:" + str(bits) + "b}").format(i)
        for char in bitStr:
            currEntry.append(char == "1")
        table.append(currEntry)
    return table
    
def primeDictToRatio(primeCountArray, primeArray, ordered=False):
    numProd = 1
    denProd = 1
    for i in range(len(primeArray)):
        if(primeCountArray[i] > 0): numProd *= pow(primeArray[i], primeCountArray[i])
        if(primeCountArray[i] < 0): denProd *= pow(primeArray[i], -primeCountArray[i])
    
    if(ordered and numProd > denProd):
        tempProd = numProd
        numProd = denProd
        denProd = numProd
    
    return (numProd, denProd)

def calcAllIntervals(minHarmonicity, verbose=False):
    maxPowerSeq = calcMaxPowerSequence(minHarmonicity)
    primes = genPrimeArray(len(maxPowerSeq)+1)[1:]
    
    if(verbose): print("Obtaining intervals for minHarmonicity:" , minHarmonicity)
    if(verbose): print("Obtaining positive intervals...")
    #get positive intervals
    positiveIntervals = []
    currInv = [0]*len(maxPowerSeq)
    finished = False
    while not finished:
        positiveIntervals.append(currInv[:])
        doRollOver = False
        for n in range(len(maxPowerSeq)-1, -1, -1):
            if(currInv[n] > maxPowerSeq[n]):
                if(n == 0):
                    finished = True
                    break
                else:
                    currInv[n] = 0
                    currInv[n-1] += 1
                    doRollOver = True
        if(not doRollOver): currInv[-1] += 1
    if(verbose): print(str(len(positiveIntervals)) + " positive intervals found")
    
    truthTable = genTruthTable(len(maxPowerSeq))
    
    #list all combinations of negative and positive versions
    if(verbose): print("Obtaining combinatory intervals...")
    possibleIntervals = []
    for negations in truthTable:
        for interval in positiveIntervals:
            new_interval = []
            for i in range(len(maxPowerSeq)):
                if(negations[i] == 0): scalar = 1
                else: scalar = -1
                new_interval.append(interval[i]*scalar)
            possibleIntervals.append(new_interval)
    if(verbose): print(str(len(possibleIntervals)) + " combinatory intervals found")
    
    #there has to be at least one negative and one positive prime
    if(verbose): print("Checking interval legality...")
    legalRatios = set()
    for i in range(len(possibleIntervals)):
        ratio = primeDictToRatio(possibleIntervals[i], primes, True)
        if(abs(ratio[1]) / abs(ratio[0]) <= 2.0): legalRatios.add(ratio)
    if(verbose): print(str(len(legalRatios)) + " legal intervals found")
    
    #remove duplicates
    if(verbose): print("Removing duplicate intervals...")
    ratios = dict()
    for ratio in legalRatios:
        harm = harmonicity(ratio[0], ratio[1])
        if((harm in ratios and ratios[harm][0] > ratio[0]) or harm not in ratios):
            if(abs(harm) > minHarmonicity): ratios[harm] = ratio
    if(verbose): print(str(len(ratios)) + " unique intervals found\n")
    
    return ratios

"""
#### TABLE 1
print(harmonicity(1,1))
print(harmonicity(15,16))
print(harmonicity(9,10))
print(harmonicity(8,9))
print(harmonicity(7,8))
print(harmonicity(6,7))
print(harmonicity(27,32))
print(harmonicity(5,6))
print(harmonicity(1,2))
"""

"""
### TABLE 2 - with some exceptions??
ratios = calcAllIntervals(0.06, True)
print(len(ratios))
for harm in ratios:
    print(ratios[harm], harm)
"""

"""
#### TABLE 3
for h in range(0, 10):
    minHarmonicity = 0.1 - float(h)*0.01
    print(calcMaxPowerSequence(minHarmonicity))
"""