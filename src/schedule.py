import sys
import numpy as np
from matplotlib import pyplot as plt

params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode' : True}

plt.rcParams['text.latex.preamble']=[r'\usepackage{lmodern}']
plt.rcParams.update(params)


#---- Input [a1,a2], output [[a1],[a2]]

def listify(r):

    rl = []
    for i in range(len(r)):
        rl.append([ r[i] ])

    return rl

#---- Recursive function

def stupid_comb(s):

    
    r0 = s[0] # initialization
    
    if len(s) == 1:
        r = listify(r0)
        
    else:
        r1 = stupid_comb(s[0:-1]) # recursion
        
        k,n1,n2 = 0, len(r1), len(s[-1])
        r,x1,x2 = [],[],[ [] ]*n1*n2
        
        for i in range(n1):
            x1.append(r1[i])

            for j in range(n2):
                x2[k] = x1[i] + [ s[-1][j] ]
                k += 1

        r = x2
            
    return r



#---- Get the names

def get_names(nphd):

    phd_names = []

    for i in range(1,nphd+1):  # loop thru all PhDs

        fname = '../data/teacher_p'+str(i)+'.txt'
        with open(fname,'r') as f:
            data = f.readlines()

        data = [x.strip() for x in data]

        name = data[1]
        phd_names.append(name)

        
    return phd_names



#---- Reduced number of combinations

def reduced_comb(nphd,ilab,nlab,lmax):

    #---> Generate input

    s = [None]*nlab  # init schedule list
    
    for i in range(1,nphd+1):  # loop thru all PhDs

        fname = '../data/teacher_p'+str(i)+'.txt'
        cpi = np.loadtxt(fname, usecols=(4,), skiprows=4)
        #print 'Choice of PhD',str(i),cpi
        
        for m in range(nlab):  # filling schedule list
            
            if i == 1:  # init sub-list
                s[m] = []
            
            if cpi[m+ilab] == 1.: # note the index shift
                s[m].append(i)

    print 'Input list mapped from choices: \n',s,'\n'
    
    #---> Remove empty sub-list

    kem, isem, sfull = 0, [], s
    for i in range(nlab):
        if not s[i]:  # i.e. if s[i] is empty
            kem += 1
            isem.append(i)    
    
    if kem > 0:
        print 'Number of empty labs =',kem,'\nIndex list',isem
        k,sfull = 0,[ [] ]*(nlab-kem)
        for i in range(nlab):
            if s[i]:
                sfull[k] = s[i]
                k += 1
            
        print 'Remaining list',sfull,'\n'
        nlab = nlab - kem

    else:
        print 'All labs filled! \n'

    ncom = 1
    for i in range(nlab):
        ncom *= len(sfull[i])

    print 'Number of all possible combinations =',ncom,'\n'
    
    #---> Generate combinations

    if nphd == 1:
        print 'The only combination is \n',sfull
        sys.exit()
    
    else:
        comb_list = stupid_comb(sfull)

    #---> Evaluate quality

    nc = len(comb_list)
    if nc != ncom:
        print 'Number of combinations inconsistent.'
        print 'Program aborted.'
        sys.exit()
        
    sigma = [0]*nc
    comb_list_new = []

    #-- Remove list containing two consecutive assignment
    
    for i in range(nc):

        cc = comb_list[i]
        #print 'Combination',i,cc

        if nlab > 1:
            flag = 0
            for j in range(nlab-1):
                if cc[j] == cc[j+1]:
                    flag = 1
                    #print 'Consecutive assignment (to remove).'
                    
            if flag == 0:
                comb_list_new.append(cc)

        else:
            comb_list_new.append(cc)

    
    nc_new = len(comb_list_new)

    #-- Keep maximum lmax combinations

    if nc_new > lmax:

        temp = []
        
        for i in range(nc_new):        

            cc = comb_list_new[i]
            #print 'Combination',i,cc
        
            load = [0]*nphd  # init work load
            for j in range(nlab):
                load[cc[j]-1] += 1  # note the index shift

            #print 'Work load list',load

            av = sum(load)/float(len(load))  # average load
        
            sigma[i] = 0
            for k in range(nphd):
                sigma[i] += (load[k]-av)**2
                sigma[i] = (sigma[i]/(nphd-1))**0.5  # standard deviation
                
            #print 'Standard deviation', sigma[i], '\n'

        # sort comb_list_new based on sigma
        Z = [x for _,x in sorted(zip(sigma,comb_list_new))] 

        for i in range(lmax):
            temp.append(Z[i])
        
        #print temp

        comb_list_new = temp
        
        print 'Reduced number of combinations =',lmax,'\n'
        print 'List of combinations \n',comb_list_new,'\n'

    else:
        print 'Reduced number of combinations =',nc_new,'\n'
        print 'List of combinations \n',comb_list_new,'\n'

    return comb_list_new



