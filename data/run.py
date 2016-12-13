# Run script with python run.py sim_id, where sim_id is an integer to use for the sim_id (and the RNG seed)
import numpy as np
import rebound
from random import random, uniform, seed
import time
import sys

def collision(reb_sim, col):
    reb_sim.contents._status = 5
    return

maxorbs = 1.e4
path = '' #'/mnt/raid-cita/dtamayo/newstability/data/'

a1 = 1. # All distances in units of the innermost semimajor axis (always at 1)
Mstar = 1. # All masses in units of stellar mass

logMmin = np.log10(3.e-7) # Mars around Sun
logMmax = np.log10(1.e-3) # Jupiter around Sun
logemin = np.log10(1.e-3)
logemax = np.log10(0.3)
logincmin = np.log10(1.e-3)
logincmax = np.log10(0.1) # max mutual inclination of 11.4 degrees
betamin = 1. # min separation in Hill radii
betamax = 20.

sim_id = sys.argv[1]

seed(sim_id)

M1 = 10.**uniform(logMmin, logMmax)
M2 = 10.**uniform(logMmin, logMmax)
M3 = 10.**uniform(logMmin, logMmax)

e1 = 10.**uniform(logemin, logemax)
e2 = 10.**uniform(logemin, logemax)
e3 = 10.**uniform(logemin, logemax)

i1 = 10.**uniform(logincmin, logincmax)
i2 = 10.**uniform(logincmin, logincmax)
i3 = 10.**uniform(logincmin, logincmax)

hill12 = a1*((M1+M2)/3.)**(1./3.)
beta1 = uniform(betamin, betamax)
a2 = a1 + beta1*hill12

hill23 = a2*((M2+M3)/3.)**(1./3.)
beta2 = uniform(betamin, betamax)
a3 = a2 + beta2*hill23

sim = rebound.Simulation()
sim.integrator="whfast"
sim.ri_whfast.safe_mode = 0
sim.G = 4*np.pi**2

sim.add(m=1.)
sim.add(m=M1, a=a1, e=e1, pomega=random()*2.*np.pi, inc=i1, Omega=random()*2.*np.pi, f=random()*2.*np.pi, r=hill12)
sim.add(m=M2, a=a2, e=e2, pomega=random()*2.*np.pi, inc=i2, Omega=random()*2.*np.pi, f=random()*2.*np.pi, r=max(hill12, hill23))
sim.add(m=M3, a=a3, e=e3, pomega=random()*2.*np.pi, inc=i3, Omega=random()*2.*np.pi, f=random()*2.*np.pi, r=hill23)
sim.move_to_com()
ps = sim.particles

sim.dt = 0.09 # 0.09 of inner orbital period
sim.collision = "direct"
sim.collision_resolve = collision

features = [(a2-a1)/hill12, (a3-a2)/hill23]
for p in ps[1:sim.N_real]:
    features += [p.m, p.a, p.P, p.e, p.pomega, p.inc, p.Omega, p.f]

E0 = sim.calculate_energy()
t0 = time.time()

sim.initSimulationArchive(path+'runs/run'+str(sim_id)+'.bin', interval=maxorbs/100.)
sim.integrate(maxorbs)

if sim.t < maxorbs-1.: # allow for some fudge for t=999999999...
    stable = ['False']
else:
    stable = ['True']

features = stable+[sim.t]+features+[np.abs((sim.calculate_energy()-E0)/E0), time.time()-t0]
fname = path+'csvs/run'+str(sim_id)+'.csv'
with open(fname, 'w') as f:
    f.write(str(sim_id))
    for feature in features:
        f.write(',{0}'.format(feature))
        f.write('\n')
