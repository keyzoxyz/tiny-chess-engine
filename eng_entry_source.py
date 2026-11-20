import json,os,sys,urllib.request as U
E = os.environ.get("MAKEFUN_ENV_URL","")
MATE = 30000
V = (0,100,325,335,500,975,0)
PST = (
 (),
 (0,0,0,0,0,0,0,0,
 95,100,100,100,100,100,100,95,
 45,50,50,50,50,50,50,45,
 20,22,24,26,26,24,22,20,
 10,12,14,18,18,14,12,10,
 3,4,6,10,10,6,4,3,
 0,0,0,-8,-8,0,0,0,
 0,0,0,0,0,0,0,0),
 (-20,-12,-8,-6,-6,-8,-12,-20,
-12,-4,2,2,2,2,-4,-12,
-8,2,8,12,12,8,2,-8,
-6,4,12,16,16,12,4,-6,
-6,4,12,16,16,12,4,-6,
-8,2,8,12,12,8,2,-8,
-12,-4,2,2,2,2,-4,-12,
-20,-12,-8,-6,-6,-8,-12,-20),
 (-8,-4,-4,-4,-4,-4,-4,-8,
-4,4,0,0,0,0,4,-4,
-4,2,6,8,8,6,2,-4,
-4,2,8,12,12,8,2,-4,
-4,2,8,12,12,8,2,-4,
-4,2,6,8,8,6,2,-4,
-4,4,0,0,0,0,4,-4,
-8,-4,-4,-4,-4,-4,-4,-8),
 (2,2,2,2,2,2,2,2,
 12,12,12,12,12,12,12,12,
 0,0,0,0,0,0,0,0,
 0,0,0,2,2,0,0,0,
 0,0,0,2,2,0,0,0,
 0,0,0,0,0,0,0,0,
 0,0,0,-4,-4,0,0,0,
 0,0,2,4,4,2,0,0),
 (-6,-3,-2,-1,-1,-2,-3,-6,
-3,0,2,0,0,0,0,-3,
-2,2,4,4,4,4,2,-2,
-1,0,4,6,6,4,0,-1,
 0,0,4,6,6,4,0,-1,
-2,2,4,4,4,4,2,-2,
-3,0,2,0,0,0,0,-3,
-6,-3,-2,-1,-1,-2,-3,-6),
 (-30,-30,-34,-40,-40,-34,-30,-30,
-26,-26,-30,-36,-36,-30,-26,-26,
-22,-22,-26,-32,-32,-26,-22,-22,
-18,-18,-22,-28,-28,-22,-18,-18,
-14,-14,-18,-24,-24,-18,-14,-14,
-8,-8,-12,-16,-16,-12,-8,-8,
 14,14,2,-6,-6,2,14,14,
 18,26,12,-4,0,-8,26,18),
)
ND = (-33,-31,-18,-14,14,18,31,33)
BID = (15,17,-15,-17)
RID = (1,-1,16,-16)
QID = BID+RID
CRLOSS = {0x74: 3,0x77: 1,0x70: 2,0x04: 12,0x07: 4,0x00: 8}
MV = [0,0,0x150,0x160,0x140,0x1C0]
Z = [[(i*2654435761+p*40503+7919) for i in range(128)]
 for p in range(13)]
ZC = [(i*2246822519+31337) for i in range(16)]
ZE = [[(i*3266489917+j*668265263+1) for j in range(8)] for i in range(8)]
ZS = 0x9E3779B9
nodes = [0]
tt = {}
kill = [[0,0] for _ in range(96)]
hist = {}
ABORT = [False]
BUDGET = [50000]
def tick():
 nodes[0]+= 1
 if nodes[0]>BUDGET[0]:
  ABORT[0] = True
def post(p,b):
 r = U.Request(E+p,data=json.dumps(b).encode())
 return json.load(U.urlopen(r))
def sq(n):
 return (n>>4)*8+(n & 7)
def lsq(j):
 return (j>>3)*16+(j & 7)
