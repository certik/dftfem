#! /usr/bin/python

import math
import utils

def load(path):
    filename=path+"fort.67";
    f=" ".join(file(filename).readlines()).split()
    data=[]
    i=0
    k0=500
    while i<len(f):
        for j in range(3):
            assert f[i]=="================================";i+=1
            assert f[i]=="=";i+=1
            assert f[i]=="N";i+=1
            n=int(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="L";i+=1
            l=int(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="E";i+=1
            E=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="K0";i+=1
            K0=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="JM";i+=1
            jm=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="AP";i+=1
            ap=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="RAD0";i+=1
            rad0=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="RINT";i+=1
            rint=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="irel";i+=1
            irel=int(f[i]);i+=1; 

            input=(n,l,E,K0,jm,ap,rad0,rint,irel)

            assert f[i:i+3]==["=====returned","by","WAVC3H========="];i+=3
            assert f[i]=="=";i+=1
            assert f[i]=="N";i+=1
            n=int(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="L";i+=1
            l=int(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="E";i+=1
            E=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="EII";i+=1
            EII=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="ACC";i+=1
            ACC=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="KX";i+=1
            KX=float(f[i]);i+=1; 
            assert f[i]=="=";i+=1
            assert f[i]=="Y";i+=1
            y=[float(x) for x in f[i:i+k0]]; assert f[i+k0]=="=";i+=k0+1

            output=(n,l,E,EII,ACC,KX,y)

            data.append((input,output))
    assert i==len(f)
    return data

def parse_fort67():
    d=load("");
    for state in d:
        input,output=state;
        #input=(n,l,E,K0,jm,ap,rad0,rint,irel)
        #output=(n,l,E,EII,ACC,KX,y)
        k0=int(input[3])
        jm=int(input[4])
        ap=input[5]
        print "-"*70
        print input
        print "Eout = %.17f"%(output[2])
    r=[ap*j/(jm-j) for j in range(1,k0+1)]
    return r

def parse_1adns():
    f=file("1a.dns")
    f.readline()
    rho=[]
    for l in f:
        rho.append(float(l.split()[1]))
    return rho;

def parse_fort49():
    f=file("fort.49")
    l=" ".join(f.readlines()).split()
    i=0;
    assert l[i]=="U-3";i+=1
    U3=[float(x) for x in l[i:i+500]];i+=500
    assert l[i]=="U-P0";i+=1
    UP0=[float(x) for x in l[i:i+500]];i+=500
    assert l[i]=="U-P1";i+=1
    UP1=[float(x) for x in l[i:i+500]];i+=500
    assert l[i]=="U-P2";i+=1
    UP2=[float(x) for x in l[i:i+500]];i+=500
    assert i==len(l)
    return U3,UP0,UP1,UP2

def parse_1adat():
    """returns (va,val,ngau)
    va ... 5 coeeficients for Vloc

    val ... val[0] .... 3*ngau values for V_0, 
            val[1] .... 3*ngau values for V_1, 
            ...
    """
    f=file("1a.dat")
    l=f.readlines();
    i=0;
    while l[i]!="CORPOT\n": i+=1
    i+=1
    va=[float(x) for x in l[i].split()[:5]]
    i+=1
    nval,ngau=[int(x) for x in l[i].split()]
    i+=1
    del l[:i]
    l=" ".join(l).split()
    val=[]
    i=0
    for j in range(nval):
        val.append([float(x) for x in l[i:i+3*ngau]])
        i+=3*ngau
    assert l[i]=="WAVE"
    return va,val,ngau

def plot(r,rho,U3,UP0,UP1,UP2,U):
    utils.makeplot(r,[
            (rho,"k+","rho"),
            (U3,"m+","U3=V_H+V_xc"),
            (UP0,"r+","UP0=V_0 (s)"),
            (UP1,"g+","UP1=V_1 (p)"),
            (UP2,"b+","UP2=V_2 (d)"),
            (U,"c+","Vloc"),
            ],"Potentials")

def plot2(r,rho,U,V0,V1,V2):
    utils.makeplot(r,[
            (rho,"k-","rho"),
            (U,"m-","U=V_H+V_xc+V_loc"),
            (V0,"r-","V_0 (s)"),
            (V1,"g-","V_1 (p)"),
            (V2,"b-","V_2 (d)"),
            ],"Potentials",(-2.3,2),(0,10))

def ERFM(x):
    from scipy.special import erf
    return erf(x)

def computeVloc(r,va):
    Vloc=[]
    for j in range(len(r)):
        corp=0.
        for k in (0,1):
            corp+=va[k+2]*ERFM(math.sqrt(va[k])*r[j])
        corp=-corp*va[4]/r[j]
        Vloc.append(corp)
    return Vloc

def computeVl(L,r,val,ngau):
    Vl=[]
    for j in range(len(r)):
        corp=0.
        for k in range(ngau):
            corp+=math.exp(-r[j]*r[j]*val[L][k])* \
                (val[L][k+ngau]+r[j]*r[j]*val[L][k+2*ngau])
        Vl.append(corp)
    return Vl

def savelist(f,l):
    for x in l:
        f.write("%.20f\n"%x)

def save(r,U3,Vloc,V0,V1,V2):
    f=file("potentials.dat","w")
    savelist(f,r)
    savelist(f,U3)
    savelist(f,Vloc)
    savelist(f,V0)
    savelist(f,V1)
    savelist(f,V2)

r=parse_fort67()
rho=parse_1adns()
U3,UP0,UP1,UP2=parse_fort49()
va,val,ngau=parse_1adat()
Vloc=computeVloc(r,va)
V0,V1,V2=[computeVl(L,r,val,ngau) for L in (0,1,2)]
utils.cmp(UP0,[x+y for (x,y) in zip(Vloc,V0)],7)
utils.cmp(UP1,[x+y for (x,y) in zip(Vloc,V1)],7)
utils.cmp(UP2,[x+y for (x,y) in zip(Vloc,V2)],7)

save(r,U3,Vloc,V0,V1,V2)

#plot(r,rho,U3,UP0,UP1,UP2,Vloc)
U=[x+y for (x,y) in zip(Vloc,U3)]
plot2(r,rho,U,V0,V1,V2)
