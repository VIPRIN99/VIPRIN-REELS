# Subtitulos "No pinta la ambiguedad" sobre video vertical 4K (2160x3840), sin hook.
# Letra: Monument Ultrabold blanco en modo diferencia, abajo, con pop por frase.
# Palabras clave: palabra gigante en 3 filas DETRAS de la persona (mascara mediapipe),
# en diferencia, que cambia relleno/contorno varias veces + negativo de 2 frames al entrar.
# Audio intacto. Uso: python subs_ambiguedad_4k.py entrada.mp4 salida.mp4 [offset_s]
import json, subprocess, sys
import numpy as np, cv2, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
OFF = float(sys.argv[3]) if len(sys.argv) > 3 else 2.44   # tiempo crudo original - tiempo de este video
BUILD = "C:/Claude Workspace/CRUDOS/ambiguedad/build/"
FB = "C:/Users/VIPRIN/AppData/Local/Microsoft/Windows/Fonts/MonumentExtended-Ultrabold.otf"
W, H = 2160, 3840
S = W / 1440
probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=r_frame_rate,nb_frames", "-of", "json", SRC], capture_output=True, text=True).stdout)["streams"][0]
a_, b_ = probe["r_frame_rate"].split("/"); FPS = int(a_) / int(b_)

KEYWORD = {"LA AMBIGÜEDAD": "AMBIGÜEDAD", "UN SUSPIRO": "SUSPIRO", "LA PRESIÓN": "PRESIÓN",
           "DELIRO?": "DELIRO", "DE SIEMPRE": "SIEMPRE"}
chunks = [(a - OFF, b - OFF, c, k) for a, b, c, k in json.load(open(BUILD + "timing.json", encoding="utf-8"))["chunks"]]
chunks = [c for c in chunks if c[1] > 0.05]

# ---------- mascara de persona ----------
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=BUILD + "selfie_multiclass.tflite"),
    running_mode=vision.RunningMode.VIDEO, output_confidence_masks=True))
prev = [None]
def person_mask(fr, i):
    small = cv2.resize(fr, (720, 1280), interpolation=cv2.INTER_AREA)
    r = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(small)), int(i * 1000 / FPS))
    p = 1.0 - r.confidence_masks[0].numpy_view()
    if prev[0] is not None: p = 0.6 * p + 0.4 * prev[0]
    prev[0] = p
    m = np.clip((cv2.resize(p, (W, H), interpolation=cv2.INTER_CUBIC) - 0.35) / 0.3, 0, 1)
    return cv2.GaussianBlur(m, (0, 0), 3.0)

# ---------- texto ----------
_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FB, sz)
    return _fc[sz]
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3

def lyric_img(text, key):
    f = font(int((108 if key else 92) * S))
    l, t, r, b = f.getbbox(text)
    pad = 30
    im = Image.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=255)
    return np.asarray(im, np.float32) / 255
LYR = {c: lyric_img(c, k) for _, _, c, k in chunks}

def paste(L, img, cx, cy, a=1.0):
    h, w = img.shape; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    ys, xs = slice(max(0, y0), min(H, y0 + h)), slice(max(0, x0), min(W, x0 + w))
    if ys.start >= ys.stop or xs.start >= xs.stop: return
    sub = img[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0] * a
    L[ys, xs] = np.maximum(L[ys, xs], sub)

def giant_row(word, size, filled):
    f = font(size); l, t, r, b = f.getbbox(word); pad = 20
    im = Image.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
    sw = max(4, int(size * 0.025))
    if filled: ImageDraw.Draw(im).text((pad - l, pad - t), word, font=f, fill=255)
    else: ImageDraw.Draw(im).text((pad - l, pad - t), word, font=f, fill=0, stroke_width=sw, stroke_fill=255)
    return np.asarray(im, np.float32) / 255
_gc = {}
def giant(word, size, filled):
    k = (word, size, filled)
    if k not in _gc: _gc[k] = giant_row(word, size, filled)
    return _gc[k]

DUR_END = chunks[-1][1]
def layers(t):
    lyr = np.zeros((H, W), np.float32); bg = np.zeros((H, W), np.float32); neg = False
    for t0, t1, c, k in chunks:
        if t0 - 0.02 <= t < t1:
            img = LYR[c]
            base = min(1.0, 0.90 * W / img.shape[1])
            top = max(base, min(base * 1.28, 0.96 * W / img.shape[1]))
            u = (t - t0) / 0.09; sc = top - (top - base) * ease(u)
            if sc != 1.0: img = cv2.resize(img, None, fx=sc, fy=sc, interpolation=cv2.INTER_LINEAR)
            paste(lyr, img, W / 2, 2010 * S)
        if k:
            word = KEYWORD.get(c, c)
            end = min(t1 + 0.5, DUR_END + 1) if c != "PIEDRA" else t1
            if not (t0 <= t < end): continue
            if t - t0 < 2.1 / FPS: neg = True                      # negativo de 2 frames al entrar
            amb = word == "AMBIGÜEDAD"
            size = int(min(250, 1330 / (0.98 * len(word))) * S)
            step = 0.085 if amb else 0.12                             # el texto cambia varias veces
            ph = int((t - t0) / step)
            nchg = 7 if amb else 4
            fade = ease((end - t) / 0.12)
            for j in range(3):
                y = (790 + size / S * 1.05 * j) * S
                dx = (140 if j % 2 == 0 else -140) * S
                p = (t - t0) / (end - t0)
                x = W / 2 + dx - (dx * 1.25) * ease(p * 1.4)
                if ph < nchg:
                    filled = (j == ph % 3) if amb else ((j + ph) % 2 == 1)
                    jitter = ((ph * 37 + j * 11) % 5 - 2) * 6 * S if amb else 0
                else:
                    filled, jitter = (j == 1), 0
                pop = 0.4 + 0.6 * ease((t - t0 - j * 0.04) / 0.09)
                img = giant(word, size, filled)
                if pop < 0.999: img = cv2.resize(img, None, fx=pop, fy=pop, interpolation=cv2.INTER_LINEAR)
                paste(bg, img, x + jitter, y, fade)
    return lyr, bg, neg

LIMIT = float(sys.argv[4]) if len(sys.argv) > 4 else None
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC] + (["-t", str(LIMIT)] if LIMIT else []) +
                       ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", probe["r_frame_rate"],
                        "-i", "-", "-i", SRC, "-map", "0:v", "-map", "1:a", "-c:v", "h264_nvenc", "-preset", "p6", "-rc", "vbr",
                        "-cq", "16", "-b:v", "40M", "-maxrate", "60M", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest",
                        "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
fs = W * H * 3; i = 0
while True:
    buf = dec.stdout.read(fs)
    if len(buf) < fs: break
    raw = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    t = i / FPS
    m = person_mask(raw, i)
    lyr, bg, neg = layers(t)
    fr = raw.astype(np.float32)
    if neg: fr = 255 - fr
    if bg.any():
        a = (bg * (1 - m))[..., None]
        fr = fr * (1 - a) + np.abs(255 - fr) * a
    if lyr.any():
        a = lyr[..., None]
        fr = fr * (1 - a) + np.abs(255 - fr) * a
    enc.stdin.write(fr.clip(0, 255).astype(np.uint8).tobytes()); i += 1
    if i % 50 == 0: print(i, file=sys.stderr, flush=True)
enc.stdin.close(); enc.wait(); print("frames", i)
