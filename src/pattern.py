patterns = [
    # Basic patterns with exact matches
    r'المة\s*:\s*(\d+)',                    # Basic Arabic with colon
    r'ﻼﻣﺔ\s*:\s*(\d+)',                    # Encoded Arabic with colon
    r'ة\s*الم\s*:\s*(\d+)',                 # Separated Arabic with colon
    
    # Patterns with optional colon
    r'المة\s*:?\s*(\d+)',                   # Basic Arabic with optional colon
    r'ﻼﻣﺔ\s*:?\s*(\d+)',                   # Encoded Arabic with optional colon
    r'ة\s*الم\s*:?\s*(\d+)',                # Separated Arabic with optional colon
    
    # Category word patterns
    r'فئة\s*(\d+)',                         # Basic category word
    r'ﻓﺌﺔ\s*([١\d]+)',                      # Encoded category word with Arabic numerals
    r'الفئة\s*(\d+)',                       # Category word with 'ال'
    r'ﺍﻟﻔﺌﺔ\s*([١\d]+)',                    # Encoded category word with 'ال' and Arabic numerals
    
    # Combined patterns with OR operator
    r'المة\s*:?\s*(\d+)|فئة\s*(\d+)',       # Basic Arabic with category word
    r'ﻼﻣﺔ\s*:?\s*(\d+)|ﻓﺌﺔ\s*([١\d]+)',     # Encoded Arabic with category word
    
    # Patterns with flexible whitespace
    r'المة[\s\n]*:[\s\n]*(\d+)',           # Basic Arabic with flexible whitespace
    r'ﻼﻣﺔ[\s\n]*:[\s\n]*(\d+)',           # Encoded Arabic with flexible whitespace
    r'ة[\s\n]*الم[\s\n]*:[\s\n]*(\d+)',    # Separated Arabic with flexible whitespace
    
    # Patterns with optional text before/after
    r'[ـ\s]*فئات\s*الع[ـ\s]*المة\s*:?\s*(\d+)',  # With optional dashes and spaces
    r'[ـ\s]*فئات\s*الع[ـ\s]*ة\s*الم\s*:?\s*(\d+)',  # Separated version with optional dashes
    
    # Patterns for category references in text
    r'بالفئة\s*(\d+)',                      # Reference to category in text
    r'ﺑﺎﻟﻔﺌﺔ\s*([١\d]+)',                   # Encoded reference to category
    
    # Numbers in both formats
    r'المة\s*:?\s*([١٢٣٤٥٦٧٨٩٠\d]+)',      # Supporting both Arabic and standard numerals
    r'ﻼﻣﺔ\s*:?\s*([١٢٣٤٥٦٧٨٩٠\d]+)',      # Encoded version with both numeral types
    
    # Most flexible patterns (use with caution as they might be too permissive)
    r'(?:المة|ﻼﻣﺔ|ة\s*الم)\s*:?\s*(\d+)',  # All variants in one pattern
    r'(?:فئة|ﻓﺌﺔ|الفئة|ﺍﻟﻔﺌﺔ)\s*([١\d]+)'  # All category word variants in one pattern
]

pattern_req = [
    # Original exact pattern
    r'[ﻗق][ﺪد][ﻡم]\s*[ﻋع][ﻨن][ﻬه]\s*[ﺍا][ﻁط][ﻠل][ﺐب]\s*[ﺭر][ﻗق][ﻢم]\s*[: .-]\s*(\d+)',
    
    # Handling potential spacing and encoding variations
    r'[ﻗق]{1,2}\s*[ﺪد]{1,2}\s*[ﻡم]{1,2}\s*[ﻋع]{1,2}\s*[ﻨن]{1,2}\s*[ﻬه]{1,2}\s*[ﺍا]{1,2}\s*[ﻁط]{1,2}\s*[ﻠل]{1,2}\s*[ﺐب]{1,2}\s*[ﺭر]{1,2}\s*[ﻗق]{1,2}\s*[ﻢم]{1,2}\s*[: .-]\s*(\d+)',
    
    # More flexible matching with optional characters and spaces
    r'[ﻗق][\u200c\u200d]?[ﺪد]\s*[ﻋع][\u200c\u200d]?[ﻨن]\s*[ﻬه]\s*[ﺍا][ﻁط][ﻠل][ﺐب]\s*[ﺭر][ﻗق][ﻢم]\s*[: .-]\s*(\d+)',
    
    # Handling potential additional whitespace or hidden characters
    r'.*?[ﻗق][ﺪد]\s*[ﻋع][ﻨن]\s*[ﻬه]\s*[ﺍا][ﻁط][ﻠل][ﺐب]\s*[ﺭر][ﻗق][ﻢم]\s*[: .-]\s*(\d+)',
    
    # Most flexible pattern (use cautiously)
    r'[ﻗق].*?[ﻋع].*?[ﻁط].*?[ﺭر].*?[ﻢم]\s*[: .-]\s*(\d+)',
     r'ﻗﺪﻡ ﻋﻨﻬﺎ ﻁﻠﺐ ﺭﻗﻢ :\s*(\d+)'
]