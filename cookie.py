import re, string

_semispacejoin = '; '.join

_LegalCharsPatt  = r"[\w\d!#%&'~_`><@,:/\$\*\+\-\.\^\|\)\(\?\}\{\=]"

_CookiePattern = re.compile(
    r"(?x)"                       # This is a Verbose pattern
    r"(?P<key>"                   # Start of group 'key'
    ""+ _LegalCharsPatt +"+?"     # Any word of at least one letter, nongreedy
    r")"                          # End of group 'key'
    r"\s*=\s*"                    # Equal Sign
    r"(?P<val>"                   # Start of group 'val'
    r'"(?:[^\\"]|\\.)*"'            # Any doublequoted string
    r"|"                            # or
    r"\w{3},\s[\s\w\d-]{9,11}\s[\d:]{8}\sGMT" # Special case for "expires" attr
    r"|"                            # or
    ""+ _LegalCharsPatt +"*"        # Any word or empty string
    r")"                          # End of group 'val'
    r"\s*;?"                      # Probably ending in a semi-colon
    )

_LegalChars       = string.ascii_letters + string.digits + "!#$%&'*+-.^_`|~"

_Translator       = {
    '\000' : '\\000',  '\001' : '\\001',  '\002' : '\\002',
    '\003' : '\\003',  '\004' : '\\004',  '\005' : '\\005',
    '\006' : '\\006',  '\007' : '\\007',  '\010' : '\\010',
    '\011' : '\\011',  '\012' : '\\012',  '\013' : '\\013',
    '\014' : '\\014',  '\015' : '\\015',  '\016' : '\\016',
    '\017' : '\\017',  '\020' : '\\020',  '\021' : '\\021',
    '\022' : '\\022',  '\023' : '\\023',  '\024' : '\\024',
    '\025' : '\\025',  '\026' : '\\026',  '\027' : '\\027',
    '\030' : '\\030',  '\031' : '\\031',  '\032' : '\\032',
    '\033' : '\\033',  '\034' : '\\034',  '\035' : '\\035',
    '\036' : '\\036',  '\037' : '\\037',

    # Because of the way browsers really handle cookies (as opposed
    # to what the RFC says) we also encode , and ;

    ',' : '\\054', ';' : '\\073',

    '"' : '\\"',       '\\' : '\\\\',

    '\177' : '\\177',  '\200' : '\\200',  '\201' : '\\201',
    '\202' : '\\202',  '\203' : '\\203',  '\204' : '\\204',
    '\205' : '\\205',  '\206' : '\\206',  '\207' : '\\207',
    '\210' : '\\210',  '\211' : '\\211',  '\212' : '\\212',
    '\213' : '\\213',  '\214' : '\\214',  '\215' : '\\215',
    '\216' : '\\216',  '\217' : '\\217',  '\220' : '\\220',
    '\221' : '\\221',  '\222' : '\\222',  '\223' : '\\223',
    '\224' : '\\224',  '\225' : '\\225',  '\226' : '\\226',
    '\227' : '\\227',  '\230' : '\\230',  '\231' : '\\231',
    '\232' : '\\232',  '\233' : '\\233',  '\234' : '\\234',
    '\235' : '\\235',  '\236' : '\\236',  '\237' : '\\237',
    '\240' : '\\240',  '\241' : '\\241',  '\242' : '\\242',
    '\243' : '\\243',  '\244' : '\\244',  '\245' : '\\245',
    '\246' : '\\246',  '\247' : '\\247',  '\250' : '\\250',
    '\251' : '\\251',  '\252' : '\\252',  '\253' : '\\253',
    '\254' : '\\254',  '\255' : '\\255',  '\256' : '\\256',
    '\257' : '\\257',  '\260' : '\\260',  '\261' : '\\261',
    '\262' : '\\262',  '\263' : '\\263',  '\264' : '\\264',
    '\265' : '\\265',  '\266' : '\\266',  '\267' : '\\267',
    '\270' : '\\270',  '\271' : '\\271',  '\272' : '\\272',
    '\273' : '\\273',  '\274' : '\\274',  '\275' : '\\275',
    '\276' : '\\276',  '\277' : '\\277',  '\300' : '\\300',
    '\301' : '\\301',  '\302' : '\\302',  '\303' : '\\303',
    '\304' : '\\304',  '\305' : '\\305',  '\306' : '\\306',
    '\307' : '\\307',  '\310' : '\\310',  '\311' : '\\311',
    '\312' : '\\312',  '\313' : '\\313',  '\314' : '\\314',
    '\315' : '\\315',  '\316' : '\\316',  '\317' : '\\317',
    '\320' : '\\320',  '\321' : '\\321',  '\322' : '\\322',
    '\323' : '\\323',  '\324' : '\\324',  '\325' : '\\325',
    '\326' : '\\326',  '\327' : '\\327',  '\330' : '\\330',
    '\331' : '\\331',  '\332' : '\\332',  '\333' : '\\333',
    '\334' : '\\334',  '\335' : '\\335',  '\336' : '\\336',
    '\337' : '\\337',  '\340' : '\\340',  '\341' : '\\341',
    '\342' : '\\342',  '\343' : '\\343',  '\344' : '\\344',
    '\345' : '\\345',  '\346' : '\\346',  '\347' : '\\347',
    '\350' : '\\350',  '\351' : '\\351',  '\352' : '\\352',
    '\353' : '\\353',  '\354' : '\\354',  '\355' : '\\355',
    '\356' : '\\356',  '\357' : '\\357',  '\360' : '\\360',
    '\361' : '\\361',  '\362' : '\\362',  '\363' : '\\363',
    '\364' : '\\364',  '\365' : '\\365',  '\366' : '\\366',
    '\367' : '\\367',  '\370' : '\\370',  '\371' : '\\371',
    '\372' : '\\372',  '\373' : '\\373',  '\374' : '\\374',
    '\375' : '\\375',  '\376' : '\\376',  '\377' : '\\377'
    }

