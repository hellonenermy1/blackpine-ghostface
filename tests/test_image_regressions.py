import unittest
from io import BytesIO
from PIL import Image, features, PngImagePlugin
from ghostface.image_tools import decode, sanitize_png, ImageInputError, pixel_quality

class RegressionTests(unittest.TestCase):
    def encode(self, image, fmt='PNG', **kwargs):
        b=BytesIO()
        image.save(b,format=fmt,**kwargs)
        return b.getvalue()

    @unittest.skipUnless(features.check('webp'), 'WebP unavailable')
    def test_webp_lossless(self):
        image=Image.new('RGB',(13,17),(11,22,33))
        out,info=sanitize_png(self.encode(image,'WEBP',lossless=True))
        self.assertEqual(info.format,'WEBP')
        self.assertTrue(pixel_quality(image,decode(out)[0])['identical'])

    def test_palette_transparency(self):
        image=Image.new('P',(3,4),0)
        image.putpalette([255,0,0]+[0,0,0]*255)
        out,info=sanitize_png(self.encode(image,transparency=0))
        self.assertTrue(info.has_alpha)
        self.assertEqual(decode(out)[0].getpixel((0,0)),(255,0,0,0))

    def test_partial_alpha(self):
        image=Image.new('RGBA',(4,4),(200,100,50,127))
        out,_=sanitize_png(self.encode(image))
        self.assertEqual(decode(out)[0].tobytes(),image.tobytes())

    def test_grayscale(self):
        image=Image.new('L',(5,5),42)
        out,_=sanitize_png(self.encode(image))
        self.assertEqual(decode(out)[0].getpixel((0,0)),(42,42,42))

    def test_unicode_metadata_removed(self):
        metadata=PngImagePlugin.PngInfo()
        metadata.add_itxt('Description','private test — 測試')
        out,_=sanitize_png(self.encode(Image.new('RGB',(3,3)),pnginfo=metadata))
        with Image.open(BytesIO(out)) as image:
            self.assertNotIn('Description',image.info)

    def test_truncation(self):
        data=self.encode(Image.new('RGB',(12,12),'red'))
        with self.assertRaises(ImageInputError): decode(data[:len(data)//2])

    def test_no_input_mutation(self):
        data=self.encode(Image.new('RGB',(3,3),'blue'))
        original=bytes(data)
        sanitize_png(data)
        self.assertEqual(data,original)
