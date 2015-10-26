import sys
import numpy as np
import cPickle as pickle

def l1_proximal_map(X,t):
    X_map = X
    #np.copyto(X,X_map)
    dim = X_map.shape[0]
    for idx in range(dim):
        if X_map[idx]>t: X_map[idx]-=t
        elif X_map[idx]<-t: X_map[idx]+=t
        else: X_map[idx] = 0
    return X_map

def SpaceProjectionMat(Phi):
    PhiT = Phi.T
    PhiTPhi_inv = np.linalg.pinv(np.dot(PhiT,Phi))
    P = np.dot(Phi,np.dot(PhiTPhi_inv,PhiT))
    return P

def main():
    iternum = 5000
    [feat_mat1, rewards, feat_mat2] = pickle.load(open('features.pkl'))
    P = SpaceProjectionMat(feat_mat1)
    gamma = 0.9
    ld = 0.07
    lr = 0.0001
    d = np.dot(P,rewards)
    C = np.dot(P,feat_mat2)*gamma-feat_mat1
    datanum,featnum = feat_mat1.shape
    beta = np.random.normal(size=featnum)
    #beta = np.zeros(featnum)
    beta_t_1 = beta

    for idx in range(iternum):
        beta_v = beta + (beta-beta_t_1)*(idx-2)/(idx+1)
        beta_t_1 = beta
        beta_grad = np.dot(C.T,np.dot(C,beta)+d)
        beta_grad_update = beta_v - beta_grad*lr
        #beta = beta_grad_update
        beta = l1_proximal_map(beta_grad_update, ld*lr)
        obj = np.linalg.norm(np.dot(C,beta)+d) + ld*np.linalg.norm(beta,1)
        if idx%100==0: print obj

    #print beta
    print obj 
    pickle.dump(beta,open('beta.pkl','wb'))
    
        

if __name__=='__main__':
    main()
