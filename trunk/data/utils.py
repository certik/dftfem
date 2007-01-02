import math
import sys

def cmp(a,b,places=18):
    """Asserts sequences a and b are the same on 'places' decimal places."""
    if isseq(a):
        cmp_seq(a,b,cmp_num,places)
    else: 
        cmp_num(a,b,places)
def cmprel(a,b,percent=1e-10):
    if isseq(a):
        def findmax(a):
            m=-1
            for x in a:
                if abs(x)>m:
                    m=abs(x)
            assert m!=-1
            return m
        m=max(findmax(a),findmax(b))
        cmp_seq(a,b,cmprel_num,(m,percent))
    else: 
        cmprel_num(a,b,(max(a,b),percent))

def cmp_num(a,b,places):
   assert abs(a-b)<math.pow(10.0,-places) 

def cmprel_num(x,y,data):
    """Asserts numbers x and y are within "percent" % of each other."""
    m,percent=data
    if m==0:
        assert x==y
        assert str(x)!="nan"
        assert str(y)!="nan"
        return
    assert abs((x-y)/float(m))<percent/100.0

def cmp_seq(a,b,cmpfunc,data):
    assert len(a)==len(b)
    for x,y in zip(a,b):
        cmpfunc(x,y,data)

def isseq(a):
#    from Numeric import array
    return not isinstance(a,(int,float))
#    return isinstance(a,list) or isinstance(a,tuple) or isinstance(a,array)

def assertAlmostEqual(x,y,places):
    assert abs(x-y)<10**(-places)
def assertNotAlmostEqual(x,y,places):
    assert abs(x-y)>10**(-places)

def write(str):
    print str,
    sys.stdout.flush()

def plot(r,y1,y2):
    makeplot(r,[
        (y1,"b+","1"),
        (y2,"g+","2"),
        ])

def plot3(r,y1,y2,y3):
    makeplot(r,[
        (y1,"b+","1"),
        (y2,"g+","2"),
        (y3,"kx","3"),
        ])

def makeplot(x,ys,title="Porovnani",lim=(-6,2),xlim=(0,20)):
    import pylab
    f=pylab.figure()
    leg=[]
    for g in ys:
        pylab.plot(x,g[0],g[1])
        leg.append(g[2])
    pylab.title(title)
    pylab.legend(leg)
    #pylab.savefig("graph.png")
    pylab.xlim(xlim)
    pylab.ylim(lim)
    pylab.xlabel("r")
    pylab.show()
