import math
import random

random.seed(10)

def prime_factors(x):
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

def stratification(x, z):
    p = prime_factors(x)
    p = p[0:min(z, len(p))]
    p += [2]*(z - len(p))
    p.insert(0, 1)
    p.append(1)
    return p

def signature_order(x):
    p = prime_factors(x)
    p.insert(0, 1)
    p.append(1)
    for i in range(len(p)-2, 0, -1):
        if(p[i] != 2): return i
    return 0

def phi_up(phi, strats, new_level):
    new_level += 1
    new_phi = []
    orig_pulse_count = len(phi)
    new_pulse_count = 1
    for level in range(0, new_level):
        new_pulse_count *= strats[level]
    for e in phi:
        new_e = e - (orig_pulse_count - new_pulse_count)
        if(new_e >= 0): new_phi.append(new_e)
    return new_phi

def phi_nonprime(p, n, z):  
    zeta = 1
    for j in range(1, z+1):
        zeta *= p[j]
    
    sum = 0
    for r in range(0, z):
        kappa = 1
        for k in range(0, r+1):
            kappa *= p[z+1-k]
    
        prod = 1
        for i in range(0, z-r):
            prod *= p[i]
        
        a = (n-2) % zeta
        b = (a / kappa) + 1
        c = math.floor(b)
        d = c % p[z-r]
        e = d + 1
        
        f = phi_prime(p[z-r], e)
        
        if(f is None):
            return None
        
        sum += prod*f
    return sum

def omega(x):
    if(x == 0): return 0
    return 1

def phi_prime(h, n):
    if(h <= 3):
        return (h + n - 2) % h
    else:
        np = n - 1 + omega(h - n)
        
        p = prime_factors(h - 1)
        p.insert(0, 1)
        p.append(1)
        
        z = len(p) - 2
        
        a = phi_nonprime(p, np, z)
        b = omega(a // (h//4))
        c = omega(h - n - 1)
        d = (h//4)*(1-omega(h - n - 1))
        return (a + b)*c + d

def clarenceBarlow(num, z):
    p = stratification(num, z)

    zeta = 1
    for j in range(1, z+1):
        zeta *= p[j]
    
    phi = []
    for i in range(0, zeta):
        indisp = phi_nonprime(p, i+1, z)
        if(indisp is None):
            return []
        phi.append(indisp)
    
    return phi
    
def weightedBarlow(num, z, R):
    strats = stratification(num, z)
    phi = clarenceBarlow(num, z)
    weighted_phi = [0]*len(phi)
    for i in range(0, z+1):
        WiMax = pow(R, i)
        WiMin = pow(R, i+1)
        phi_level = phi_up(phi, strats, i)
        weight_per_idx = (WiMax - WiMin) / (len(phi_level) + 1)
        idx_per_idx = len(phi) / len(phi_level)
        for i in range(0, len(phi_level)):
            weight = WiMax - weight_per_idx*i
            index = int(i*idx_per_idx)
            weighted_phi[index] += weight
    return weighted_phi

def stochasticBarlow(num, z, R, N):
    W = weightedBarlow(num, z, R)
    p = [0]*len(W)
    n = 1.0/max(W)
    for l in range(0, len(W)):
        p[l] = n*pow(W[l], M)
    return p

def randomWeights(n):
    arr = []
    for i in range(0, n):
        arr.append(random.uniform(0, 1))
    return arr

def syncopationRamp(sequentialShiftCount, sequentialShiftMax, currWeight):
    a = 1.0 - (sequentialShiftCount/sequentialShiftMax)
    b = 1.0 - currWeight
    return 1.0 - max(0, a*b)

def syncopatedBarlow(phi, P, ssMax, weights, counter_weights):
    weighted_phi = []
    mute = False
    seq_shift = 0
    for i in range(0, len(phi)):
        if(mute):
            weighted_phi.append(0.0)
            mute = False
        else:
            do_shift = P > weights[i]
            cancel_shift = syncopationRamp(seq_shift, ssMax, phi[i]) > counter_weights[i]
            do_shift = do_shift and not cancel_shift
            if(do_shift):
                weighted_phi.append(phi[(i + 1) % len(phi)])
                mute = True
                seq_shift += 1
            else:
                weighted_phi.append(phi[i])
                seq_shift = 0
    return weighted_phi
    
#Numerator of the time signature. Denominator does not matter, only scales time
n = 3
#Max stratification level
z = 3
#Controls how much each stratification level contributes
#float between 0 to 1
#0 means only first level contributes, 1 means all levels contribute equally
R = 1
#Controls metrical feel
#float between 0 to 1
M = 1
#Controls syncopation probability
#float between 0 to 1
#0 means no change, 1 means entirely shifted over by 1
P = 0.5

#Controls how many syncopated (shifted) notes there could possibly be in a row
#int range 0 to n
ssMax = 3

phi = stochasticBarlow(n, z, R, M)

sync_weights = randomWeights(len(phi))
sync_counter_weights = randomWeights(len(phi))

print(phi)
print(syncopatedBarlow(phi, 0, ssMax, sync_weights, sync_counter_weights))