"""Deterministic photo preservation and ivory monochrome composition. Python 3 + Pillow."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageChops, ImageOps

PAPER = (245, 241, 232)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_rgb(path):
    with Image.open(path) as im:
        if getattr(im, 'n_frames', 1) != 1:
            raise ValueError('Animated/multiframe input is unsupported; choose one frame explicitly.')
        im = ImageOps.exif_transpose(im)
        alpha = 'A' in im.getbands() or 'transparency' in im.info
        if alpha:
            rgba = im.convert('RGBA')
            base = Image.new('RGBA', rgba.size, PAPER + (255,))
            im = Image.alpha_composite(base, rgba)
        return im.convert('RGB'), alpha


def fit_size(size, box):
    scale = min(box[0] / size[0], box[1] / size[1])
    return (max(1, round(size[0] * scale)), max(1, round(size[1] * scale)))


def layout(photo, width=1800):
    if width < 300 or width % 3:
        raise ValueError('Width must be >=300 and divisible by 3.')
    height = width * 4 // 3
    im, alpha = read_rgb(photo)
    top_h = round(width * im.height / im.width)
    if height-top_h < round(height*.15):
        raise ValueError('Full-width uncropped photo leaves less than 15% for the sketch on a 3:4 canvas. Ask user to choose a taller canvas or permit photo cropping; do not silently add borders or crop.')
    photo_box = [0, 0, width, top_h]
    return dict(canvas=[width, height], paper=list(PAPER), margin=0, gap=0,
                layout_mode='full_bleed_photo',
                top_region=photo_box, photo_box=photo_box,
                sketch_box=[0, top_h, width, height-top_h], alpha_composited=alpha)


def mono(im):
    # Remove chroma while preserving every tonal step, avoiding thresholded pencil loss.
    gray = ImageOps.grayscale(im)
    return Image.merge('RGB', tuple(gray.point([round(v*c/255) for v in range(256)]) for c in PAPER))


def compose(photo, sketch, output_dir, name='concept', width=1800):
    if not re.fullmatch(r'[\w\-]+', name, flags=re.UNICODE):
        raise ValueError('Name must contain only letters, numbers, underscore or hyphen.')
    photo, sketch = Path(photo).resolve(), Path(sketch).resolve()
    p, _ = read_rgb(photo)
    s, _ = read_rgb(sketch)
    geometry = layout(photo, width)
    canvas = Image.new('RGB', geometry['canvas'], PAPER)
    x,y,w,h = geometry['photo_box']
    canvas.paste(p.resize((w,h), Image.Resampling.LANCZOS), (x,y))
    sx,sy,sw,sh = geometry['sketch_box']
    panel = Image.new('RGB', (sw,sh), PAPER)
    # Convert near-ivory source paper to white luminance before tinting back to PAPER.
    # Source should already be single-medium; this is not a substitute for visual QA.
    gray = ImageOps.grayscale(s)
    paper_luma = round(.299*245 + .587*241 + .114*232)
    gray = gray.point([min(255, round(v*255/paper_luma)) for v in range(256)])
    normalized = mono(gray.convert('RGB'))
    target = fit_size(normalized.size, (sw,sh))
    normalized = normalized.resize(target, Image.Resampling.LANCZOS)
    # Re-project after resize so interpolation cannot leave the black-to-ivory ramp.
    r = normalized.getchannel('R').point([min(v,245) for v in range(256)])
    normalized = Image.merge('RGB', (r, r.point([round(v*241/245) for v in range(256)]),
                                      r.point([round(v*232/245) for v in range(256)])))
    panel.paste(normalized, ((sw-target[0])//2,(sh-target[1])//2))
    canvas.paste(panel, (sx,sy))
    dest = Path(output_dir).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    version = 1
    while True:
        stem = f'{name}-v{version}'
        manifest = dest / f'{stem}.json'
        final = dest / f'{stem}.png'
        lower = dest / f'{stem}-sketch.png'
        if final.exists() or lower.exists():
            version += 1
            continue
        try:
            handle = manifest.open('x', encoding='utf-8')
            break
        except FileExistsError:
            version += 1
    data = dict(schema_version=2, **geometry, photo=str(photo), raw_sketch=str(sketch),
                photo_sha256=sha(photo), raw_sketch_sha256=sha(sketch),
                final=str(final), sketch=str(lower),
                photo_policy='EXIF orientation + RGB decode + proportional Lanczos resize; no crop or retouch',
                sketch_policy='black-to-ivory tonal normalization, proportional contain; visual QA required')
    with handle:
        canvas.save(final, format='PNG')
        panel.save(lower, format='PNG')
        json.dump(data, handle, ensure_ascii=False, indent=2)
    return {'manifest': str(manifest), **verify(manifest)}


def verify(manifest):
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    p,_ = read_rgb(data['photo'])
    final,_ = read_rgb(data['final'])
    lower,_ = read_rgb(data['sketch'])
    x,y,w,h = data['photo_box']
    sx,sy,sw,sh = data['sketch_box']
    expected = p.resize((w,h), Image.Resampling.LANCZOS)
    diff = ImageChops.difference(final.crop((x,y,x+w,y+h)), expected)
    pixels = lower.get_flattened_data() if hasattr(lower,'get_flattened_data') else lower.getdata()
    invalid = sum(1 for r,g,b in pixels if r>245 or abs(g-round(r*241/245))>1 or abs(b-round(r*232/245))>1)
    checks = dict(ratio_3_4=final.width*4==final.height*3,
                  exact_dimensions=list(final.size)==data['canvas'],
                  source_unchanged=sha(data['photo'])==data['photo_sha256'],
                  raw_sketch_unchanged=sha(data['raw_sketch'])==data['raw_sketch_sha256'],
                  photo_pixels_identical=diff.getbbox() is None,
                  independent_panel_matches=lower.size==(sw,sh) and ImageChops.difference(lower,final.crop((sx,sy,sx+sw,sy+sh))).getbbox() is None,
                  monochrome_on_ivory=invalid==0)
    if data.get('layout_mode') == 'full_bleed_photo':
        checks['borderless_photo_and_direct_join'] = (x==0 and y==0 and w==final.width and sx==0 and sy==h and sw==final.width and sy+sh==final.height)
    if not all(checks.values()):
        raise ValueError(json.dumps(checks))
    return dict(passed=True, checks=checks, final=data['final'], sketch=data['sketch'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    a = sub.add_parser('layout'); a.add_argument('--photo', required=True); a.add_argument('--width', type=int, default=1800)
    a = sub.add_parser('compose'); a.add_argument('--photo', required=True); a.add_argument('--sketch', required=True)
    a.add_argument('--output-dir', required=True); a.add_argument('--name', default='concept'); a.add_argument('--width', type=int, default=1800)
    a = sub.add_parser('verify'); a.add_argument('--manifest', required=True)
    args = vars(parser.parse_args()); command = args.pop('command')
    result = {'layout':layout, 'compose':compose, 'verify':verify}[command](**args)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