def zh(b,w,cr,ep):
 h = ZS if w else 0
 for i in range(128):
  if i & 0x88:
   continue
  p = b[i]
  if p:
   h ^= Z[p+6][i]
 h ^= ZC[cr]
 if ep>=0:
  h ^= ZE[ep>>4][ep & 7]
 return h
def parse(fen):
 f = fen.split()
 b = [0]*128
 for r,row in enumerate(f[0].split("/")):
  fi = 0
  for ch in row:
   if ch.isdigit():
    fi+= int(ch)
   else:
    v = ".PNBRQK".index(ch.upper())
    b[(r<<4)+fi] = v if ch.isupper() else-v
    fi+= 1
 cr = 0
 for i,c in enumerate("KQkq"):
  if c in f[2]:
   cr |= 1<<i
 ep =-1
 if f[3]!="-":
  ep = ((8-int(f[3][1]))<<4)+"abcdefgh".index(f[3][0])
 w = f[1]=="w"
 s = 0
 kw = kb =-1
 for i in range(128):
  if not i & 0x88 and b[i]:
   p = b[i]
   a = p if p>0 else-p
   j = sq(i)
   s+= V[a]+PST[a][j] if p>0 else-(V[a]+PST[a][j ^ 56])
   if p==6:
    kw = i
   elif p==-6:
    kb = i
 return [b,w,cr,ep,zh(b,w,cr,ep),s,kw,kb]
def lf(ps):
 s = ps[5] if ps[1] else-ps[5]
 if s>480 or s<-480:
  k = ps[7] if s>0 else ps[6]
  r = k>>4
  f = k & 7
  u = r if r<4 else 7-r
  t = f if f<4 else 7-f
  v = (3-(u if u<t else t))*8
  s+= v if s>0 else-v
 return s
def att(b,t,byw):
 pw = 1 if byw else-1
 for d in ((15,17) if byw else (-15,-17)):
  n = t+d
  if not n & 0x88 and b[n]==pw:
   return True
 for d in ND:
  n = t+d
  if not n & 0x88 and b[n]==(2 if byw else-2):
   return True
 for d in BID:
  n = t+d
  while not n & 0x88:
   v = b[n]
   if v:
    if v==(3 if byw else-3) or v==(5 if byw else-5):
     return True
    break
   n+= d
 for d in RID:
  n = t+d
  while not n & 0x88:
   v = b[n]
   if v:
    if v==(4 if byw else-4) or v==(5 if byw else-5):
     return True
    break
   n+= d
 k = 6 if byw else-6
 for d in QID:
  n = t+d
  if not n & 0x88 and b[n]==k:
   return True
 return False
