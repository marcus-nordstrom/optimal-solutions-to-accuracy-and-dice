import pylidc as pl
from pylidc.utils import consensus
import numpy as np
import matplotlib.pyplot as plt
import os

# Computes a segmentation according to eq [17]
def get_opt_A_seg(m):
    s = m>=1/2
    return s

# Computes a segmentation according to eq [18]
def get_opt_D_seg(m):
    psi = np.flip(np.sort(m.flatten())) # Corresponds to a discrete version of 1-F^{-1}(v)  in the paper
    d = 2*np.cumsum(psi)/(np.sum(m)+np.arange(1,len(psi)+1)) # Vectorized computaton of Dice score for all threshold solutions
    s = m>=np.max(d)/2
    return s

def get_rel_vol():
    scans = pl.query(pl.Scan)

    print("Loaded " + str(scans.count()) + " patients.")
    res_data = -np.ones([scans.count(),2])
    for i in range(scans.count()):
    # for i in range(5):
        scan = scans[i]
        anns = scan.annotations

        if len(anns)==0:
            vsa=1
            vsd=1
        else:
            _,_,masks = consensus(anns, clevel=0.5, pad=[(0,0), (0,0), (0,0)])

            m = np.sum(masks,axis=0)/4
            sa = get_opt_A_seg(m)
            sd = get_opt_D_seg(m)

            vsa = np.sum(sa)/np.sum(m)
            vsd = np.sum(sd)/np.sum(m)


        print(str(i) + " : " + '{0:.3f}'.format(vsd-vsa) + " : " + '{0:.3f}'.format(vsa) + " " + '{0:.3f}'.format(vsd))
        res_data[i,0] = vsa
        res_data[i,1] = vsd

    return res_data

def save_results(res_data):
    os.mkdir('results')
    np.save('results/results_data_L', res_data)

    f,ax = plt.subplots(figsize=(4,4))

    ax.scatter(res_data[:,0],res_data[:,1],s=20,facecolors='none', edgecolors='b')
    ax.set_xlabel(r'$|s^{\mathrm{A}_m}|/|m|$', fontsize=10)
    ax.set_ylabel(r'$|s^{\mathrm{D}_m}|/|m|$', fontsize=10)
    ax.set_xlim([0,4])
    ax.set_ylim([0,4])
    ax.set_xticks([0.0,1.0,2.0,3.0,4.0],["0.0","1.0","2.0","3.0","4.0"])
    ax.set_yticks([0.0,1.0,2.0,3.0,4.0],["0.0","1.0","2.0","3.0","4.0"])
    ax.set_title("Lung nodules")

    f.tight_layout()
    f.savefig('results/results_L.pdf', bbox_inches='tight', pad_inches=0.0, transparent=True)

    res_table = open("results/results_table.txt", "w")
    res_table.write('|s^{\mathrm{A}_m}|/|m| Mean: ' + '{0:.3f}'.format(np.average(res_data[:,0]))+ ', Std: ' + '{0:.3f}'.format(np.std(res_data[:,0])) + ', Min: ' + '{0:.3f}'.format(np.min(res_data[:,0]))+ ', Max: ' + '{0:.3f}'.format(np.max(res_data[:,0])) + '\n')
    res_table.write('|s^{\mathrm{D}_m}|/|m| Mean: ' + '{0:.3f}'.format(np.average(res_data[:,1]))+ ', Std: ' + '{0:.3f}'.format(np.std(res_data[:,1])) + ', Min: ' + '{0:.3f}'.format(np.min(res_data[:,1]))+ ', Max: ' + '{0:.3f}'.format(np.max(res_data[:,1])) + '\n')
    res_table.write('\n')
    res_table.close()


res_data = get_rel_vol()
save_results(res_data)
