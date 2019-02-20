"""
KUEventParser Library
---------------------
KUEventParser is a library to parse events of Kyoto_univ
usage:
   >>> import kueventparser
   >>> events = kueventparser.get_all(2019,1)
   >>> list(events)
   [<events.Events
The other  methods are supported - see `kueventparser.api`. Full documentation
is got by sphinx .
:copyright: (c) 2019 by kkiyama117.
:license: MIT, see LICENSE for more details.
"""

from .api import kueventparser, get, get_all
from .core import event_parser

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __maintainer__, __maintainer_email__