def gen(ps,caponly=False):
 b = ps[0]
 w = ps[1]
 cr = ps[2]
 ep = ps[3]
 mv = []
 for i in range(128):
  if i & 0x88:
   continue
  pc = b[i]
  if not pc or (pc>0)!=w:
   continue
  a = pc if pc>0 else-pc
  if a==1:
   d =-16 if w else 16
   home = 6 if w else 1
   last = 0 if w else 7
   n = i+d
   if not n & 0x88 and not b[n]:
    if not caponly:
     if (n>>4)==last:
      for pr0 in (5,4,3,2):
       mv.append((i,n,pr0,0))
     else:
      mv.append((i,n,0,0))
     if (i>>4)==home and not b[n+d]:
      mv.append((i,n+d,0,1))
   if ep>=0:
    for dd in (d-1,d+1):
     if i+dd==ep and not i+dd & 0x88:
      mv.append((i,ep,0,2))
   for dd in (d-1,d+1):
    q = i+dd
    if not q & 0x88:
     t = b[q]
     if t and (t>0)!=w:
      if (q>>4)==last:
       for pr0 in (5,4,3,2):
        mv.append((i,q,pr0,0))
      else:
       mv.append((i,q,0,0))
  elif a==6:
   for d in QID:
    n = i+d
    if not n & 0x88:
     t = b[n]
     if (not t) or ((t>0)!=w):
      if caponly and not t:
       continue
      mv.append((i,n,0,0))
   if not caponly:
    if w and i==0x74:
     if cr & 1 and not b[0x75] and not b[0x76] and \
       not att(b,0x74,False) and not att(b,0x75,False) and not att(b,0x76,False):
      mv.append((0x74,0x76,0,3))
     if cr & 2 and not b[0x71] and not b[0x72] and not b[0x73] and \
       not att(b,0x74,False) and not att(b,0x73,False) and not att(b,0x72,False):
      mv.append((0x74,0x72,0,3))
    elif not w and i==0x04:
     if cr & 4 and not b[0x05] and not b[0x06] and \
       not att(b,0x04,True) and not att(b,0x05,True) and not att(b,0x06,True):
      mv.append((0x04,0x06,0,3))
     if cr & 8 and not b[0x01] and not b[0x02] and not b[0x03] and \
       not att(b,0x04,True) and not att(b,0x03,True) and not att(b,0x02,True):
      mv.append((0x04,0x02,0,3))
  elif a==2:
   for d in ND:
    n = i+d
    if not n & 0x88:
     t = b[n]
     if not t:
      if not caponly:
       mv.append((i,n,0,0))
     elif (t>0)!=w:
      mv.append((i,n,0,0))
  else:
   ds = BID if a==3 else RID if a==4 else QID
   for d in ds:
    n = i+d
    while not n & 0x88:
     t = b[n]
     if not t:
      if not caponly:
       mv.append((i,n,0,0))
     else:
      if (t>0)!=w:
       mv.append((i,n,0,0))
      break
     n+= d
 return mv
def pv(p,i):
 a = p if p>0 else-p
 j = sq(i)
 return (V[a]+PST[a][j]) if p>0 else-(V[a]+PST[a][j ^ 56])
def mk(ps,m):
 b = ps[0]
 i,j,pr,fl = m
 pc = b[i]
 cap = b[j]
 h = ps[4]
 oldcr = ps[2]
 oldep = ps[3]
 s = ps[5]-pv(pc,i)
 kw = ps[6]
 kb = ps[7]
 epc =-1
 if fl==2:
  epc = j+(16 if pc>0 else-16)
  cap = b[epc]
  b[epc] = 0
  h ^= Z[cap+6][epc]
  s-= pv(cap,epc)
 b[i] = 0
 h ^= Z[pc+6][i]
 if cap and fl!=2:
  h ^= Z[cap+6][j]
  s-= pv(cap,j)
 b[j] = (pr if pc>0 else-pr) if pr else pc
 h ^= Z[b[j]+6][j]
 s+= pv(b[j],j)
 if pc==6:
  kw = j
 elif pc==-6:
  kb = j
 if fl==3:
  if j==0x76:
   b[0x77] = 0
   b[0x75] = 4
   h ^= Z[10][0x77] ^ Z[10][0x75]
   s+= pv(4,0x75)-pv(4,0x77)
  elif j==0x72:
   b[0x70] = 0
   b[0x73] = 4
   h ^= Z[10][0x70] ^ Z[10][0x73]
   s+= pv(4,0x73)-pv(4,0x70)
  elif j==0x06:
   b[0x07] = 0
   b[0x05] =-4
   h ^= Z[2][0x07] ^ Z[2][0x05]
   s+= pv(-4,0x05)-pv(-4,0x07)
  else:
   b[0x00] = 0
   b[0x03] =-4
   h ^= Z[2][0x00] ^ Z[2][0x03]
   s+= pv(-4,0x03)-pv(-4,0x00)
 h ^= ZS
 oldcr = ps[2]
 ps[2] = oldcr & ~(CRLOSS.get(i,0) | CRLOSS.get(j,0))
 if ps[2]!=oldcr:
  h ^= ZC[oldcr] ^ ZC[ps[2]]
 if ps[3]>=0:
  h ^= ZE[ps[3]>>4][ps[3] & 7]
 ps[3] =-1
 if fl==1:
  ep = (i+j)//2
  mypawn = b[j]
  left = b[j-1] if not (j-1) & 0x88 else 0
  right = b[j+1] if not (j+1) & 0x88 else 0
  if mypawn>0 and (left==-1 or right==-1):
   ps[3] = ep
  elif mypawn<0 and (left==1 or right==1):
   ps[3] = ep
 if ps[3]>=0:
  h ^= ZE[ps[3]>>4][ps[3] & 7]
 u = (pc,cap,ps[1],ps[4],epc,oldcr,oldep,ps[5],ps[6],ps[7])
 ps[1] = not ps[1]
 ps[4] = h
 ps[5] = s
 ps[6] = kw
 ps[7] = kb
 return u
