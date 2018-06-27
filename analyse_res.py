from data3 import *
from data2 import *
p=1.8
demande=[[0 for x in range(0,n)] for y in range(0,n)]

for i in range(0,n):
    for j in range(0,n):
        if i<nc and j>=nc:
            demande[i][j]=dem[i][j-nc]

D=[0]*n
O=[0]*n
for i in range(0,nc):
    D[i]=round(sum(demande[i]),2)
for i in range(nc,n):
    for j in range(0,nc):
        O[i]=round(O[i]+demande[j][i],2)
M=sum(O)    
Fichier = open('Analyse.txt','w')
Rv=0
nnd=24
nr=91
Moy=[0]*nh
for h in range(0,nh):
    if yh[h]==1:
        for i in range(0,n):
            Rv=round((((u[i][h]+v[i][h]-O[i])/C)*100)+Rv,2)
        for i in range(0,n):
            if (z[i][h][h]==1):
                Rv=Rv+round(((u[i][h]+v[i][h]-D[i])/C)*100,2)
        Moy[h]=round(Rv/(n+1),2)
        Fichier.write('Le taux de remplissage des véhicules est= %s ; \n' %str(Moy[h]) )


dt=[]
nvo=nve
for i in range(0,n):
    for h in range(0,nh):
        if znh[i][h][h]==1:
            dt.append(round(t[i][h]+thn[i][h]+td,2))
for i in range(0,nve):
    Fichier.write('la durée de la tournée ')
    Fichier.write(str(i+1))
    Fichier.write(' est égale à %s ; \n '  %str(dt[i]))
for tt in range(0,nve):
    for ttt in range(0,nve):
        if dt[tt]+dt[ttt]<=T and tt!=ttt:
            dt[tt]=dt[tt]+dt[ttt]
            dt[ttt]=T
            nvo=nvo-1
Fichier.write('Le nombre des voitures est :  %s ; \n' %str(nvo))
Fichier.write('Le cout de location des véhicules %s ; \n' %str(nvo*Fv))
Nv_Obj=0


if p<=2:
    Pr=10*nr*nnd
elif p>2 and p<=4:
    Pr=16*nr*nnd
elif p>4 and p<=6:
    Pr=23*nr*nnd
else :
    Pr=30*nr*nnd

Cv=nvo*Fv

Nv_Obj=Obj-nve*Fv+Cv


Fichier.write('La valeur de la nouvelle fonction objectif %s ; \n' %str(Nv_Obj))
Ch=sum(yh[h]*Fh for h in range(0,nh))
Pv=round((Cv/Pr)*100,2)
Fichier.write('Le pourcentage de coût de location des véhicules %s ; \n' %str(Pv))
Pv=round(((Cv+Ch)/Pr)*100,2)
Fichier.write('Le pourcentage des coûts sans les coûts kilomètriques %s ; \n'%str( Pv))
Pv=round((Nv_Obj/Pr)*100,2)
Fichier.write('Le pourcentage des coûts totaux %s ; \n' %str(Pv))
pk= round(Nv_Obj/(nr*nnd*p),2)
Fichier.write('Le coût par Kg est égale à:  %s ; \n' %str(pk))
Fichier.close()

