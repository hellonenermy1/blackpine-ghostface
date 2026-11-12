import unittest
from io import BytesIO
from math import isinf
from unittest.mock import patch
from PIL import Image, PngImagePlugin
from ghostface.image_tools import decode, sanitize_png, pixel_quality, ImageInputError

def fixture(mode='RGB', size=(8, 6), fmt='PNG', **kwargs):
    buf = BytesIO()
    Image.new(mode, size).save(buf, format=fmt, **kwargs)
    return buf.getvalue()

class ImageToolsTests(unittest.TestCase):
    def test_png(self):
        im, info = decode(fixture())
        self.assertEqual((info.format, info.width, info.height), ('PNG', 8, 6))
        self.assertEqual(im.mode, 'RGB')
    def test_jpeg(self):
        self.assertEqual(decode(fixture(fmt='JPEG'))[1].format, 'JPEG')
    def test_alpha(self):
        out, info = sanitize_png(fixture(mode='RGBA'))
        self.assertTrue(info.has_alpha)
        self.assertEqual(decode(out)[0].mode, 'RGBA')
    def test_text_removed(self):
        meta = PngImagePlugin.PngInfo(); meta.add_text('Comment', 'private test metadata')
        out, _ = sanitize_png(fixture(pnginfo=meta))
        with Image.open(BytesIO(out)) as im:
            self.assertNotIn('Comment', im.info)
    def test_exif_orientation_and_removal(self):
        exif = Image.Exif(); exif[274] = 6; exif[315] = 'test author'
        out, info = sanitize_png(fixture(fmt='JPEG', exif=exif))
        self.assertEqual((info.width, info.height), (6, 8))
        with Image.open(BytesIO(out)) as im:
            self.assertFalse(im.getexif())
    def test_invalid(self):
        for bad in (b'', b'not image', b'\x89PNG\r\n\x1a\n', 'bad'):
            with self.subTest(bad=bad), self.assertRaises(ImageInputError): decode(bad)
    def test_byte_limit(self):
        with patch('ghostface.image_tools.MAX_BYTES', 5), self.assertRaises(ImageInputError): decode(fixture())
    def test_pixel_limit(self):
        with patch('ghostface.image_tools.MAX_PIXELS', 47), self.assertRaises(ImageInputError): decode(fixture())
    def test_unsupported_format(self):
        with self.assertRaises(ImageInputError): decode(fixture(fmt='BMP'))
    def test_animation(self):
        b=BytesIO(); Image.new('RGB',(8,6)).save(b,format='PNG',save_all=True,append_images=[Image.new('RGB',(8,6),'white')],duration=100)
        with self.assertRaises(ImageInputError): decode(b.getvalue())
    def test_profile_rejected(self):
        with self.assertRaises(ImageInputError): decode(fixture(icc_profile=b'test profile'))
    def test_cmyk_rejected(self):
        with self.assertRaises(ImageInputError): decode(fixture(mode='CMYK',fmt='JPEG'))
    def test_exact_fidelity(self):
        im=Image.new('RGB',(2,2),'white'); result=pixel_quality(im,im.copy())
        self.assertTrue(result['identical']); self.assertTrue(isinf(result['psnr_db']))
    def test_known_mse(self):
        a=Image.new('RGB',(2,2),(0,0,0)); b=Image.new('RGB',(2,2),(1,1,1))
        self.assertEqual(pixel_quality(a,b)['mse'],1)
        self.assertAlmostEqual(pixel_quality(a,b)['psnr_db'],48.1308036)
    def test_metric_rejects_mismatch(self):
        with self.assertRaises(ValueError): pixel_quality(Image.new('RGB',(2,2)),Image.new('RGB',(3,2)))
    def test_metric_rejects_alpha(self):
        with self.assertRaises(ValueError): pixel_quality(Image.new('RGBA',(2,2)),Image.new('RGBA',(2,2)))
    def test_pixels_preserved(self):
        original=fixture(); out,_=sanitize_png(original)
        self.assertTrue(pixel_quality(decode(original)[0],decode(out)[0])['identical'])