_idmap = ''.join(chr(x) for x in xrange(256))

def _quote(str, LegalChars=_LegalChars,
           idmap=_idmap, translate=string.translate):
    #
    # If the string does not need to be double-quoted,
    # then just return the string.  Otherwise, surround
    # the string in doublequotes and precede quote (with a \)
    # special characters.
    #
    if "" == translate(str, idmap, LegalChars):
        return str
    else:
        return '"' + _nulljoin( map(_Translator.get, str, str) ) + '"'
# end _quote

class Morsel(dict):
    # RFC 2109 lists these attributes as reserved:
    #   path       comment         domain
    #   max-age    secure      version
    #
    # For historical reasons, these attributes are also reserved:
    #   expires
    #
    # This is an extension from Microsoft:
    #   httponly
    #
    # This dictionary provides a mapping from the lowercase
    # variant on the left to the appropriate traditional
    # formatting on the right.
    _reserved = { "expires" : "expires",
                   "path"        : "Path",
                   "comment" : "Comment",
                   "domain"      : "Domain",
                   "max-age" : "Max-Age",
                   "secure"      : "secure",
                   "httponly"  : "httponly",
                   "version" : "Version",
                   }

    def __init__(self):
        # Set defaults
        self.key = self.value = self.coded_value = None

        # Set default attributes
        for K in self._reserved:
            dict.__setitem__(self, K, "")
    # end __init__

    def __setitem__(self, K, V):
        K = K.lower()
        if not K in self._reserved:
            raise CookieError("Invalid Attribute %s" % K)
        dict.__setitem__(self, K, V)
    # end __setitem__

    def isReservedKey(self, K):
        return K.lower() in self._reserved
    # end isReservedKey

    def set(self, key, val, coded_val,
            LegalChars=_LegalChars,
            idmap=_idmap, translate=string.translate):
        # First we verify that the key isn't a reserved word
        # Second we make sure it only contains legal characters
        if key.lower() in self._reserved:
            raise CookieError("Attempt to set a reserved key: %s" % key)
        if "" != translate(key, idmap, LegalChars):
            raise CookieError("Illegal key value: %s" % key)

        # It's a good key, so save it.
        self.key                 = key
        self.value               = val
        self.coded_value         = coded_val
    # end set

    def output(self, attrs=None, header = "Set-Cookie:"):
        return "%s %s" % ( header, self.OutputString(attrs) )

    __str__ = output

    def __repr__(self):
        return '<%s: %s=%s>' % (self.__class__.__name__,
                                self.key, repr(self.value) )

    def js_output(self, attrs=None):
        # Print javascript
        return """
        <script type="text/javascript">
        <!-- begin hiding
        document.cookie = \"%s\";
        // end hiding -->
        </script>
        """ % ( self.OutputString(attrs).replace('"',r'\"'), )
    # end js_output()

    def OutputString(self, attrs=None):
        # Build up our result
        #
        result = []
        RA = result.append

        # First, the key=value pair
        RA("%s=%s" % (self.key, self.coded_value))

        # Now add any defined attributes
        if attrs is None:
            attrs = self._reserved
        items = self.items()
        items.sort()
        for K,V in items:
            if V == "": continue
            if K not in attrs: continue
            if K == "expires" and type(V) == type(1):
                RA("%s=%s" % (self._reserved[K], _getdate(V)))
            elif K == "max-age" and type(V) == type(1):
                RA("%s=%d" % (self._reserved[K], V))
            elif K == "secure":
                RA(str(self._reserved[K]))
            elif K == "httponly":
                RA(str(self._reserved[K]))
            else:
                RA("%s=%s" % (self._reserved[K], V))

        # Return the result
        return _semispacejoin(result)
    # end OutputString