def um(ps,m,u):
 b = ps[0]
 i,j,pr,fl = m
 pc,cap,w,h,epc,ps[2],ps[3],ps[5],ps[6],ps[7] = u
 b[i] = pc
 b[j] = cap
 if epc>=0:
  b[epc] = cap
  b[j] = 0
 if fl==3:
  if j==0x76:
   b[0x77] = 4
   b[0x75] = 0
  elif j==0x72:
   b[0x70] = 4
   b[0x73] = 0
  elif j==0x06:
   b[0x07] =-4
   b[0x05] = 0
  else:
   b[0x00] =-4
   b[0x03] = 0
 ps[1] = w
 ps[4] = h
def kic(ps,w):
 return att(ps[0],ps[6] if w else ps[7],not w)
def lgl(ps,ms):
 out = []
 w = ps[1]
 for m in ms:
  u = mk(ps,m)
  if not kic(ps,w):
   out.append(m)
  um(ps,m,u)
 return out
def srt(ps,mv,ply,pv):
 b = ps[0]
 out = []
 for m in mv:
  s = 0
  if m==pv:
   s = 1<<40
  else:
   t = b[m[1]]
   if t:
    s = 1<<20
    if V[abs(t)]>V[abs(b[m[0]])]:
     s+= (V[abs(t)]<<6)-V[abs(b[m[0]])]+(1<<18)
    else:
     s+= (V[abs(t)]<<3)-V[abs(b[m[0]])]
   elif m[2]:
    s = 1<<19
   elif m==kill[ply][0]:
    s = 1<<18
   elif m==kill[ply][1]:
    s = 1<<17
   else:
    s = hist.get(m,0)
  out.append((s,m))
 out.sort(reverse=True)
 return out
def qs(ps,a,be,ply):
 tick()
 if ABORT[0]:
  return a
 st = ps[5] if ps[1] else-ps[5]
 g,lg,mk_,um_ = gen,lgl,mk,um
 mv = srt(ps,g(ps,True),ply,None)
 if not mv and (st>480 or st<-480):
  st = lf(ps)
  if not kic(ps,ps[1]) and not lg(ps,g(ps)):
   return 0
 if st>=be:
  return be
 if st>a:
  a = st
 if ply>14:
  return a
 for s,m in mv:
  u = mk_(ps,m)
  if abs(u[1])==6:
   um_(ps,m,u)
   return MATE-ply
  v =-qs(ps,-be,-a,ply+1)
  um_(ps,m,u)
  if ABORT[0]:
   return a
  if v>a:
   a = v
   if a>=be:
    break
 return a
P = []
def abret(v,ps):
 P.pop();return v
