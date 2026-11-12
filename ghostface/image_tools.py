"""Local image privacy utilities; no identity protection or network operations."""
from dataclasses import dataclass
from io import BytesIO
from math import log10, inf
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_BYTES = 15_000_000
MAX_PIXELS = 24_000_000
FORMATS = frozenset({'JPEG', 'PNG', 'WEBP'})

class ImageInputError(ValueError):
    """Invalid, unsupported or oversized image."""

@dataclass(frozen=True)
class ImageInfo:
    format: str
    width: int
    height: int
    has_alpha: bool

def _check_header(im):
    if im.format not in FORMATS:
        raise ImageInputError('Unsupported image format')
    if im.width < 1 or im.height < 1 or im.width * im.height > MAX_PIXELS:
        raise ImageInputError('Decoded pixel limit exceeded')
    if getattr(im, 'n_frames', 1) != 1:
        raise ImageInputError('Animated images are unsupported')

def decode(data: bytes):
    """Decode one bounded image, apply orientation and preserve pixel alpha."""
    if not isinstance(data, bytes) or not 0 < len(data) <= MAX_BYTES:
        raise ImageInputError('Input must be 1–15,000,000 bytes')
    try:
        with Image.open(BytesIO(data)) as im:
            _check_header(im)
            fmt = im.format
            im.verify()
        with Image.open(BytesIO(data)) as im:
            _check_header(im)
            im.load()
            oriented = ImageOps.exif_transpose(im)
            alpha = 'A' in oriented.getbands() or 'transparency' in oriented.info
            if oriented.mode not in {'RGB', 'RGBA', 'L', 'LA', 'P', '1'}:
                raise ImageInputError('Unsupported color mode')
            if oriented.info.get('icc_profile'):
                raise ImageInputError('Embedded color profile requires color-managed export')
            pixels = oriented.convert('RGBA' if alpha else 'RGB')
            clean = Image.new(pixels.mode, pixels.size)
            clean.paste(pixels)
            return clean, ImageInfo(fmt, clean.width, clean.height, alpha)
    except ImageInputError:
        raise
    except (OSError, ValueError, SyntaxError, UnidentifiedImageError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ImageInputError('Image cannot be safely decoded') from exc

def sanitize_png(data: bytes) -> tuple[bytes, ImageInfo]:
    """Re-encode decoded pixels without copying source metadata; no protection claim."""
    pixels, info = decode(data)
    with BytesIO() as output:
        pixels.save(output, format='PNG')
        return output.getvalue(), info

def pixel_quality(reference: Image.Image, candidate: Image.Image) -> dict:
    """Exact RGB fidelity metrics for same-size opaque images; not an AI score."""
    if reference.size != candidate.size or reference.mode != 'RGB' or candidate.mode != 'RGB':
        raise ValueError('Equal-size RGB images required')
    if reference.width * reference.height > MAX_PIXELS:
        raise ValueError('Pixel limit exceeded')
    a, b = reference.tobytes(), candidate.tobytes()
    mse = sum((x-y)**2 for x,y in zip(a,b)) / len(a)
    return {'mse': mse, 'psnr_db': inf if mse == 0 else 10*log10(255**2/mse), 'identical': mse == 0}
