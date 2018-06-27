import random    
import math
from data import*
        
def createfile(filename,n,nc,nf,nh,T,td,Fv,Fh,C,Ci,nnd,p):
    NomFichier=filename
    Fichier = open(NomFichier,'w')
    Fichier.write('n= %s ; \n' %str(n) )
    Fichier.write('nc= %s  ;\n' %str(nc) )  
    Fichier.write('nf= %s  ;\n' %str(nf) )
    Fichier.write('nh= %s ; \n' %str(nh) )
    nbpoint=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    #nbpoint=[6, 1, 1, 1, 2, 1, 1, 1, 20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 6, 1,1, 1, 1, 1, 5, 1, 1, 1, 1, 3, 1, 1, 1]
    d = [[0 for x in range(0,nf)] for y in range(0,nc)]
    dnn = [[0 for x in range(0,n)] for y in range(0,n)]
    dnh = [[0 for x in range(0,nh)] for y in range(0,n)]
    dnc = [[0 for x in range(0,n)] for y in range(0,n)]
    l= [0 for x in range (0,n-1)]
    h= [0 for x in range (0,nh)]
    dhh=[[0 for x in range(0,nh)]for y in range (0,nh)]
    dm=[0 for x in range(0,n)]
    O=[0 for x in range(0,nf)]
    nd=0
    for i in range(0,nc):
        for t in range(0,nnd):
            j=random.randint(0,nf-1)
            d[i][j]=round(p*nbpoint[i]+d[i][j],2)
            nd=nd+1

    for i in range(0,nf):
            for j in range(0,nc):
                    O[i]=d[j][i]+O[i]
            if O[i]==0:
                    j=random.randint(0,nc-1)
                    d[j][i]=round(p*nbpoint[j]+d[j][i],2)
                    nd=1+nd
  
 
    ndd=nnd*91
    Fichier.write('T= %s ; \n' %str(T) )
    Fichier.write('C= %s ; \n' %str(C) )
    Fichier.write('Ci= %s ; \n' %str(Ci) )
    Fichier.write('td= %s ; \n' %str(td) )
    Fichier.write('Fv= %s ; \n' %str(Fv) )
    Fichier.write('Fh= %s ; \n' %str(Fh) )
    Fichier.write('nnd= %s ; \n' %str(ndd))

  

 
  
    

    for i in range(0,nc):
        for j in range(0,nh):
            dnh[i][j]=dch[i][j]
      for i in range(0,nc):
        for j in range(0,nh):
            tnh[i][j]=tch[i][j]
    for i in range(nc, nc+nf):
            for j in range (0,nh):
                    dnh[i][j]=dfh[i-nc][j]

    for i in range(nc, nc+nf):
            for j in range (0,nh):
                    tnh[i][j]=tfh[i-nc][j]

 
    
    Fichier.write('dhh=%s ; \n' %str(dh))
    Fichier.write('thh=%s ; \n' %str(th)
    for i in range(0,n):
        k=0
        for j in range (0,n):
                if j!=i:
                    l[k]=dnn[i][j]
                    k+=1
        for j in range(0,nh):
            h[j]=dnh[i][j]
        m=min(l)
        mh=min(h)
        dm[i]=min(m,mh)
    top=[td for x in range (0,n)]
    D=[0]*n
    for i in range(0,nc):
        D[i]=sum(d[i][:])

   
    for i in range(0, nc):
        top[i]=td*nbpoint[i]


    Fichier.write('top= %s ; \n' %str(top) )
    Fichier.write('dem= %s  ;\n' %str(d))
    Fichier.write('dnn= %s ; \n' %str(dnn) )
    Fichier.write('dhn=%s ; \n' %str(dnh))
    Fichier.write('tnn= %s ; \n' %str(tnn) )
    Fichier.write('thn=%s ; \n' %str(tnh))
    Fichier.write('dm=%s ; \n' %str(dm))
    
    demande=[[0 for x in range(0,n)] for y in range(0,n)]

    for i in range(0,n):
        for j in range(0,n):
            if i<nc and j>=nc:
                demande[i][j]=d[i][j-nc]
    print('dem= ',d)
    print('demande= ', demande)
    D=[0]*n
    O=[0]*n
    for i in range(0,nc):
        D[i]=round(sum(demande[i]),2)
    for i in range(nc,n):
        for j in range(0,nc):
            O[i]=round(O[i]+demande[j][i],2)
    M=sum(O)    
    nv1=math.trunc(M/C)+1
    Top= sum(top)
    tmin=0
    for i in range(0,n):
        h=[x for x in dnn[i] if dnn[i].index(x)!=i]
        tmin=round(min(h)+tmin,2)
    nv2=math.trunc((Top+tmin)/T)+1
    nv=max(nv1,nv2)
    print('D =', D)
    print('O = ', O)
    print('tmin = ', tmin)
    print('nv= ',nv)


    
createfile('data2.py',20,10,10,2,480,10,250,500,1500,1500,24,1.8)
