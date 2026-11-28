import sys, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
key, SRC, OUT, D = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
LIMIT = float(sys.argv[5]) if len(sys.argv)>5 else None
FB="C:/Users/VIPRIN/AppData/Local/Microsoft/Windows/Fonts/MonumentExtended-Ultrabold.otf"
W,H=1440,2560; FPS=24000/1001
HOOKS={"A":(["MEZCLANDO A JUSTIN","BIEBER CON MI TEMA"],None),
       "B":(["“NO PODÉS MEZCLAR A JUSTIN","BIEBER CON TU PROPIO TEMA”"],"YO:"),
       "C":(["LA MEZCLA NO PUEDE","SER TAN BUE..."],None),
       "R":(["RECREANDO MEZCLAS","QUE ESCUCHÉ POR AHÍ"],None)}
lines,extra=HOOKS[key]
tmp=ImageDraw.Draw(Image.new("L",(10,10)))
sz=84
while max(tmp.textlength(l,font=ImageFont.truetype(FB,sz)) for l in lines)>1180: sz-=2
f=ImageFont.truetype(FB,sz); lh=int(sz*1.3)
tot=lh*(len(lines)-1)+sz+(int(sz*1.9) if extra else 0); y0=1290-tot//2
# palabras con posición
words=[]
sp=tmp.textlength(" ",font=f)
for i,l in enumerate(lines):
    x=(W-tmp.textlength(l,font=f))/2; y=y0+i*lh
    for w in l.split(" "):
        words.append((w,x,y,f)); x+=tmp.textlength(w,font=f)+sp
if extra:
    f2=ImageFont.truetype(FB,int(sz*1.25)); w=tmp.textlength(extra,font=f2)
    words.append((extra,(W-w)/2,y0+(len(lines)-1)*lh+sz+int(sz*0.75),f2))
STAG=0.11; DUR=0.32; T0=0.05
def ease(u): u=min(max(u,0),1); return 1-(1-u)**3
def text_mask(t):
    m=Image.new("L",(W,H),0)
    for i,(w,x,y,ff) in enumerate(words):
        st=T0+i*STAG+(0.15 if (extra and i==len(words)-1) else 0)
        u=ease((t-st)/DUR)
        if u<=0: continue
        lay=Image.new("L",(W,H),0); ImageDraw.Draw(lay).text((x,y+18*(1-u)),w,font=ff,fill=int(255*u))
        m=Image.fromarray(np.maximum(np.asarray(m),np.asarray(lay)))
    return np.asarray(m,dtype=np.float32)/255
TEXT_END=T0+len(words)*STAG+DUR+0.2
final_mask=text_mask(99)
# tapas
s=473; gap=70; yc=1610; x1=(W-2*s-gap)//2; x2=x1+s+gap
def load(p):
    c=Image.open(p).convert("RGB").resize((s,s),Image.LANCZOS)
    m=Image.new("L",(s,s),0); ImageDraw.Draw(m).rounded_rectangle((0,0,s-1,s-1),22,fill=255)
    c=c.convert("RGBA"); c.putalpha(m)
    pad=90; g=Image.new("RGBA",(s+2*pad,s+2*pad),(0,0,0,0))
    col=Image.open(p).convert("RGB").resize((1,1),Image.LANCZOS).getpixel((0,0))
    col=tuple(min(255,int(v*1.4)+40) for v in col)
    ImageDraw.Draw(g).rounded_rectangle((pad,pad,pad+s,pad+s),30,fill=col+(150,))
    g=g.filter(ImageFilter.GaussianBlur(38))
    return c,g,pad
import os
CL=os.environ.get("COVER_L",D+"/1900x1900-000000-80-0-0.jpg"); CR=os.environ.get("COVER_R",D+"/portada/portada_A_cupula.jpg")
covers=[(load(CL),x1,0.0),(load(CR),x2,1.3)]
# tapa "?" que se revela en REVEAL segundos (opcional)
REVEAL=float(os.environ["REVEAL"]) if os.environ.get("REVEAL") else None
if REVEAL is not None:
    qp=os.path.join(os.environ.get("TEMP","."),f"_qcard_{os.getpid()}.png")
    q=Image.new("RGB",(900,900),(0,0,0)); qd=ImageDraw.Draw(q)
    for yy in range(900):
        v=yy/899; qd.line([(0,yy),(899,yy)],fill=(int(18+30*v),int(6+8*v),int(34+50*v)))
    qf=ImageFont.truetype(FB,560); bb=qd.textbbox((0,0),"?",font=qf)
    qd.text(((900-(bb[2]-bb[0]))/2-bb[0],(900-(bb[3]-bb[1]))/2-bb[1]),"?",font=qf,fill=(255,255,255))
    q.save(qp); QCARD=load(qp); os.remove(qp)
def backout(u):
    u=min(max(u,0),1); c1=1.70158; c3=c1+1; return 1+c3*(u-1)**3+c1*(u-1)**2
def cover_layer(t):
    L=Image.new("RGBA",(W,H),(0,0,0,0))
    for k,((c,g,pad),x,ph) in enumerate(covers):
        st=0.25+k*0.15
        if k==1 and REVEAL is not None:
            if t<REVEAL: c,g,pad=QCARD
            else: st=REVEAL
        u=(t-st)/0.5
        if u<=0: continue
        pop=backout(u); a=min(1,u*1.6)
        br=1+0.025*math.sin(2*math.pi*t/3.2+ph)
        fl=9*math.sin(2*math.pi*t/4.1+ph*1.7)
        sc=(0.82+0.18*pop)*br
        glow=0.75+0.25*math.sin(2*math.pi*t/2.6+ph)
        cx=x+s/2; cy=yc+s/2+fl
        gs=int((s+2*pad)*sc); gg=g.resize((gs,gs),Image.BILINEAR)
        ga=gg.getchannel("A").point(lambda v:int(v*a*glow)); gg.putalpha(ga)
        L.alpha_composite(gg,(int(cx-gs/2),int(cy-gs/2)))
        cs=int(s*sc); cc=c.resize((cs,cs),Image.BICUBIC)
        if a<1: cc.putalpha(cc.getchannel("A").point(lambda v:int(v*a)))
        L.alpha_composite(cc,(int(cx-cs/2),int(cy-cs/2)))
    return np.asarray(L,dtype=np.float32)
dec=subprocess.Popen(["ffmpeg","-v","error","-i",SRC]+(["-t",str(LIMIT)] if LIMIT else [])+["-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","24000/1001","-i","-","-i",SRC,
    "-map","0:v","-map","1:a","-c:v","h264_nvenc","-preset","p6","-cq","23","-b:v","5M","-maxrate","7M","-pix_fmt","yuv420p","-c:a","copy","-shortest","-movflags","+faststart",OUT],stdin=subprocess.PIPE)
n=0; fs=W*H*3
while True:
    b=dec.stdout.read(fs)
    if len(b)<fs: break
    t=n/FPS; v=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)
    m=final_mask if t>TEXT_END else text_mask(t)
    v=np.abs(v-255*m[...,None])
    cl=cover_layer(t); a=cl[...,3:4]/255
    v=v*(1-a)+cl[...,:3]*a
    enc.stdin.write(v.clip(0,255).astype(np.uint8).tobytes()); n+=1
enc.stdin.close(); enc.wait(); print("frames",n)
