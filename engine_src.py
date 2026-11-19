import json,os,sys,urllib.error,urllib.request as U
ENV_URL=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
VALUE={"p":1,"n":3,"b":3,"r":5,"q":9,"k":100}
def post(p,b):
 try:
  with U.urlopen(U.Request(ENV_URL+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"}))as r:return json.load(r)
 except urllib.error.HTTPError as e:sys.exit(f"{p}: HTTP {e.code} {e.read().decode(errors='replace')}")
def board_of(n):
 b={}
 for i,r in enumerate(n.split()[0].split("/")):
  x=0
  for c in r:
   if c.isdigit():x+=int(c)
   else:b["abcdefgh"[x]+str(8-i)]=c;x+=1
 return b
L,M=200000,99999
O=(-9,-11,9,11,-10,1,10,-1)
D={'P':(-10,-20,-11,-9),'N':(-19,-21,19,21,-8,8,-12,12),'B':O[:4],'R':O[4:],'Q':O,'K':O}
def Z(p,i):r,c=divmod(i,10);x=abs(2*c-9);return(7-x)*(9-r)if p=='P'else 20-3*(x+abs(2*r-11))if p=='N'else 0
S={p:[100*VALUE[p.lower()]*(p!='K')+Z(p,i)for i in range(120)]for p in D}
R=lambda b:b[::-1].swapcase()
E=lambda b:sum(S[p][i]if p<'a'else-S[p.upper()][119-i]for i,p in enumerate(b)if p.isalpha())
def G(b):
 for i,p in enumerate(b):
  if p.isupper():
   for d in D[p]:
    j=i+d
    while 1:
     q=b[j]
     if q==' 'or q.isupper()or p=='P'and(d in(-10,-20)and(q!='.'or d<-10 and(i<81 or b[i-10]!='.'))or d in(-11,-9)and q=='.'):break
     yield i,j
     if p in'PNK'or q!='.':break
     j+=d
def V(b,i,j):
 p,q=b[i],b[j];g=S[p][j]-S[p][i]+(q!='.'and S[q.upper()][119-j])
 if p=='P'and j<29:p='Q';g+=S[p][j]-S['P'][j]
 c=list(b);c[j]=p;c[i]='.';return R(''.join(c)),g
def F(b,s,d,a,e):
 global N;N+=1
 if d<1:
  if s>=e:return s
  a=max(a,s)
 t=-M
 for i,j in sorted(G(b),key=lambda m:(b[m[1]]=='.',VALUE[b[m[0]].lower()]-VALUE.get(b[m[1]].lower(),0))):
  if b[j]=='k':return M
  if N>=L:break
  if d<1 and b[j]=='.':continue
  c,g=V(b,i,j);v=-F(c,-s-g,d-1,-e,-a);t=max(t,v);a=max(a,v)
  if a>=e:break
 if d>0 and t==-M and N<L and not any(R(b)[j]=='k'for _,j in G(R(b))):return 0
 return a
def Q(s,f):i=(10-int(s[1]))*10+' abcdefgh'.index(s[0]);return 119-i if f else i
def P(b,m,f):
 i,j=Q(m,f),Q(m[2:],f);p=b[i];c=list(b);c[j],c[i]=p,'.'
 if p=='P':
  if m[4:]:c[j]=m[4].upper()
  if(i-j)%10 and b[j]=='.':c[j+10]='.'
 if p=='K'and abs(j-i)==2:
  d=(j-i)//2;k=j
  while c[k]!='R':k+=d
  c[k],c[i+d]='.','R'
 return R(''.join(c))
def C(n,l):
 global N
 X=board_of(n);f=n.split()[1]=='b'
 b=' '*20+''.join(' '+''.join(X.get(x+str(r),'.')for x in'abcdefgh')+' 'for r in range(8,0,-1))+' '*20
 if f:b=R(b)
 K=sorted(((m,c,E(c))for m in l for c in[P(b,m,f)]),key=lambda k:k[2])
 N=0;w=l[0];d=1
 while d<40:
  a,h=-2*M,0
  for m,c,e in K:
   v=-F(c,e,d-1,-2*M,-a)
   if N>=L and d>1:break
   if v>a:a,h=v,m
  else:
   w=h;K.sort(key=lambda k:k[0]!=h);d+=1
   if N<L and abs(a)<M:continue
  break
 return w
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
