# > vdifheader - __utils__.py
# Defines utility methods for tasks such as bit and color manipulation

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

"""
> vdifheader - __utils__.py (private)
Defines utility methods for tasks such as bit and color manipulation
"""
__author__ = "Mars Buttfield-Addison"
__authors__ = [__author__]
__contact__ = "hello@themartianlife.com"
__copyright__ = f"Copyright 2022, {__author__}"
__credits__ = __authors__
__date__ = "2022/04/07"
__deprecated__ = False
__email__ = __contact__
__license__ = "GPLv3"
__maintainer__ = __author__
__status__ = "Pre-release"
__version__ = "0.1"

from os import path, strerror
from sys import stderr
from errno import ENOENT
from pathlib import Path
from datetime import datetime,timezone

try:  # colors if they have them
    import colorama
    colorama.init()
except:  # else don't worry about it
    pass

def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        # add timezone to datetime that has none
        return dt.replace(tzinfo=timezone.utc)
    # otherwise convert from potentially other timezone to correct one
    return dt.astimezone(timezone.utc)

def sanitized_path(filepath: str) -> str:
    """Remove symlinks, home references, and relative segments in path"""
    return str(Path(filepath).expanduser().resolve())


def switch_end(data: str, padded_bits: int=0) -> str:
    """Reverse bits to deal with endianness issues"""
    return "".join(reversed(data)).ljust(padded_bits, "0")


def vh_warn(message: str):
    """Writes message to stdout in red text with ERROR in front"""
    stderr.write(f"\033[0;33mWARNING: {message}.\033[0m\n")


def vh_error(message: str):
    """Writes message to stdout in yellow text with WARNING in front"""
    stderr.write(f"\033[0;31mERROR: {message}.\033[0m\n")


def posint(value: int) -> int:
    int_value = int(value)
    if int_value <= 0:
        raise ValueError(f"NUM_HEADERS must be > 0.")
    return int_value


def filepath(value: str) -> str:
    path_value = sanitized_path(value)
    if not path.exists(path_value):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), path_value)
    return path_value


def station_information(station_id: str) -> str:
    """Checks for station id in included list of known ids"""
    # TODO better central source of more station codes? these ones are from IVS
    # maybe include from e.g. https://ivscc.bkg.bund.de/sessions/stations/
    # TODO also consider possible mark4 transformation mangling?
    # e.g. www.atnf.csiro.au/vlbi/dokuwiki/doku.php/difx/difx2mark4/stationcodes
    known_ids = {
        "Oh": "ERS/VLBI Station O'Higgins, Antarctica",
        "Sy": "JARE Syowa Station, Antarctica",
        "Ag": "Observatorio Argentina-Alemán de Geodesia (AGGO), Argentina",
        "Hb": "Hobart 12m, Mt. Pleasant Radio Observatory, Australia",
        "Ho": "Hobart 26m, Mt. Pleasant Radio Observatory, Australia",
        "Ke": "Katherine, Australia",
        "Mp": "Moprah, Australia",
        "Yg": "Yarragadee, Australia",
        "Pa": "Parkes Observatory, Australia",
        "Ft": "Fortaleza, Radio Observatorio Espacial do Nordes (ROEN), Brazil",
        "Ur": "Nanshan VLBI Station, China",
        "Sh": "Seshan, China",
        "Mh": "Metsähovi Radio Observatory, Finland",
        "Eb": "Effelsberg, Germany",
        "Wz": "Geodetic Observatory Wettzell, Germany",
        "Mc": "Medicina, Italy",
        "Nt": "Noto (Sicily), Italy",
        "Ma": "Matera, Italy",
        "Kb": "Kashima 34m, Japan",
        "K1": "Key Stone Project Kashima 11m, Japan",
        "Kg": "Key Stone Project Koganei, Japan",
        "Ts": "Tsukuba VLBI Station, Japan",
        "Is": "Ishioka VLBI Station, Japan",
        "Mn": "Mizusawa 10m, Japan",
        "Ww": "Warkworth Observatory, New Zealand",
        "Ny": "Ny-Alesund Geodetic Observatory, Norway",
        "Bd": "Radioastronomical Observatory Badary, Russia",
        "Sv": "Svetloe Radio Astronomy Observatory, Russia",
        "Zc": "Radioastronomical Observatory Zelenchukskaya, Russia",
        "Yb": "IGN Yebes Observatory, Spain",
        "Hh": "Hartebeesthoek Radio Astronomy Observatory, South Africa",
        "Kv": "Sejong Station, South Korea",
        "On": "Onsala Space Observatory, Sweden",
        "Sm": "Simeiz, Ukraine",
        "Gs": "Goddard Geophysical and Astronomical Observatory, USA",
        "Gg": "Goddard Geophysical and Astronomical Observatory, USA",
        "Wf": "Westford Antenna, Haystack Observatory, USA",
        "Kk": "Kokee Park Geophysical Observatory, USA",
    }
    return known_ids.get(station_id, "Unknown Station")