def ab(ps,d,a,be,ply):
 tick()
 h = ps[4]
 if ply>1 and h in P:
  return 0
 P.append(h)
 if ABORT[0]:
  return abret(a,ps)
 k = (h,ps[1],ps[3])
 pv = None
 e = tt.get(k)
 if e is not None:
  ed,evv,fl,em = e
  pv = em
  if ed>=d:
   if fl==0:
    return abret(evv,ps)
   if fl==1 and evv<=a:
    return abret(evv,ps)
   if fl==2 and evv>=be:
    return abret(evv,ps)
 if d<=0:
  return abret(qs(ps,a,be,ply),ps)
 w = ps[1]
 if d>=3 and not kic(ps,w) and ply>1:
  material = sum(1 for x in ps[0] if x and (x>0)==w and abs(x)>1)
  if material>=3:
   ps[1] = not w
   ps[3] =-1
   ps[4] = h ^ ZS
   v =-ab(ps,d-3,-be,-be+1,ply+1)
   ps[1] = w
   ps[4] = h
   if ABORT[0]:
    return abret(a,ps)
   if v>=be:
    return abret(v,ps)
 mv = gen(ps)
 best =-MATE-1
 bm = None
 oa = a
 for s,m in srt(ps,mv,ply,pv):
  u = mk(ps,m)
  if abs(u[1])==6:
   um(ps,m,u)
   return abret(MATE-ply,ps)
  v =-ab(ps,d-1,-be,-a,ply+1)
  um(ps,m,u)
  if ABORT[0]:
   return abret(a,ps)
  if v>best:
   best = v
   bm = m
   if v>a:
    a = v
    if a>=be:
     if not u[1] and not m[2] and ply<96:
      if kill[ply][0]!=m:
       kill[ply][1] = kill[ply][0]
       kill[ply][0] = m
      hist[m] = hist.get(m,0)+d*d
     break
 if best==-MATE-1:
  if lgl(ps,mv):
   best = 0
  else:
   best = (ply-MATE) if kic(ps,w) else 0
  if len(tt)<500000:
   tt[k] = (d,best,0,None)
  return abret(best,ps)
 fl = 1 if best<=oa else (2 if best>=be else 0)
 if len(tt)<500000:
  tt[k] = (d,best,fl,bm)
 return abret(best,ps)
def u2m(u,b=None):
 i = lsq((8-int(u[1]))*8+"abcdefgh".index(u[0]))
 j = lsq((8-int(u[3]))*8+"abcdefgh".index(u[2]))
 pr = ".PNBRQK".index(u[4].upper()) if len(u)>4 else 0
 fl = 0
 if b is None:
  return (i,j,pr,fl)
 pc = b[i]
 if pc and abs(pc)==6 and not pr and u in ("e1g1","e1c1","e8g8","e8c8"):
  fl = 3
 elif pc and abs(pc)==1 and not pr:
  if abs((i>>4)-(j>>4))==2 and (j & 7)==(i & 7):
   fl = 1
  elif (j & 7)!=(i & 7) and not b[j]:
   fl = 2
 return (i,j,pr,fl)
def choose(ps,legal,budget=50000):
 nodes[0] = 0
 ABORT[0] = False
 tt.clear()
 hist.clear()
 for x in kill:
  x[0] = x[1] = 0
 BUDGET[0] = budget
 ms = []
 for u in legal:
  m = u2m(u,ps[0])
  h = mk(ps,m)
  s0 =not lgl(ps,gen(ps)) and not kic(ps,ps[1])
  um(ps,m,h)
  ms.append((m,u,s0))
 best = legal[0]
 for d in range(1,24):
  a =-MATE-1
  be = MATE+1
  cb = None
  cv =-MATE-1
  ok = True
  for m,us,s0 in ms:
   u = mk(ps,m)
   v = 0 if s0 else-ab(ps,d-1,-be,-a,1)
   um(ps,m,u)
   if ABORT[0]:
    ok = False
    break
   if v>cv:
    cv = v
    cb = us
   if v>a:
    a = v
  if not ok:
   break
  if cb is not None:
   best = cb
   ms.sort(key=lambda t: t[1]!=cb)
  if cv>=MATE-200:
   break
 return best
def main():
 g = post("/game",{})
 while g.get("status")!="done":
  if not g.get("legal_moves"):
   g = post("/game",{})
   continue
  ps = parse(g["fen"])
  m = choose(ps,g["legal_moves"])
  g = post("/move",{"game": g["game"],"move": m})
 
if __name__=="__main__":
 main()