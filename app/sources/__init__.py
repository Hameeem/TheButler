from .base import JobSource, NormalizedJob
from .linkedin import LinkedInSource
from .naukri import NaukriSource
from .indeed import IndeedSource
from .internshala import InternshalaSource
from .wellfound import WellfoundSource
from .glassdoor import GlassdoorSource
from .foundit import FounditSource
from .cutshort import CutshortSource

ALL_SOURCES = [
    LinkedInSource(),
    NaukriSource(),
    IndeedSource(),
    InternshalaSource(),
    WellfoundSource(),
    GlassdoorSource(),
    FounditSource(),
    CutshortSource()
]
