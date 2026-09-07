import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from compose import compose, layout, verify, read_rgb


class CompositionTests(unittest.TestCase):
    def test_preservation_aspects_and_versions(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sketch = root/'raw.png'
            Image.linear_gradient('L').resize((320,180)).convert('RGB').save(sketch)
            for i,size in enumerate([(600,100),(200,220),(200,200)]):
                photo = root/f'photo{i}.png'
                Image.effect_noise(size,70).convert('RGB').save(photo)
                g = layout(photo,300)
                self.assertEqual(g['photo_box'],[0,0,300,round(300*size[1]/size[0])])
                self.assertEqual(g['sketch_box'][1],g['photo_box'][3])
                result = compose(photo, sketch,root, f'case{i}',300)
                self.assertTrue(result['passed'])
                again = compose(photo, sketch,root, f'case{i}',300)
                self.assertNotEqual(result['final'],again['final'])
                final=Image.open(result['final']).convert('RGB')
                x,y,_,_=g['photo_box']; final.putpixel((x,y),(255,0,0)); final.save(result['final'])
                with self.assertRaises(ValueError): verify(result['manifest'])

    def test_exif_and_transparency(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'rotation.jpg'
            exif=Image.Exif(); exif[274]=6
            Image.new('RGB',(30,50),'red').save(p,exif=exif)
            self.assertEqual(read_rgb(p)[0].size,(50,30))
            a=Path(td)/'alpha.png'; Image.new('RGBA',(20,20),(0,0,0,0)).save(a)
            rgb,has_alpha=read_rgb(a)
            self.assertTrue(has_alpha); self.assertEqual(rgb.getpixel((0,0)),(245,241,232))

    def test_bad_width(self):
        with self.assertRaises(ValueError): layout('unused',301)

    def test_tall_photo_needs_explicit_layout_choice(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'tall.png'
            Image.new('RGB',(100,600),'blue').save(p)
            with self.assertRaisesRegex(ValueError,'Ask user'): layout(p,300)

    def test_sharp_ink_upscale_does_not_exceed_paper(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); p=root/'photo.png'; s=root/'ink.png'
            Image.new('RGB',(20,10),'blue').save(p)
            ink=Image.new('RGB',(20,10),(245,241,232))
            for y in range(10): ink.putpixel((10,y),(0,0,0))
            ink.save(s)
            self.assertTrue(compose(p,s,root,'sharp',300)['passed'])


if __name__=='__main__': unittest.main()
