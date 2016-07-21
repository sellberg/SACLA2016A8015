#!/home/software/SACLA_tool/bin/python2.7

import numpy as np
import h5py 
import matplotlib
import matplotlib.pyplot as plt
import argparse
import time

# -- default parameters
run = 448571#448539
hit_thr = 77 # threshold for hit rate
n_shots=1000
ADU_thr = [50,150]

# -- files and folders
file_folder = '/UserData/fperakis/2016_6/run%d/'%(run)
fig_folder  = '/home/fperakis/2016_06/figs/'
file_name = '%d.h5'%(run)
file_path = file_folder+file_name

# -- import data
fh5       = h5py.File(file_path, 'r')
run_key   = [ k for k in fh5.keys() if k.startswith('run_') ][0]
tags      = fh5['/%s/detector_2d_assembled_1'%run_key].keys()[1:]

# -- image generator
num_im = len(tags)
img_gen   = (  fh5['%s/detector_2d_assembled_1/%s/detector_data'%(run_key,tag) ].value for tag in tags )
num_im = len(tags)
max_int = np.zeros(num_im)

# -- average image
im1 = img_gen.next()

# -- make mask
mask = np.ones(im1.shape)
mask[im1<ADU_thr[0]]=0
mask[im1>ADU_thr[1]]=0
im = im1*mask

# -- loop
i=0
for i_shot in range(n_shots):
#for im_next in img_gen:
    im_next = img_gen.next()
    t1 = time.time() 
    max_int[i] = np.average(im_next.flatten())
    im += im_next
    i  += 1
    print 'R.%d | S.%d/%.d | %.1f Hz'%(run,i,num_im,1.0/(time.time() - t1))

im /= n_shots#num_im
#max_int/=n_shots

## -- histogram ADUs of mean image
bi,bf,db1 = -200,500,10#ADU_thr[0],ADU_thr[1],5#70,100,1#3e6,1e4
hy1,hx1 = np.histogram(im,bins = np.arange(bi,bf,db1)) 

# -- histogram shots
bi,bf,db2 = 70.,100.,1.#70,100,1#3e6,1e4
hy2,hx2 = np.histogram(max_int,bins = np.arange(bi,bf,db2)) 

# -- hit rate
num_hits = float(len(max_int[max_int>hit_thr]))
hit_rate = num_hits/float(n_shots)

# -- plot
plt.figure()
vmin,vmax=ADU_thr[0],ADU_thr[1]
plt.subplot(2,2,1)
plt.imshow(im,vmin=vmin,vmax=vmax)#,vmin=0,vmax=0.3)
plt.colorbar()
plt.title('r.%d'%(run))

plt.subplot(2,2,3)
plt.bar(hx1[:-1]-db1/2.,hy1,width = db1,color='green')
plt.axvline(x=ADU_thr[0],ls='--',color='gray')
plt.axvline(x=ADU_thr[1],ls='--',color='gray')
plt.yscale('log',nonposy='clip')
plt.xlabel('ADUs/shot')
plt.ylabel('number of pixels')
plt.title('Pixels histogram')


plt.subplot(2,2,2)
plt.bar(hx2[:-1]-db2/2.,hy2,width = db2)
plt.axvline(x=hit_thr,ls='--',color='gray',label='threshold=%d'%(hit_thr))
plt.yscale('log',nonposy='clip')
plt.xlabel('mean ADUs/shot')
plt.ylabel('number of shots')
plt.title('Shots histogram')
plt.ylim([0.1,n_shots])
plt.legend(frameon=False)

plt.subplot(2,2,4)
plt.plot(max_int[:n_shots],'ro')
plt.axhline(y=hit_thr,ls='--',color='gray')
plt.title('hit rate: %.2f percent'%(hit_rate*100))#mean: %.3f ADUS/pixel'%(total_mean))
plt.xlabel('Shot number')
plt.ylabel('mean ADUS/shot')
plt.tight_layout()

plt.savefig(fig_folder+'SAXS_run%d.png'%(run))
#plt.show()