#---- Script

if __name__ == '__main__':

    ## init input list (of list)
    #s=[[1,2]]
    #
    ## get list of combinations
    #comb_list = stupid_comb(s)
    #print comb_list
    #
    #sys.exit()
    

    #---> Init parameters

    # below can be machine generated
    nday = 10 # number of days
    iday = [0,5,8,11,16,21,26,29,32,37,40] # ending index of days (beginning with 0)
    nphd = 6  # number of PhDs
    
    lmax = 4  # numerical parameter: max number of day lists

    #---> Generate combinations of each lab day

    ncom = 1
    empty_day = []
    comb_all,load_all = [],[]

    for i in range(nday):

        print '--------------------------'
        print 'Lab day',i+1,'\n'

        ilab = iday[i]         # beginning index of lab day i
        nlab = iday[i+1]-ilab  # number of labs in lab day i

        #print ilab,nlab

        phd_name = get_names(nphd)
        comb_day = reduced_comb(nphd,ilab,nlab,lmax)

        # compute load
        load_day = []
        for j in range(len(comb_day)):
            load = [0]*nphd
            for k in range(nlab):
                load[comb_day[j][k]-1] += 1  # note the index shift
            load_day.append(load)
            
        if len(comb_day) == 0:
            nday -= 1
            empty_day.append(i)
            print 'Empty list.'
        else:
            ncom *= len(comb_day)
            comb_all.append(comb_day)
            load_all.append(load_day)

    print '\n-----------------------------------------'
    print 'Total number of combinations =',ncom,'\n'
    print 'List of day-list of combination-list: \n',comb_all
    print 'List of day-list of load-list: \n',load_all, '\n'
   
    
    #---> Generate the complete combinations
    
    print 'Generating list of list of list...'
    
    comb = stupid_comb(comb_all)
    load = stupid_comb(load_all)

    print 'Done.\n'

    #---> Evaluate load

    print 'Computing the work load of each combination...'

    LD = []
    SG = [0]*ncom

    for i in range(ncom):
        
        buf1 = load[i]
        ld = [0]*nphd
        
        for j in range(nphd):
            for k in range(nday):

                ld[j] += buf1[k][j]

        LD.append(ld)
        av = sum(ld)/float(len(ld))  # average load
        
        for j in range(nphd):
            SG[i] += (ld[j]-av)**2
            SG[i] = (SG[i]/(nphd-1))**0.5  # standard deviation

    #print 'Minimum standard deviation =',min(SG)
    print 'Done.\n'
    
    # index array of sorted list of sigma
    print 'Sorting the deviation list...'
    isg = sorted(range(len(SG)), key=lambda k: SG[k])
    print 'Done.\n'
    
    
    print '--------------------------------------------------------------------------------'
    ntop = 3
    print 'The',ntop,'best combinations are \n'
    for i in range(ntop):
        print '(',i+1,') Load distribution:',LD[isg[i]],'Standard deviation:',SG[isg[i]]
        print comb[isg[i]],'\n'
        
    if empty_day:
        print 'Note that days',empty_day,'(begin from 0) is/are not filled.'
    print '--------------------------------------------------------------------------------'
            

    # Create a file and write the final combination

    f = open('../output/final.txt','w')

    buf = comb[isg[0]]
    
    for i in range(len(buf)):
        for j in range(len(buf[i])):
            f.write(phd_name[ buf[i][j]-1 ]+'\n')

        
    f.close()
