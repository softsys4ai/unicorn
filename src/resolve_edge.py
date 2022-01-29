import random
import pandas as pd
import numpy as np
class ResolveEdge:
    def __init__(self):
        print ("[STATUS]: initializing ResolveEdge class")

    def latent_search(Pxy, N, beta):
        """This function is used to perform the latent search
        """
        m = len(Pxy["X"])
        n = len(Pxy["Y"])
        r = np.max([m,n])
        # initialization
        Qxyz = np.zeros((r, m*n))
        Qz = np.zeros((r,1))
        Qx = np.zeros((1,m))
        Qy = np.zeros((1,n))
        Qzgx = np.zeros((r,m))
        Qzx = np.zeros((r,m))
        Qzgy = np.zeros((r,n))
        Qzy = np.zeros((r,n))
        Fxy = Pxy
        Qzgxy = np.random.rand(r, m*n)
        s = Qzgxy.sum(axis=0)
        for k in range(N):
            for j in range(r):
                Qxyz[j] = Qzgxy[j] ## TODO dot multiply with Pxy

            s = Qxyz.sum()
            Qxyz = Qxyz/s

            # calculate q(z)
            for j in range(r):
                Qz[j] = Qzgxy[j].sum()
            Qz = Qz+10**(-15)

            # calculate q(z|x)
            for j in range(m):
                #Qzx[:,j] = Qxyz[:] # # TODO: Fix indices

                Qx[j] = Qzx[j].sum()
                Qzgx[:,j] = Qzx[:,j]/Qx[j]
            # calculate q(z|y)
            for j in range(n):
                #Qzy[:,j] = Qxyz[:] # # TODO: Fix indices

                Qy[j] = Qzy[j].sum()
                Qzgy[:,j] = Qzy[:,j]/Qy[j]
            # Update
            for i in range(m):
                for j in range(n):
                    Fxy[i,j] = Qzgx[:,i]*Qzgy[:,j]*Qz**(beta-1)
            c = 1
            for i in range(m):
                for j in range(n):
                    Qzgxy[:,c] = Qzgx[:,i]*Qzgy[:,j]*Qz**(beta-1)/Fxy[i,j]
                    c = c+1
            for j in range(r):
                Qxyz[j,:] = Qzgxy[j,:]*Pxy
            s = Qxyz.sum()
            Qxyz = Qxyz/s
        return Qxyz


    def infer_graph(Pxy, r , m,
                n, Hx, Hy,
                alpha):
        a = 0
        b = 0.1
        beta = [random.uniform(0,0.1) for i in range(50)]
        Qzx = np.zeros((r,m))
        Qzy = np.zeros((r,n))
        Hz = []
        # conditional mutual information
        cmi = np.zeros((1,50))
        S = []
        for i in range(50):
            Qxyz = LatentSearch(Pxy, 500, beta[i])
            r = len(Qxyz)
            Qz = np.zeros((1,r))
            for j in range(r):
                Qz[j] = Qxyz[j,:].sum()
            e = np.nonzero(Qz)
            Hz[i] = sum(-e*log2(e))
            for j in range(1, m):
                Qzx[:,j] = Qxyz[:,(j*n)-(n-1):j*n].sum()
            for j in range(n):
                Qzy[:,j]=Qxyz[:,j:n:-1].sum()
            for j in range(r):
                for k in range(m):
                    for l in range(n):
                        c = (k*n) - (n-l)
                    if Qxyz[j,c] > 0.001:
                        cmi[i] = cmi[i] + Qxyz[j,c]*log2(Qxyz[j,c])+log2(Qz[j])-log2(Qzx(j,k)-log2(Qzy[j,l]))
            if abs(cmi[i]) <= 0.001:
                s = [S,i]
                Hz = [Hz, Hz[i]]
            if len(S) == 0 or np.min(Hz) > alpha*m np.min(Hx,Hy):
                latent_graph = False
            else:
                latent_graph = True
        return latent_graph


