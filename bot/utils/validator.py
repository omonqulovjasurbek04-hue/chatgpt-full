import urllib.parse

def is_valid_url(url: str) -> bool:
    """URL to'g'riligini tekshirish"""
    try:
        result = urllib.parse.urlparse(url)
        return result.scheme in ('http', 'https') and bool(result.netloc)
    except (ValueError, AttributeError):
        return False
