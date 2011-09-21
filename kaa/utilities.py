import bitlyapi

bitly = bitlyapi.BitLy(
        'voxinfinitus', 
        'R_d3664470e5404623b5c0e3a25a873286', 
        )

def unescape(s):
    html_codes = (
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    ('\'', '&#39;'),
    )
    
    for code in html_codes:
        s = s.replace(code[-1], code[0])
    
    return s

