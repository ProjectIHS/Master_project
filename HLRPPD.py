import sys
import math
import cplex
try:
    import docplex.mp
except:
    if hasattr(sys, 'real_prefix'):
        #we are in a virtual env.
        !pip install docplex 
    else:
        !pip install --user docplex
        
url = None
key = None

from data2 import *
      
from docplex.mp.environment import Environment
env = Environment()
env.print_information()
#traitement données
demande=[[0 for x in range(0,n)] for y in range(0,n)]

for i in range(0,n):
    for j in range(0,n):
        if i<nc and j>=nc:
            demande[i][j]=dem[i][j-nc]
print('dem= ',dem)
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
# modèle
from docplex.mp.model import Model
mdl = Model(name="HubLRP")
hubs=range(0,nh)
noeuds=range(0,n)
agri=range(0,nf)
clients=range(0,nc)
p=1
x = mdl.binary_var_matrix(noeuds, hubs, name='high_xx')
yh = mdl.binary_var_dict(hubs, name='high_yy')
z= mdl.binary_var_cube(noeuds,noeuds, hubs, name='low_zz')
zhn= mdl.binary_var_cube(hubs,noeuds, hubs, name='medium_voit_zhn')
znh= mdl.binary_var_cube(noeuds,hubs, hubs, name='medium_voit_znh')
y= mdl.continuous_var_cube(noeuds,hubs, hubs, lb=0, name='qtite_y')
yt = mdl.binary_var_matrix(hubs, hubs, name='high_yyt')
u=mdl.continuous_var_matrix(noeuds, hubs,lb=0, name='uu')
v=mdl.continuous_var_matrix(noeuds, hubs,lb=0, name='vv')
t=mdl.continuous_var_matrix(noeuds, hubs, lb=0,name='tt')
ninter=mdl.integer_var(lb=0,name="medium_nombre_inter")
ni=mdl.integer_var_matrix(hubs, hubs,lb=0, name='medium_vehicules_inter')
nin=mdl.integer_var(lb=0,name="medium_nombre_in")
nve=mdl.integer_var(lb=0,name="medium_nombre_nve")
dur= mdl.continuous_var_dict(hubs,lb=0, name='duree')
# --- constraints ---

# nombre des hubs
mdl.add_constraint(mdl.sum(yh[i] for i in hubs) <= p)

# --- affectation ---

mdl.add_constraints(x[i,h] <= yh[h]
                   for i in noeuds
                    for h in hubs)

# --- affectation ---
mdl.add_constraints(mdl.sum(x[i,h]  for h in hubs)==1 for i in noeuds)

mdl.add_constraints(mdl.sum(y[i,h,k]  for i in noeuds)<=M*yt[h,k]*n for h in hubs for k in hubs if k!=h)

mdl.add_constraints((mdl.sum(y[i,h,k] for k in hubs if k!=h)-mdl.sum(y[i,k,h]  for k in hubs if k!=h))==O[i]*x[i,h]-mdl.sum(demande[j][i]* (x[j,h]) for j in noeuds if j!=i) for h in hubs for i in noeuds )

mdl.add_constraints(y[i,h,k]<=x[i,h]*M for i in noeuds for h in hubs for k in hubs if k!=h)


# tournéé
mdl.add_constraints(mdl.sum(z[i,j,h] for j in noeuds if j!=i)+znh[i,h,h] ==x[i,h]for i in noeuds for h in hubs)
mdl.add_constraints(mdl.sum(z[i,j,h]  for i in noeuds if j!=i)+zhn[h,j,h]==x[j,h]for j in noeuds for h in hubs)

mdl.add_constraints(u[i,h]>=u[j,h]-C + (C+D[i])*z[i,j,h]+(C-D[j])*z[j,i,h] for i in noeuds for j in noeuds if i!=j for h in hubs) 
mdl.add_constraints(v[j,h]>=v[i,h]-C + (C+O[j])*z[i,j,h]+(C-O[i])*z[j,i,h] for i in noeuds for j in noeuds if i!=j for h in hubs)

mdl.add_constraints(u[i,h]<=C*x[i,h] + (-C+D[i])*znh[i,h,h] for i in noeuds for h in hubs) 
mdl.add_constraints(v[i,h]<=C*x[i,h] + (-C+O[i])*zhn[h,i,h] for i in noeuds for h in hubs) 
mdl.add_constraints(u[i,h]>=D[i]*x[i,h] for i in noeuds for h in hubs)
mdl.add_constraints(v[i,h]>=O[i]*x[i,h] for i in noeuds for h in hubs)
mdl.add_constraints(u[i,h]+v[i,h]<=C*x[i,h] for i in noeuds for h in hubs)