# end Morsel class

class BaseCookie(dict):
    # A container class for a set of Morsels
    #

    def value_decode(self, val):
        """real_value, coded_value = value_decode(STRING)
        Called prior to setting a cookie's value from the network
        representation.  The VALUE is the value read from HTTP
        header.
        Override this function to modify the behavior of cookies.
        """
        return val, val
    # end value_encode

    def value_encode(self, val):
        """real_value, coded_value = value_encode(VALUE)
        Called prior to setting a cookie's value from the dictionary
        representation.  The VALUE is the value being assigned.
        Override this function to modify the behavior of cookies.
        """
        strval = str(val)
        return strval, strval
    # end value_encode

    def __init__(self, input=None):
        if input: self.load(input)
    # end __init__

    def __set(self, key, real_value, coded_value):
        """Private method for setting a cookie's value"""
        M = self.get(key, Morsel())
        M.set(key, real_value, coded_value)
        dict.__setitem__(self, key, M)
    # end __set

    def __setitem__(self, key, value):
        """Dictionary style assignment."""
        rval, cval = self.value_encode(value)
        self.__set(key, rval, cval)
    # end __setitem__

    def output(self, attrs=None, header="Set-Cookie:", sep="\015\012"):
        """Return a string suitable for HTTP."""
        result = []
        items = self.items()
        items.sort()
        for K,V in items:
            result.append( V.output(attrs, header) )
        return sep.join(result)
    # end output

    __str__ = output

    def __repr__(self):
        L = []
        items = self.items()
        items.sort()
        for K,V in items:
            L.append( '%s=%s' % (K,repr(V.value) ) )
        return '<%s: %s>' % (self.__class__.__name__, _spacejoin(L))

    def js_output(self, attrs=None):
        """Return a string suitable for JavaScript."""
        result = []
        items = self.items()
        items.sort()
        for K,V in items:
            result.append( V.js_output(attrs) )
        return _nulljoin(result)
    # end js_output

    def load(self, rawdata):
        """Load cookies from a string (presumably HTTP_COOKIE) or
        from a dictionary.  Loading cookies from a dictionary 'd'
        is equivalent to calling:
            map(Cookie.__setitem__, d.keys(), d.values())
        """
        if type(rawdata) == type(""):
            self.__ParseString(rawdata)
        else:
            # self.update() wouldn't call our custom __setitem__
            for k, v in rawdata.items():
                self[k] = v
        return
    # end load()

    def __ParseString(self, str, patt=_CookiePattern):
        i = 0            # Our starting point
        n = len(str)     # Length of string
        M = None         # current morsel

        while 0 <= i < n:
            # Start looking for a cookie
            match = patt.search(str, i)
            if not match: break          # No more cookies

            K,V = match.group("key"), match.group("val")
            i = match.end(0)

            # Parse the key, value in case it's metainfo
            if K[0] == "$":
                # We ignore attributes which pertain to the cookie
                # mechanism as a whole.  See RFC 2109.
                # (Does anyone care?)
                if M:
                    M[ K[1:] ] = V
            elif K.lower() in Morsel._reserved:
                if M:
                    M[ K ] = _unquote(V)
            else:
                rval, cval = self.value_decode(V)
                self.__set(K, rval, cval)
                M = self[K]
    # end __ParseString
# end BaseCookie class

class SimpleCookie(BaseCookie):
    """SimpleCookie
    SimpleCookie supports strings as cookie values.  When setting
    the value using the dictionary assignment notation, SimpleCookie
    calls the builtin str() to convert the value to a string.  Values
    received from HTTP are kept as strings.
    """
    def value_decode(self, val):
        return _unquote( val ), val
    def value_encode(self, val):
        strval = str(val)
        return strval, _quote( strval )