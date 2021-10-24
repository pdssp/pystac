# -*- coding: utf-8 -*-
# pySTAC - Library implementing STAC protocole
# Copyright (C) 2021 - CNES (Jean-Christophe Malapert for Pôle Surfaces Planétaires)
#
# This file is part of pySTAC.
#
# pySTAC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pySTAC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pySTAC.  If not, see <https://www.gnu.org/licenses/>.
"""Library implementing STAC protocole"""
import logging.config
import os
from logging import NullHandler

from ._version import __author__
from ._version import __author_email__
from ._version import __copyright__
from ._version import __description__
from ._version import __license__
from ._version import __name_soft__
from ._version import __title__
from ._version import __url__
from ._version import __version__
from .constants import CommonMediaType
from .constants import IANARelationTypes
from .constants import LicenseType
from .constants import MediaType
from .constants import MediaTypeAsset
from .constants import RelationTypes
from .constants import RoleAsset
from .constants import RoleType
from .custom_logging import LogRecord
from .custom_logging import UtilsLogs
from .exception import ValueNotFindInEnumError
from .pystac import AssetObject
from .pystac import ExtentObject
from .pystac import Link
from .pystac import Properties
from .pystac import Provider
from .pystac import PystacLib as PySTAC
from .pystac import RangeObject
from .pystac import SpatialExtentObject
from .pystac import StacCatalog
from .pystac import StacCollection
from .pystac import StacItem
from .pystac import TemporalExtentObject

logging.getLogger(__name__).addHandler(NullHandler())

UtilsLogs.add_logging_level("TRACE", 15)
try:
    PATH_TO_CONF = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(
        os.path.join(PATH_TO_CONF, "logging.conf"),
        disable_existing_loggers=False,
    )
    logging.debug(
        "file %s loaded" % os.path.join(PATH_TO_CONF, "logging.conf")
    )
except Exception as exception:  # pylint: disable=broad-except
    logging.warning("cannot load logging.conf : %s" % exception)
logging.setLogRecordFactory(LogRecord)  # pylint: disable=no-member

__all__ = [
    "PySTAC",
    "StacCatalog",
    "StacCollection",
    "StacItem",
    "ExtentObject",
    "Properties",
    "SpatialExtentObject",
    "TemporalExtentObject",
    "CommonMediaType",
    "MediaType",
    "MediaTypeAsset",
    "RelationTypes",
    "IANARelationTypes",
    "RoleType",
    "RoleAsset",
    "LicenseType",
    "Provider",
    "AssetObject",
    "Link",
    "RangeObject",
    "ValueNotFindInEnumError",
]
