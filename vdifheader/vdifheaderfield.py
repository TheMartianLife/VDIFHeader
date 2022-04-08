"""
> vdifheader - vdifheaderfield.py
Defines VDIFHeaderField class that represents a single field within a VDIFHeader

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
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

from vdifheader.__utils__ import Validity


class VDIFHeaderField:
    """A class that represents a single field within a VDIFHeader object"""

    ######## PUBLIC FUNCTIONS

    def __init__(self, name, value, raw_value, validity):
        self._name = name
        self.value = value
        self.raw_value = raw_value
        self.validity = validity
        self.__validity_test = None
        self.__always_valid = False

    ######## PRIVATE FUNCTIONS

    def __repr__(self):
        """Defines pretty print string representation of object"""
        return f"<VDIFHeaderField _name={self._name}, value={self.value}>"

    def __str__(self):
        """Defines string representation of object"""
        return f"{self.value}"

    def __eq__(self, other):
        """Defines field equality to include a primitive equal to field value"""
        if other is VDIFHeaderField:
            return (
                self._name == other._name
                and self.value == other.value
                and self._raw_value == other._raw_value
                and self._validity == other._validity
            )
        else:
            # allows e.g. field whose .value is 1 to == 1
            return self.value == other

    ######## INTERNAL FUNCTIONS

    def _set_validity_test(self, validity_test, validity, message):
        """Stores given validity test for field value"""
        self.__validity_test = (validity_test, validity, message)
        return

    def _set_always_valid(self):
        """Sets validity test to always pass for this field"""
        self.__always_valid = True
        return

    def _revalidate(self):
        """Updates validity based on current value versus field constraints"""
        if self.__always_valid:
            return (Validity.VALID, None)
        elif self.__validity_test is None:
            self.validity = Validity.UNKNOWN
            default_message = "no known validity test for field {self._name}"
            return (Validity.UNKNOWN, default_message)
        validity_test, failure_validity, message = self.__validity_test
        test_success = validity_test(self.value)
        if test_success:
            self.validity = Validity.VALID
        elif not test_success:
            self.validity = failure_validity
        return (self.validity, message)
