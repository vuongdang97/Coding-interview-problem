# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 23:59:01 2024

@author: dangt
"""
import numpy as np
import math
import matplotlib.pyplot as plt

def fx(t):
    return 0
def fy(t):
    return 0
def fz(t):
    return 1700
def falpha(t):
    return 21*math.sin(2*math.pi*5*t)*math.pi/180
def fbeta(t):
    return 8*math.sin(2*math.pi*5*t)*math.pi/180
def fgamma(t):
    return 0
def fx_t(t):
    return 0
def fy_t(t):
    return 0
def fz_t(t):
    return 0
def falpha_t(t):
    return 21*2*math.pi*5*math.cos(2*math.pi*5*t)*math.pi/180
def fbeta_t(t):
    return 8*2*math.pi*5*math.cos(2*math.pi*5*t)*math.pi/180
def fgamma_t(t):
    return 0
        

def Matrix_Euler(alpha, beta, gamma):
    # Create rotational matrix for each angle alpha, beta, gamma
    R_alpha = np.zeros((3,3))
    R_alpha[0][0] = 1
    R_alpha[1][1] = math.cos(alpha)
    R_alpha[1][2] = -math.sin(alpha)
    R_alpha[2][1] = math.sin(alpha)
    R_alpha[2][2] = math.cos(alpha)
    
    R_beta = np.zeros((3,3))
    R_beta[0][0] = math.cos(beta)
    R_beta[0][2] = math.sin(beta)
    R_beta[1][1] = 1
    R_beta[2][0] = -math.sin(beta)
    R_beta[2][2] = math.cos(beta)

    R_gamma = np.zeros((3,3))
    R_gamma[0][0] = math.cos(gamma)
    R_gamma[0][1] = -math.sin(gamma)
    R_gamma[1][0] = math.sin(gamma)
    R_gamma[1][1] = math.cos(gamma)
    R_gamma[2][2] = 1

    R_P = np.matmul(np.matmul(R_alpha,R_beta), R_gamma)
    
    # old paper
    #R_P[0][0] = math.cos(xi)*math.cos(phi)- math.cos(theta)*math.sin(phi)*math.sin(xi)
    #R_P[0][1] = -math.sin(xi)*math.cos(phi) - math.cos(theta)*math.sin(phi)*math.cos(xi)
    #R_P[0][2] = math.sin(theta)*math.sin(phi)
    #R_P[1][0] = math.cos(xi)*math.sin(phi) + math.cos(theta)*math.cos(phi)*math.sin(xi)
    #R_P[1][1] = -math.sin(xi)*math.sin(phi) +math.cos(theta)*math.cos(phi)*math.cos(xi)
    #R_P[1][2] = -math.sin(theta)*math.cos(phi)
    #R_P[2][0] = math.sin(xi)*math.sin(theta)
    #R_P[2][1] = math.cos(xi)*math.sin(theta)
    #R_P[2][2] = math.cos(theta)

    return R_P
    
def Inverse_Kinematics(x,y,z,alpha,beta,gamma, a_i,b_i):
    # Define matrix corresponding to Euler rotation
    R_P = Matrix_Euler(alpha, beta, gamma)
    
    # Define position 
    position = np.array([x,y,z])
    
    # Compute the corresponding coordinate for frame W
    a_iW = position + np.matmul(R_P,a_i)
    
    # Compute the xi lanh and its length
    L_i = a_iW-b_i
    
    l_i = np.dot(L_i,L_i)
    l_i = math.sqrt(l_i)
    
    return L_i
    
def Inverse_rate_Kinematics(x,y,z,x_t,y_t,z_t,alpha,beta,gamma, alpha_t,beta_t,gamma_t, a,b):
    # Define matrix corresponding to Euler rotation
    R_P = Matrix_Euler(alpha, beta, gamma)
    
    # Compute normal vector
    n = []
    for i in range(6):
        L_i = Inverse_Kinematics(x,y,z,alpha,beta,gamma,a[i],b[i])
        n.append(L_i/np.linalg.norm(L_i, ord=2))

    # Velocity vector and position vector
    P = np.array([x,y,z])
    P_t = np.array([x_t,y_t,z_t])

    # Angular velocity
    omega_t = np.array([alpha_t,beta_t,gamma_t])

    J = np.zeros((3,3))
    J[0][0] = math.cos(beta)
    J[1][1] = 1
    J[1][2] = -math.sin(alpha)
    J[2][0] = -math.sin(beta)
    J[2][2] = math.cos(alpha)

    omega = np.matmul(J,omega_t)
    l_t = []
    for i in range(6):
        l_i = np.dot(P_t,n[i]) + np.dot(omega,np.cross(np.matmul(R_P,P),n[i]))
        l_t.append(l_i)
    return l_t
    
    # Compute Jacobian matrix 
    
    # Compute J1
    #J1 = np.zeros((6,6))
    #for i in range(6):
        #J1[i,:3] = n[i]
        #J1[i,3:6] = np.cross(np.matmul(R_P,a[i]),n[i])
    # Compute J2
    #J2 = np.zeros((6,6))
    #J2[0][0] = 1
    #J2[1][1] = 1
    #J2[2][2] = 1
    #J2[3][3] = math.cos(beta)
    #J2[4][4] = 1
    #J2[4][5] = -math.sin(alpha)
    #J2[5][3] = -math.sin(beta)
    #J2[5][5] = math.cos(alpha)
    # Compute J
    #J = J1*J2
    
    # Vector velocity
    #q_t = np.array([x_t,y_t,z_t,alpha_t,beta_t,gamma_t])
    
    # Velocity of xilanh
    #l_t = np.matmul(J,q_t)
    
    return l_t

# Implement the kinetic system

# Initialize the state vector
a = [np.array([1050.52, 123.1, -145.52])]
a.append(np.array([-418.99, 961.71, -150.86]))
a.append(np.array([-632.6, 839.3, -139.13]))
a.append(np.array([-631.87, -848.23, -145.52]))
a.append(np.array([-418.65, -971.33, -145.52]))
a.append(np.array([1035, -123.1, -144.46]))
         
b = [np.array([751.01, 1057.89, 294.21])]
b.append(np.array([540.65, 1179.34, 294.21]))
b.append(np.array([-1290.76, 131.74, 284.17]))
b.append(np.array([-1291.01, -131.95, 284.2]))
b.append(np.array([531.69, -1189.22, 286.19]))
b.append(np.array([753.98, -1050.63, 286.5]))

# Create mesh point in time
T = 20
t = np.arange(0,T,1/2048)
vector_l1 = np.zeros((len(t),1))
vector_l2 = np.zeros((len(t),1))
vector_l3 = np.zeros((len(t),1))
vector_l4 = np.zeros((len(t),1))
vector_l5 = np.zeros((len(t),1))
vector_l6 = np.zeros((len(t),1))





for i in range(len(t)):

    L = Inverse_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), a[0],b[0])
    vector_l1[i] = np.linalg.norm(L, ord=2)

    L = Inverse_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), a[1],b[1])
    vector_l2[i] = np.linalg.norm(L, ord=2)

    L = Inverse_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), a[2],b[2])
    vector_l3[i] = np.linalg.norm(L, ord=2)

    L = Inverse_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), a[3],b[3])
    vector_l4[i] = np.linalg.norm(L, ord=2)

    L = Inverse_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), a[4],b[4])
    vector_l5[i] = np.linalg.norm(L, ord=2)

    L = Inverse_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), a[5],b[5])
    vector_l6[i] = np.linalg.norm(L, ord=2)

    l_t = Inverse_rate_Kinematics(fx(t[i]),fy(t[i]),fz(t[i]),fx_t(t[i]),fy_t(t[i]),fz_t(t[i]),falpha(t[i]),fbeta(t[i]),fgamma(t[i]), falpha_t(t[i]),fbeta_t(t[i]),fgamma_t(t[i]), a,b)
    vector_l1[i] = l_t[0]
    vector_l2[i] = l_t[1]
    vector_l3[i] = l_t[2]
    vector_l4[i] = l_t[3]
    vector_l5[i] = l_t[4]
    vector_l6[i] = l_t[5]

plt.plot(t,vector_l1,label = "l_1", color = "red")
plt.plot(t,vector_l2,label = "l_2", color = "blue")
plt.plot(t,vector_l3,label = "l_3", color = "green")
plt.plot(t,vector_l4,label = "l_4", color = "orange")
plt.plot(t,vector_l5,label = "l_5", color = "purple")
plt.plot(t,vector_l6,label = "l_6", color = "yellow")

plt.legend()


plt.show()
