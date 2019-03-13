import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['figure.titlesize'] = 18
plt.rcParams['figure.titleweight'] = 'medium'
plt.rcParams['lines.linewidth'] = 2.5

#S = stock underlying
#K = strike Price
#Price = premium paid for the option

S =
K =
Price =

def long_call(S,K,Price):
    #Long Call Payoff = max(Stock Price - Stike Price, 0)
    #If we are long a call, we would only elect to call if the current stock price is greater than
    # the stike price on our option
    P = list(map(lambda x: max(x - K,0) - Price, S))
    return P

def long_put(S,K,Price):
    #Long Put Payoff = max(Strike Price - Stock Price, 0)
    #If we are long a call, we would only elect to call if the current stock price is less than
    # the stike price on our option

    P = list(map(lambda x: max(K - x, 0) - Price, S))
    return P

def short_call(S,K,Price):
    #Payoff of a short put is just the inverse of the payoff a long put

    P = long_put(S,K, Price)
    return [-1.0*p for p in P]

def binary_call(S,K,Price):
    #payoff of a binary call is either:
    # 1. Strike if current price > strike
    #2. 0

    P = list(map(lambda x: K - Price if x > K else 0 - Price, S))
    return P

S = [t/S for t in range(0,1000)]

fig, ax = plt.subplot(nrows=2, ncols=2, sharex=True,sharey=True, figsize = (20,15))
fig.suptitle('Payoff Functions for long/Short Put/Calls', fontsize=20, fontweight='bold')
fig.text(0.5, 0.04, 'Stock/Underlying Price ($)', ha='center', fontsize=14, fontweight='bold')
fig.text(0.08, 0.5, 'Option Payoff ($)', va = 'center', rotations ='vertical', fontsize=14, fontweight='bold')

lc_p = long_call(S,100,10)
lp_p = long_puts(S,100,10)
plt.plot(S,lc_p,'r')
plt.plot(S,lp_p,'b')
plt.legend(['Long Call', 'Long Put'])

bc_P = binary_call(S,100,10)
bp_P = binary_put(S,100,10)
plt.subplot(222)
plt.plot(S,bc_P, 'b')
plt.plot(S,bp_P, 'r')
plt.legend(['Binary Call', 'Binary Put'])

T2 = long_call(S,120,10)
T4 = long_put(S,100,10)
plt.subplot(223)
plt.plot(S,T2,'r')
plt.plot(S,T4,'b')