# tiny-chess-01 engine (MIT, see LICENSE). Negamax alpha-beta, iterative
# deepening under a fixed node budget L (no clock, no random), captures first
# (victim minus mover), quiescence over captures. Board: 120-char mailbox,
# rotated so the side to move is uppercase. <=4,096 bytes, stdlib only.

import json
import os
import sys
import urllib.error
import urllib.request

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")

VALUE = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}


def post(path, body):
    """POST a JSON body to the env and return its JSON answer."""
    req = urllib.request.Request(
        ENV_URL + path,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")


def board_of(fen):
    """The FEN's pieces as {square: letter}, e.g. {"e1": "K", "e8": "k"}."""
    board = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        file = 0
        for c in row:
            if c.isdigit():
                file += int(c)
            else:
                board["abcdefgh"[file] + str(8 - i)] = c
                file += 1
    return board


L,M=200000,99999
O=(-9,-11,9,11,-10,1,10,-1)
D={'P':(-10,-20,-11,-9),'N':(-19,-21,19,21,-8,8,-12,12),'B':O[:4],'R':O[4:],'Q':O,'K':O}
def bon(p,i):  # centipawn piece-square bonus for central pawns/knights
 r,c=divmod(i,10);x=abs(2*c-9)
 return(7-x)*(9-r)if p=='P'else 20-3*(x+abs(2*r-11))if p=='N'else 0
S={p:[100*VALUE[p.lower()]*(p!='K')+bon(p,i)for i in range(120)]for p in D}
rot=lambda b:b[::-1].swapcase()
def ev(b):return sum(S[p][i]if p<'a'else-S[p.upper()][119-i]for i,p in enumerate(b)if p.isalpha())
def gen(b):
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
def mv(b,i,j):
 p,q=b[i],b[j];g=S[p][j]-S[p][i]+(q!='.'and S[q.upper()][119-j])
 if p=='P'and j<29:p='Q';g+=S[p][j]-S['P'][j]  # promotion adds the queen
 c=list(b);c[j]=p;c[i]='.';return rot(''.join(c)),g
def se(b,s,d,a,e):
 global N;N+=1
 if d<1:
  if s>=e:return s
  a=max(a,s)
 t=-M
 for i,j in sorted(gen(b),key=lambda m:(b[m[1]]=='.',VALUE[b[m[0]].lower()]-VALUE.get(b[m[1]].lower(),0))):
  if b[j]=='k':return M
  if N>=L:break
  if d<1 and b[j]=='.':continue
  c,g=mv(b,i,j);v=-se(c,-s-g,d-1,-e,-a);t=max(t,v);a=max(a,v)
  if a>=e:break
 if d>0 and t==-M and N<L and not any(rot(b)[j]=='k'for _,j in gen(rot(b))):return 0
 return a
def sq(s,f):i=(10-int(s[1]))*10+' abcdefgh'.index(s[0]);return 119-i if f else i
def pl(b,m,f):
 i,j=sq(m,f),sq(m[2:],f);p=b[i];c=list(b);c[j],c[i]=p,'.'
 if p=='P':
  if m[4:]:c[j]=m[4].upper()
  if(i-j)%10 and b[j]=='.':c[j+10]='.'
 if p=='K'and abs(j-i)==2:
  d=(j-i)//2;k=j
  while c[k]!='R':k+=d
  c[k],c[i+d]='.','R'
 return rot(''.join(c))
def choose(fen,legal):
 global N
 B=board_of(fen);f=fen.split()[1]=='b'
 b=' '*20+''.join(' '+''.join(B.get(x+str(r),'.')for x in'abcdefgh')+' 'for r in range(8,0,-1))+' '*20
 if f:b=rot(b)
 K=sorted(((m,c,ev(c))for m in legal for c in[pl(b,m,f)]),key=lambda k:k[2])
 N=0;w=legal[0];d=1
 while d<40:
  a,bm=-2*M,0
  for m,c,e in K:
   v=-se(c,e,d-1,-2*M,-a)
   if N>=L and d>1:break
   if v>a:a,bm=v,m
  else:
   w=bm;K.sort(key=lambda k:k[0]!=bm);d+=1
   if N<L and abs(a)<M:continue
  break
 return w


while True:
    g = post("/game", {})
    if g["status"] == "done":
        break
    while g["status"] == "your_move":
        g = post("/move", {"game": g["game"], "move": choose(g["fen"], g["legal_moves"])})
    print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost", file=sys.stderr)
