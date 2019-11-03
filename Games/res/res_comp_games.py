#!/usr/bin/env python
"""
Library for welfare resource games
"""

from Games.basic_games import *
from scipy import linprog


class CompResourceGame(ResourceGame):
    """ framework for resource games with computable price of anarchy
    --cite here """
    def __init__(self, players, strategies, r_m):
        ResourceGame.__init__(self, players, strategies, r_m)

    def optimalPoA(n, w, costMinGame=False, method='revised simplex'):
        """ """
        I = generateIR(n) # [a,b,x]
        a = I[:,0]
        b = I[:,1]
        x = I[:,2]

        A1 = -1.0*np.eye(n+1)[0:n]
        B1 = np.zeros(n)

        A2 = np.zeros((I.shape[0],n+1))
        A2[np.arange(I.shape[0])[a+x > 0, ...],(a+x-1)[a+x > 0, ...]] = a[a+x > 0, ...]
        A2[np.arange(I.shape[0]),a+x] = -b
        A2[np.arange(I.shape[0]),-1] = -1.0*w[a+x]
        B2 = -1.0*w[b+x]

        if costMinGame:
            A = np.vstack( (A1,-A2) )
            B = np.hstack( (B1,-B2) )
        else:
            A = np.vstack( (A1,A2) )
            B = np.hstack( (B1,B2) )
        
        if costMinGame:
            c = -1.0*np.eye(n+1)[-1] # [ f, mu ]
        else:
            c = np.eye(n+1)[-1] # [ f, mu ]

        res = linprog(c, A_ub=A, b_ub=B, method=method)

        return res

    def primalPoA(n, w, f, costMinGame=False, method='revised simplex'):     
        """ """
        
        I = generateI(n) # [a,b,x]
        a = I[:,0]
        b = I[:,1]
        x = I[:,2]

        numRowsI = I.shape[0]

        A_ub = np.zeros( (numRowsI*colsW + 1, numRowsI*colsW) )
        b_ub = np.zeros( (numRowsI*colsW + 1,) )

        A_eq = np.zeros( (1, numRowsI*colsW) )
        b_eq = 1.0
        
        c = np.zeros( (numRowsI*colsW,) )

        for idx in np.arange(colsW):        
            # sum of NE constraints
            A1 = a*f[a+x, idx] - b*f[a+x+1, idx]

            # \sum_{a,x,b} w(a+x) theta(a,x,b) = 1
            A2 = w[a+x, idx]

            if costMinGame:
                A_ub[0, idx*numRowsI:(idx+1)*numRowsI] = A1
            else:
                A_ub[0, idx*numRowsI:(idx+1)*numRowsI] = -A1
        
            A_eq[0, idx*numRowsI:(idx+1)*numRowsI] = A2

            if costMinGame:
                c[idx*numRowsI:(idx+1)*numRowsI] = w[b+x, idx]
            else:
                c[idx*numRowsI:(idx+1)*numRowsI] = -1.0*w[b+x, idx]

        # theta(a,x,b) \geq 0
        A_ub[1:numRowsI*colsW + 1,:] = -1.0*np.eye(numRowsI*colsW)

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method=method)
        
        return res

    def generateI( n ):
        """ """
        vtri = np.vectorize(np.tri, otypes=[np.object], excluded=['N','M'])
        matrix = np.vstack( np.nonzero( np.fliplr( np.stack( vtri( n+1, n+1, -np.arange(n+1) ) ) ) ) ).T[1:]

        return matrix

    def generateIR( n ):
        """ """
        height = 2*n**2 + 1
        matrix = np.zeros((height,3), dtype=np.int)

        sideFaceLen = int((n+1)*n/2)
        sideFace = np.vstack( np.nonzero( np.flipud(np.tri(n+1)) ) )[:,n+1:]
        
        matrix[0:sideFaceLen,0:2] = sideFace.T
        matrix[sideFaceLen:2*sideFaceLen,1:3] = sideFace.T
        matrix[2*sideFaceLen:3*sideFaceLen,[2,0]] = sideFace.T

        lastFace = np.vstack( (sideFace, n - np.sum(sideFace, axis=0)) )
        mask = np.prod(lastFace, axis=0) >= 1
        
        matrix[3*sideFaceLen:,:] = lastFace.T[mask,...]

        return matrix

    def dualPoA(n, w, f, costMinGame=False, method='revised simplex'):
        """ """  
        IR = generateIR(n) # [a,b,x]
        a = IR[:,0]
        b = IR[:,1]
        x = IR[:,2]

        numRowsIR = IR.shape[0]

        A_ub = np.zeros( ( numRowsIR*colsW+1, 2 ) )
        b_ub = np.zeros( numRowsIR*colsW+1 )

        # lambda \geq 0
        A_ub[-1,:] = np.array([-1., 0.])
        b_ub[-1] = 0.0

        for idx in np.arange(colsW):
            # lambda (a f(a+x)w(a+x) - bf(a+x+1)w(a+x+1)) - mu w(a+x) \leq w(b+x)
            A2 = np.zeros( (numRowsIR, 2) )
            
            A2[:,0] = a*f[a+x, idx] - b*f[a+x+1, idx]
            A2[:,1] = -1.0*w[a+x, idx]
            
            b2 = w[b+x,idx]

            if costMinGame:
                A_ub[idx*numRowsIR:(idx+1)*numRowsIR,:] = -A2
                b_ub[idx*numRowsIR:(idx+1)*numRowsIR] = b2
            else:
                A_ub[idx*numRowsIR:(idx+1)*numRowsIR,:] = A2
                b_ub[idx*numRowsIR:(idx+1)*numRowsIR] = -b2
        
        if costMinGame:
            c = np.array([0., -1])
        else:
            c = np.array([0., 1])

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, method=method)
        
        return res