#durée des tournées
mdl.add_constraints(dur[h]==(mdl.sum((dhn[i][h]+td+top[i])*zhn[h,i,h] for i in noeuds)+mdl.sum((thn[i][h]+td)*znh[i,h,h] for i in noeuds)+mdl.sum((tnn[i][j]+top[j])*z[i,j,h] for i in noeuds for j in noeuds if j!=i)) for h in hubs)

mdl.add_constraints(t[i,h]>=t[j,h]-T + (T-tnn[i][j]-top[j])*z[i,j,h]+(T+tnn[j][i]+top[i])*z[j,i,h] for i in noeuds for j in noeuds if i!=j for h in hubs) 
mdl.add_constraints(t[i,h]+(thn[i][h]+td)*znh[i,h,h]<=T*x[i,h]  for i in noeuds for h in hubs) 
mdl.add_constraints(t[i,h]>=(thn[i][h]+td)*zhn[h,i,h] for i in noeuds for h in hubs) 



#véhicules inter-hubs
mdl.add_constraints(mdl.sum(y[i,h,k] for i in noeuds)<= Ci*ni[h,k] for h in hubs for k in hubs if k!=h )
mdl.add_constraint(mdl.sum((thh[h][k]+2*td)*ni[h,k] for h in hubs for k in hubs if k!=h)<=nin*T )

#inégalités valides
mdl.add_constraint(mdl.sum(zhn[h,i,h]  for h in hubs for i in noeuds)==nve )
mdl.add_constraints(mdl.sum(x[i,h]  for i in noeuds)<=mdl.sum(z[i,j,h] for i in noeuds for j in noeuds if i!=j) + mdl.sum(zhn[h,i,h]+znh[i,h,h] for i in noeuds) for h in hubs)
mdl.add_constraints(mdl.sum(zhn[h,i,h] for i in noeuds)*T>=dur[h] for h in hubs )
mdl.add_constraints(dur[h]<= T*nve for h in hubs)
mdl.add_constraints(mdl.sum(zhn[h,i,h]   for i in noeuds)==yh[h] for h in hubs )
mdl.add_constraints(mdl.sum(znh[i,h,h]   for i in noeuds)==yh[h] for h in hubs )
mdl.add_constraints(mdl.sum(z[i,j,h]+z[j,i,h]  for j in noeuds)>=x[i,h] for h in hubs for i in noeuds )
mdl.add_constraints(z[i,i,h]==0 for h in hubs for i in noeuds )
mdl.add_constraints(zhn[h,i,h]<=x[i,h] for i in noeuds for h in hubs )
mdl.add_constraints(znh[i,h,h]<=x[i,h] for i in noeuds for h in hubs )

mdl.add_constraints(zhn[h,i,hh]==0 for i in noeuds for h in hubs for hh in hubs if hh!=h )
mdl.add_constraints(znh[i,h,hh]==0 for i in noeuds for h in hubs for hh in hubs if hh!=h )

mdl.add_constraints(mdl.sum(x[i,h]*(O[i]+D[i]) for i in noeuds)<=mdl.sum(zhn[h,i,h] for i in noeuds)*C for h in hubs) 

mdl.add_constraints(mdl.sum(zhn[h,j,h]   for j in noeuds)==yh[h] for h in hubs for i in noeuds )
mdl.add_constraints(mdl.sum(znh[j,h,h]   for j in noeuds)==yh[h] for h in hubs for i in noeuds)

mdl.add_constraints(mdl.sum(z[i,j,h]   for j in noeuds)<=x[i,h] for h in hubs for i in noeuds)
mdl.add_constraints(mdl.sum(z[j,i,h]   for j in noeuds)<=x[i,h] for h in hubs for i in noeuds )





cout_tournee = mdl.sum(z[i,j,h] *dnn[i][j]*0.5 for h in hubs for i in noeuds  for j in noeuds if j!=i )+ mdl.sum(znh[i,h,h] *dhn[i][h]*0.5 for i in noeuds  for h in hubs)+mdl.sum(zhn[h,i,h] *dhn[i][h]*0.5 for i in noeuds  for h in hubs)
cout_inter=mdl.sum(ni[h,hh]*dhh[h][hh] for h in hubs for hh in hubs if hh!=h)
cout_fixe=mdl.sum(yh[i]*Fh for i in hubs) + ninter*Fv+nve*Fv
total_cost=cout_tournee+cout_inter+ cout_fixe
mdl.minimize(total_cost)
from docplex.mp.progress import TextProgressListener
unfiltered_texter = TextProgressListener(filtering=False)
mdl.add_progress_listener(unfiltered_texter)
mdl.set_time_limit(3600)
msol=mdl.solve(url=url, key=key,clean_before_solve=True)
if msol is None:
    print("model can't solve")
mdl.report()


obj = mdl.objective_value

print("* Model solved with objective: {:g}".format(obj))
assert msol
msol.display()
