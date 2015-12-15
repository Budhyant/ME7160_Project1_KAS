import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import fmin_slsqp
from scipy.integrate import odeint
# # --------------------------------------------------------------------------------------------------------------------
font = {'family' : 'monospace',
        'weight' : 'normal',
        'size'   : 52}
plt.rc('font', **font)
linewidth = 9.0
markersize = 20
# # --------------------------------------------------------------------------------------------------------------------
m1=2.0
l1=1.0
m2=1.0
l2=2.0
g=32.2

N = 9
T = 2*2*np.pi
t = np.linspace(0, T, N+1)
t = t[0:-1]
Omega = np.fft.fftfreq(N, T/(2*np.pi*N))
theta10 = 0
theta20 = 0

def residual(theta):
    Theta1 = np.fft.fft(theta(1))
    Theta2 = np.fft.fft(theta(2))
    dtheta1 = np.fft.ifft(np.multiply(1j * Omega, Theta1))
    dtheta2 = np.fft.ifft(np.multiply(1j * Omega, Theta2))
    ddtheta1 = np.fft.ifft(np.multiply(-Omega**2, Theta1))
    ddtheta2 = np.fft.ifft(np.multiply(-Omega**2, Theta2))
    R1 = (m1+m2)*l1*ddtheta1+m2*l2*np.cos(theta(1)-theta(2))*ddtheta2+m2*l2*np.sin(theta(1)-theta(2))*dtheta2**2+g*(m1+m2)*np.sin(theta(1))
    R2 = m2*l2*ddtheta2+m2*l1*np.cos(theta(1)-theta(2))*ddtheta1-m2*l1*np.sin(theta(1)-theta(2))*dtheta2**2+g*(m2)*np.sin(theta(2))

    #R2 =  m2*l2*ddtheta2 + m2*l1*np.cos(theta(1)- theta(2))*ddtheta1-m2*l1*np.sin(theta(1)-theta(2))*dtheta1**2+m2*g*np.sin(theta(2))
    R = np.sum(np.abs((R1**2+R2**2)))
    return R

# res = minimize(residual, x0, options={'method':'SLSQP', 'maxiter':1000000})
res1 = minimize(residual,[1,1])
#res2 = minimize(residual, theta20)
theta1Sol = res1.theta1
#theta2Sol = res2.theta2

# Numerical solution
# def RHS(X, t=0.0):
#     x1, x2 = X
#     x1dot = x2
#     x2dot = -x1 - epsilon * (2 * mu * x2 + alpha * x1**3 + 2 * k * x1 * np.cos(omega * t)) + np.sin(2 * t)
#     return [x1dot, x2dot]
#
# ta = np.linspace(0.0, T, N)
# sol = odeint(RHS, [0, 0], ta)
plt.figure(figsize=(30,15))
plt.plot(t, theta1Sol, 'k',
         t, theta2Sol, 'b-',
         lw=linewidth, ms=markersize)
plt.legend(['Harmonic Balance', 'Time integration'], loc='best')
# plt.xlabel('Time')
# plt.ylabel('Displacement')
plt.savefig('4N20.eps', format='eps', dpi=1000, bbox_inches='tight')
plt.show()