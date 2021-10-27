# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 - Centre National d'Etudes Spatiales
# jean-christophe.malapert@cnes.fr
#
# This file is part of pystac.
#
# pystac is a free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301  USA
"""The SpatioTemporal Asset Catalog (STAC) family of specifications aim to
standardize the way geospatial asset metadata is structured and queried. A
"spatiotemporal asset" is any file that represents information about the Earth
at a certain place and time. The original focus was on scenes of satellite
imagery, but the specifications now cover a broad variety of uses, including
sources such as aircraft and drone and data such as hyperspectral optical,
synthetic aperture radar (SAR), video, point clouds, lidar, digital elevation
models (DEM), vector, machine learning labels, and composites like NDVI and
mosaics. STAC is intentionally designed with a minimal core and flexible
extension mechanism to support a broad set of use cases.

The STAC specifications define related JSON object types connected by link
relations to support a HATEOAS-style traversable interface and a RESTful API
providing additional browse and search interfaces. Typically, several STAC
specifications are composed together to create an implementation. The Item,
Catalog, and Collection specifications define a minimal core of the most
frequently used JSON object types. Because of the hierarchical structure
between these objects, a STAC catalog can be implemented in a completely
'static' manner as a group of hyperlinked Catalog, Collection, and Item URLs,
enabling data publishers to expose their data as a browsable set of files. If
more complex query abilities are desired, such as spatial or temporal
predicates, the STAC API specification can be implemented as a web service
interface to query over a group of STAC objects, usually held in a database.

To the greatest extent possible, STAC uses and extends existing specifications.
The most important object in STAC is an Item, which is simply a GeoJSON Feature
with a well-defined set of additional attributes ("foreign members"). The STAC
API extends the OGC API - Features - Part 1: Core with additional web service
endpoints and object attributes.
"""
import configparser
import json
import logging
import os
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import shapely
from shapely.geometry import LineString
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPoint
from shapely.geometry import MultiPolygon
from shapely.geometry import Point
from shapely.geometry import Polygon

from ._version import __name_soft__
from .constants import CommonMediaType
from .constants import IANARelationTypes
from .constants import LicenseType
from .constants import MediaType
from .constants import MediaTypeAsset
from .constants import RelationTypes
from .constants import RoleAsset
from .constants import RoleType

# TODO 1: STRONGLY RECOMMENDED. Absolute URL to the location that the Catalog file
# can be found online, if available.
# This is particularly useful when in a download package that includes metadata,
# so that the downstream user can know where the data has come from.
# Remove SELF link when no absolute URL is set

# TODO 2 : Extend enum

# TODO 3 : from typing import Type
#          def process_any_subclass_type_of_A(cls: Type[A]):
#             pass

# TODO 4: Extend Asset Item by loading an extension

# TODO 5 : Extend properties by loading an extension

# TODO Additional attributes relating to an Item should be added into the Item Properties object, rather than directly in the Item object.
# TODO In general, additional attributes that apply to an Item Asset should also be allowed in Item Properties and vice-versa. For example, the eo:bands attribute may be used in Item Properties to describe the aggregation of all bands available in the Item Asset objects contained in the Item, but may also be used in an individual Item Asset to describe only the bands available in that asset.

logger = logging.getLogger(__name__)


class Observable:
    def __init__(self):
        self._observers = list()

    def subscribe(self, observer):
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for obs in self._observers:
            obs.notify(self, *args, **kwargs)

    def unsubscribe(self, observer):
        self._observers.remove(observer)


class Observer:
    def __init__(self, observable):
        observable.subscribe(self)

    def notify(self, observable, *args, **kwargs):
        print("Got", args, kwargs, "From", observable)


class Utils:
    """Utility class."""

    @staticmethod
    def fix_directory_syntax(directory: str) -> str:
        """Check if the directory ends with "/". If yes, remove the "/"

        Args:
            directory (str): the directory path

        Returns:
            str: the directory path
        """
        if directory[-1] == "/":
            directory = directory[:-1]
        return directory


class Link:
    """This object describes a relationship with another entity. Data providers
    are advised to be liberal with links."""

    def __init__(
        self, href: str, rel: Union[RelationTypes, IANARelationTypes]
    ):
        """Constructor

        Args:
            href (str): The actual link in the format of an URL. Relative and
            absolute links are both allowed.
            rel (Union[RelationTypes, IANARelationTypes]): Relationship between
            the current document and the linked document.
        """
        self.__href: str = href
        self.__rel: Union[RelationTypes, IANARelationTypes] = rel
        self.__type: Optional[Union[MediaType, CommonMediaType]] = None
        self.__title: Optional[str] = None

    @property
    def href(self):
        """The actual link in the format of an URL.

        :getter: Returns the href
        :type: str
        """
        return self.__href

    @property
    def rel(self):
        """Relationship between the current document and the linked document.

        :getter: Returns the relationship
        :type: Union[RelationTypes, IANARelationTypes]
        """
        return self.__rel

    @property
    def type(self):
        """Media type of the referenced entity.

        :getter: Returns the media type of the referenced entity
        :setter: Set the media type of the referenced entity
        :type: Union[MediaType, CommonMediaType, None]
        """
        return self.__type

    @type.setter
    def type(self, value: Union[MediaType, CommonMediaType, None]):
        if (
            not isinstance(value, MediaType)
            and not isinstance(value, CommonMediaType)
            and value is not None
        ):
            raise TypeError(
                f"value has type {type(value)} but must have MediaType CommonMediaType type or None"
            )
        self.__type = value

    @property
    def title(self):
        """A human readable title to be used in rendered displays of the link.

        :getter: Returns a human readable title to be used in rendered displays of the link.
        :setter: Set the media type of the referenced entity
        :type: Union[str, None]
        """
        return self.__title

    @title.setter
    def title(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__title = value

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        link = dict()
        link["href"] = self.href
        link["rel"] = self.rel.value
        if self.type is not None:
            link["type"] = self.type.value
        if self.title is not None:
            link["title"] = self.title
        return link

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class Provider:
    """The object provides information about a provider. A provider is any of
    the organizations that captures or processes the content of the Collection
    and therefore influences the data offered by this Collection. May also
    include information about the final storage provider hosting the data."""

    def __init__(self, name: str):
        """Create a provider based on its name

        Args:
            name (str): The name of the organization or the individual.
        """
        self.__name: str = name
        self.__description: Optional[str] = None
        self.__roles: List[RoleType] = list()
        self.__url: Optional[str] = None

    @property
    def name(self):
        """The name of the organization or the individual.

        :getter: Returns the name of the organization or the individual.
        :setter: Set the name
        :type: str
        """
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError(
                f"value has type {type(value)} but must have str type"
            )
        self.__name = value

    @property
    def description(self):
        """Multi-line description to add further provider information such as
        processing details for processors and producers, hosting details for
         hosts or basic contact information. CommonMark 0.29 syntax MAY be used
         for rich text representation.

        :getter: Returns the description.
        :setter: Sets the description
        :type: Union[str, None]
        """
        return self.__description

    @description.setter
    def description(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__description = value

    @property
    def roles(self):
        """Roles of the provider. Any of licensor, producer, processor or host.

        :getter: Returns the role of the provider
        :type: List[RoleType]
        """
        return self.__roles

    @property
    def url(self):
        """Homepage on which the provider describes the dataset and publishes contact information.

        :getter: Returns the homepage
        :setter: Sets the homepage
        :type: Union[str, None]
        """
        return self.__url

    @url.setter
    def url(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__url = value

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        provider = dict()
        provider["name"] = self.name
        if self.description is not None:
            provider["description"] = self.description
        if len(self.roles) > 0:
            provider["roles"] = [role.value for role in self.roles]
        if self.url is not None:
            provider["url"] = self.url
        return provider

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class SpatialExtentObject:
    """The object describes the spatial extents of the Collection."""

    def __init__(self, bbox: List[List[float]]):
        """Create a spatial extent

        The first bounding box always describes the overall spatial extent of
        the data. All subsequent bounding boxes can be used to provide a more
        precise description of the extent and identify clusters of data.
        Clients only interested in the overall spatial extent will only need to
        access the first item in each array. It is recommended to only use
        multiple bounding boxes if a union of them would then include a large
        uncovered area (e.g. the union of Germany and Chile).

        The length of the inner array must be 2*n where n is the number of
        dimensions. The array contains all axes of the southwesterly most
        extent followed by all axes of the northeasterly most extent specified
        in Longitude/Latitude or Longitude/Latitude/Elevation based on WGS 84.
        When using 3D geometries, the elevation of the southwesterly most
        extent is the minimum depth/height in meters and the elevation of the
        northeasterly most extent is the maximum.

        The coordinate reference system of the values is WGS 84
        longitude/latitude. Example that covers the whole Earth:
        [[-180.0, -90.0, 180.0, 90.0]]. Example that covers the whole earth
        with a depth of 100 meters to a height of 150 meters:
        [[-180.0, -90.0, -100.0, 180.0, 90.0, 150.0]]

        Args:
            bbox (List[List[float]]): Potential spatial extents covered by the Collection.
        """
        self.__bbox: List[List[float]] = bbox

    @property
    def bbox(self):
        """Potential spatial extents covered by the Collection.

        :getter: Returns the spatial extents covered by the Collection.
        :setter: Sets the bbox
        :type: List[List[float]]
        """
        return self.__bbox

    @bbox.setter
    def bbox(self, value: List[List[float]]):
        self.__bbox = value

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        return {"bbox": self.bbox}

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class TemporalExtentObject:
    """The object describes the temporal extents of the Collection."""

    def __init__(self, interval: List[List[Union[datetime, None]]]):
        """Create a temporal extent

        interval: Each outer array element can be a separate temporal extent.
        The first time interval always describes the overall temporal extent of
        the data. All subsequent time intervals can be used to provide a more
        precise description of the extent and identify clusters of data.
        Clients only interested in the overall extent will only need to access
        the first item in each array. It is recommended to only use multiple
        temporal extents if a union of them would then include a large
        uncovered time span (e.g. only having data for the years 2000,
        2010 and 2020).

        Each inner array consists of exactly two elements, either a timestamp
        or null.

        Timestamps consist of a date and time in UTC and MUST be formatted
        according to RFC 3339, section 5.6. The temporal reference system is
        the Gregorian calendar.

        Open date ranges are supported by setting the start and/or the end time
        to null. Example for data from the beginning of 2019 until now:
        [["2019-01-01T00:00:00Z", null]]. It is recommended to provide at
        least a rough guideline on the temporal extent and thus it's not
        recommended to set both start and end time to null. Nevertheless, this
        is possible if there's a strong use case for an open date range to
        both sides.

        Args:
            interval (List[List[Union[datetime, None]]]): Potential temporal extents covered by the Collection.
        """
        self.__interval: List[List[Union[datetime, None]]] = interval

    @property
    def interval(self):
        """Potential temporal extents covered by the Collection.

        :getter: Returns the temporal extents covered by the Collection.
        :setter: Sets the interval
        :type: List[List[Union[datetime, None]]]
        """
        return self.__interval

    @interval.setter
    def interval(self, value: List[List[Union[datetime, None]]]):
        self.__interval = value

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        interval = list()
        for simple_interval in self.interval:
            min_val = (
                None if simple_interval[0] is None else str(simple_interval[0])
            )
            max_val = (
                None if simple_interval[1] is None else str(simple_interval[1])
            )
            interval.append([min_val, max_val])
        return {"interval": interval}

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class ExtentObject:
    """The object describes the spatio-temporal extents of the Collection."""

    def __init__(
        self, spatial: SpatialExtentObject, temporal: TemporalExtentObject
    ) -> None:
        """Create an extent object

        Args:
            spatial (SpatialExtentObject): Potential spatial extents covered by the Collection.
            temporal (TemporalExtentObject): Potential temporal extents covered by the Collection.
        """
        self.__spatial: SpatialExtentObject = spatial
        self.__temporal: TemporalExtentObject = temporal

    @property
    def spatial(self):
        """Potential spatial extents covered by the Collection.

        :getter: Returns the spatial extent object
        :setter: Sets the spatial extent object
        :type: SpatialExtentObject
        """
        return self.__spatial

    @spatial.setter
    def spatial(self, value: SpatialExtentObject):
        if not isinstance(value, SpatialExtentObject):
            raise TypeError(
                f"value has type {type(value)} but must have SpatialExtentObject type"
            )
        self.__spatial = value

    @property
    def temporal(self):
        """Potential temporal extents covered by the Collection.

        :getter: Returns the temporal extent object
        :setter: Sets the temporal extent object
        :type: TemporalExtentObject
        """
        return self.__temporal

    @temporal.setter
    def temporal(self, value: TemporalExtentObject):
        if not isinstance(value, TemporalExtentObject):
            raise TypeError(
                f"value has type {type(value)} but must have TemporalExtentObject type"
            )
        self.__temporal = value

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        extent = dict()
        extent["spatial"] = self.spatial.to_dict()
        extent["temporal"] = self.temporal.to_dict()
        return extent

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class RangeObject:
    """Range object."""

    def __init__(self, minimum: Union[str, float], maximum: Union[str, float]):
        """Create a range object

        For summaries that would normally consist of a lot of continuous
        values, statistics can be added instead. By default, only ranges with
        a minimum and a maximum value can be specified. Ranges can be specified
        for ordinal values only, which means they need to have a rank order.
        Therefore, ranges can only be specified for numbers and some special
        types of strings. Examples: grades (A to F), dates or times.
        Implementors are free to add other derived statistical values to the
        object, for example mean or stddev.

        Args:
            minimum (Union[str, float]): Minimum value.
            maximum (Union[str, float]): Maximum value.
        """
        self.__minimum = minimum
        self.__maximum = maximum

    @property
    def minimum(self):
        """Minimum value.

        :getter: Returns the minimum value
        :setter: Sets the minimum value
        :type: Union[str, float]
        """
        return self.__minimum

    @minimum.setter
    def minimum(self, value: Union[str, float]):
        if not isinstance(value, str) and not isinstance(value, float):
            raise TypeError(
                f"value has type {type(value)} but must have str or float type"
            )
        self.__minimum = value

    @property
    def maximum(self):
        """Maximum value.

        :getter: Returns the maximum value
        :type: Union[str, float]
        """
        return self.__maximum

    @maximum.setter
    def maximum(self, value: Union[str, float]):
        if not isinstance(value, str) and not isinstance(value, float):
            raise TypeError(
                f"value has type {type(value)} but must have str or float type"
            )
        self.__maximum = value

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            [Union[str, float], Union[str, float]]: convert to dictionnary
        """
        return [self.minimum, self.maximum]

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class AssetObject:

    """An Asset is an object that contains a URI to data associated with the
    Item that can be downloaded or streamed. It is allowed to add additional
    fields."""

    # TODO : Add a class AssetObjectItem to add additional information in assets
    #       see https://github.com/stac-extensions/eo/blob/main/examples/item.json

    def __init__(self, href: str) -> None:
        """Create an asset

        Args:
            href (str): URI to the asset object. Relative and absolute URI are both allowed.
        """
        self.__href: str = href
        self.__title: Optional[str] = None
        self.__description: Optional[str] = None
        self.__type: Optional[Union[MediaTypeAsset, CommonMediaType]] = None
        self.__roles: List[RoleAsset] = list()

    @property
    def href(self):
        """URI to the asset object. Relative and absolute URI are both allowed.

        :getter: Returns the URI to the asset
        :setter: Sets href
        :type: str
        """
        return self.__href

    @href.setter
    def href(self, value: str):
        if not isinstance(value, str):
            raise TypeError(
                f"value has type {type(value)} but must have str type"
            )
        self.__href = value

    @property
    def title(self):
        """The displayed title for clients and users.

        :getter: Returns the displayed title for clients and users.
        :setter: Set the displayed title for clients and users.
        :type: Union[str, None]
        """
        return self.__title

    @title.setter
    def title(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__title = value

    @property
    def description(self):
        """A description of the Asset providing additional details, such as
        how it was processed or created. CommonMark 0.29 syntax MAY be used for
        rich text representation.

        :getter: Returns the description.
        :setter: Set the description.
        :type: Union[str, None]
        """
        return self.__description

    @description.setter
    def description(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__description = value

    @property
    def type(self):
        """Media type of the asset.

        :getter: Returns the media type.
        :setter: Set the media type.
        :type: Union[MediaTypeAsset, CommonMediaType, None]
        """
        return self.__type

    @type.setter
    def type(self, value: Union[MediaTypeAsset, CommonMediaType, None]):
        if (
            not isinstance(value, MediaTypeAsset)
            and not isinstance(value, CommonMediaType)
            and value is not None
        ):
            raise TypeError(
                f"value has type {type(value)} but must have MediaTypeAsset type or CommonMediaType type or None"
            )
        self.__type = value

    @property
    def roles(self):
        """The semantic roles of the asset, similar to the use of rel in links.

        :getter: Returns the semantic roles of the asset.
        :type: List[RoleAsset]
        """
        return self.__roles

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        assets = dict()
        assets["href"] = self.href
        if self.title is not None:
            assets["title"] = self.title
        if self.description is not None:
            assets["description"] = self.description
        if self.type is not None:
            assets["type"] = self.type.value
        if len(self.roles) > 0:
            assets["roles"] = [role.value for role in self.roles]
        return assets

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class Properties:
    """Additional metadata fields can be added to the GeoJSON Object
    Properties. The only required field is datetime but it is recommended to
    add more fields"""

    def __init__(self, datetime: Union[str, None]):
        """Create properties

        Args:
            datetime (Union[str, None]): the searchable date and time of the
            assets, which must be in UTC. It is formatted according to
            RFC 3339, section 5.6. null is allowed, but requires start_datetime
            and end_datetime from common metadata to be set.
        """
        self.__datetime: Union[str, None] = datetime
        self.__other_properties = dict()

    @property
    def datetime(self):
        """The searchable date

        :getter: Returns the searchable date
        :type: Union[str, None]
        """
        return self.__datetime

    @datetime.setter
    def datetime(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__datetime = value

    @property
    def other_properties(self):
        """Add additional properties

        :getter: Returns the additional properties
        :setter: add entries in the additional properties
        :type: Union[Dict, None]
        """
        return self.__other_properties

    @other_properties.setter
    def other_properties(self, value: Union[Dict, None]):
        if not isinstance(value, Dict) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have dict type or None"
            )
        if value is None:
            self.__other_properties.clear()
        else:
            self.__other_properties.update(value)

    def to_dict(self):
        """Convert to Dictionary

        Returns:
            Dict[str, any]: convert to dictionnary
        """
        properties = self.other_properties.copy()
        properties["datetime"] = self.datetime
        return properties

    def __str__(self):
        return f"{self.to_dict()}"

    def __repr__(self):
        return str(self.to_dict())


class StacCatalog(Observer):
    """A Catalog is a very simple construct - it just provides links to Items
    or to other Catalogs. The closest analog is a folder in a file structure,
    it is the container for Items, but it can also hold other containers
    (folders / catalogs).

    Catalogs in turn are used for two main things:
     - Split overly large collections into groups
     - Group collections into a catalog of Collections (e.g. as entry point for
     navigation to several Collections).
    """

    def __init__(
        self,
        directory: str,
        id: str,
        path: str,
        description: str,
        stac_version: str = "1.0.0",
        *args,
        **kwargs,
    ):
        """Create a STAC catalog

        Args:
            directory (str): Root directory where STAC files are written
            id (str): Identifier for the Catalog.
            path (str): Path of this catalog (as REST path)
            description (str): Detailed multi-line description to fully explain
            the Catalog. CommonMark 0.29 syntax MAY be used for rich text
            representation.
            stac_version (str, optional): The STAC version the Catalog implements. Defaults to "1.0.0".

        Raises:
            ValueError: When no parent is set, path must be set to '/'
            TypeError: parent must be either a collection or a catalog in a catalog when parent is defined
        """
        self.__type: str = "Catalog"
        self.__directory: str = Utils.fix_directory_syntax(directory)
        self.__id: str = id
        self.__path: str = Utils.fix_directory_syntax(path)
        self.__description: str = description
        self.__stac_version: str = stac_version
        self.__links: List[Link] = list()
        self.__stac_extensions: List[str] = list()
        self.__stac_extensions_properties: Dict[str, Any] = dict()
        self.__title: Optional[str] = kwargs.get("title", None)
        self.__parent: Union[
            StacCatalog, StacCollection, None
        ] = self._validate_parent(kwargs.get("parent", None))
        self._create_links()

    def _validate_parent(
        self, parent: Union["StacCollection", "StacCatalog", None]
    ) -> Union["StacCollection", "StacCatalog", None]:
        """Validate the type of parent. Must be either StacCatalog or StacCollection

        Args:
            parent (Union[StacCollection, StacCatalog, None]): the parent of the item

        Raises:
            ValueError: When no parent is set, path must be set to '/'
            TypeError: parent must be either a collection or a catalog in a catalog when parent is defined

        Returns:
            [Union[StacCollection, StacCatalog, None]]: parent
        """
        if parent is None and self.path != "":
            raise ValueError("When no parent is set, path must be set to '/'")
        if (
            parent is not None
            and not isinstance(parent, StacCatalog)
            and not isinstance(parent, StacCollection)
        ):
            raise TypeError(
                f"parent must be either a collection or a catalog in a catalog when parent is defined: {type(parent)}"
            )
        return parent

    def _create_root_link(self):
        """Create root link"""
        back_path: str
        filename: str
        if self.parent is None:
            back_path = "."
            filename = self.id + ".json"
        else:
            root = [
                link.href
                for link in self.parent.links
                if link.rel == RelationTypes.ROOT
            ][0]
            filename = root.split("/")[-1]
            frags: List[str] = self.path.split("/")[1:-1]
            back: List[str] = [".." for i in range(0, len(frags) + 1)]
            back_path = "/".join(back) if len(back) > 0 else "."
        parentLink: Link = Link(back_path + "/" + filename, RelationTypes.ROOT)
        parentLink.type = MediaType.STAC_CATALOG
        self.__links.append(parentLink)

    def _create_self_link(self, catalog_name: str):
        """Create self link

        Args:
            catalog_name (str): name of this catalog
        """
        selfLink = Link(catalog_name, RelationTypes.SELF)
        selfLink.type = (
            MediaType.STAC_CATALOG
            if self.type == "Catalog"
            else MediaType.STAC_COLLECTION
        )
        selfLink.title = self.title if self.title is not None else str(self.id)
        self.__links.append(selfLink)

    def _create_child_link(
        self, parent: Union["StacCatalog", "StacCollection"]
    ):
        """Create the child link of the parent

        Args:
            parent (Union["StacCatalog", "StacCollection"]): parent

        Raises:
            TypeError: Unexpected type
        """
        parent_path: str = parent.path
        child_path: str = self.path.replace(parent_path, "")
        childLink: Link = Link(
            f".{child_path}/{self.id}.json", RelationTypes.CHILD
        )
        if self.type == "Catalog":
            childLink.type = MediaType.STAC_CATALOG
        elif self.type == "Collection":
            childLink.type = MediaType.STAC_COLLECTION
        else:
            raise TypeError(f"Unexpected type: {self.type}")

        if self.title is not None:
            childLink.title = self.title

        parent.links.append(childLink)

    def _create_parent_link(
        self, parent: Union["StacCatalog", "StacCollection"]
    ):
        """Create parent link

        Args:
            parent (Union["StacCatalog", "StacCollection"]): parent

        Raises:
            TypeError: Unexpected type
        """
        parentLink: Link = Link(f"../{parent.id}.json", RelationTypes.PARENT)
        if parent.type == "Catalog":
            parentLink.type = MediaType.STAC_CATALOG
        elif parent.type == "Collection":
            parentLink.type = MediaType.STAC_COLLECTION
        else:
            raise TypeError(
                f"Unexpected type: {parent.type} for {type(parent)}"
            )

        if parent.title is not None:
            parentLink.title = parent.title

        self.links.append(parentLink)

    def _update_self_link_title(self, title: Union[str, None]):
        """Update self link

        Args:
            catalog_name (str): name of this catalog
            title (Union[str, None]): title to update in self_link
        """
        for link in self.links:
            if link.rel == RelationTypes.SELF:
                link.title = title
                break

    def _update_child_link_title(
        self,
        parent: Union["StacCatalog", "StacCollection"],
        title: Union[str, None],
    ):
        """Update the child link of the parent

        Args:
            parent (Union["StacCatalog", "StacCollection"]): parent
            title (Union[str, None]) : title

        Raises:
            TypeError: Unexpected type
        """
        parent_path: str = parent.path
        child_path: str = self.path.replace(parent_path, "")
        href: str = f".{child_path}/{self.id}.json"
        for link in parent.links:
            if link.href == href:
                link.title = title
                break

    def _create_links(self):
        """Create the links"""
        if self.parent is None:
            self._create_root_link()
            self._create_self_link(f"{self.id}.json")
        else:
            self._create_root_link()
            self._create_self_link(f"{self.id}.json")
            self._create_child_link(self.parent)
            self._create_parent_link(self.parent)

    def add_stac_extension(
        self, extension_name: str, properties: Dict[str, Any]
    ) -> None:
        """Additional attributes relating to a Catalog or Collection should be added to the root of the object.

        Args:
            extension_name (str): Extension name
            properties (Dict[str, Any]): Dictionary to insert in root object
        """
        self.stac_extensions.append(extension_name)
        self.stac_extensions_properties.update(properties)
        # TODO : check the extension according JSON schema

    @property
    def directory(self):
        """The root directory

        :getter: Returns the root directory where the files are saved
        :type: str
        """
        return self.__directory

    @property
    def type(self):
        """Set to Catalog if this Catalog only implements the Catalog spec.

        :getter: Returns the type
        :type: str
        """
        return self.__type

    @type.setter
    def type(self, value: str):
        if isinstance(self, StacCatalog) and value == "Catalog":
            self.__type = value
        elif isinstance(self, StacCollection) and value == "Collection":
            self.__type = value
        else:
            raise ValueError(f"Value {value} is forbidden")

    @property
    def id(self):
        """Identifier for the Catalog.

        :getter: Returns the identifier for the Catalog
        :type: str
        """
        return self.__id

    @property
    def stac_extensions_properties(self):
        return self.__stac_extensions_properties

    @property
    def path(self):
        """Path of the cataloge (as REST style)

        :getter: Returns the path
        :type: str
        """
        return self.__path

    @property
    def description(self):
        """Detailed multi-line description to fully explain the Catalog.
        CommonMark 0.29 syntax MAY be used for rich text representation.

        :getter: Returns the detailed multi-line description to fully explain
        the Catalog
        :setter: Sets the description
        :type: str
        """
        return self.__description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError(
                f"value has type {type(value)} but must have str type"
            )
        self.__description = value

    @property
    def stac_version(self):
        """The STAC version the Catalog implements.

        :getter: Returns the STAC version
        :type: str
        """
        return self.__stac_version

    @property
    def title(self):
        """A short descriptive one-line title for the Catalog.

        Update the self link and the child link of the parent with the title

        :getter: Returns the short descriptive one-line title for the Catalog
        :setter: Set the title
        :type: Union[str, None]
        """
        return self.__title

    @title.setter
    def title(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__title = value
        if self.parent is None:
            self._update_self_link_title(value)
        else:
            self._update_self_link_title(value)
            self._update_child_link_title(self.parent, value)

    @property
    def links(self):
        """A list of references to other documents.

        :getter: Returns the list of references to other documents
        :type: List[Link]
        """
        return self.__links

    @property
    def stac_extensions(self):
        """A list of extension identifiers the Catalog implements.

        :getter: Returns the list of extension identifiers the Catalog implements
        :type: List[str]
        """
        return self.__stac_extensions

    @property
    def parent(self):
        """The parent of this item.

        :getter: Returns the parent of this item
        :type: Union[StacCollection, StacCatalog]
        """
        return self.__parent

    def to_json(self):
        """Convert to JSON as Dict

        Returns:
            [Dict]: The JSON output
        """
        catalog: Dict = dict()
        catalog["type"] = self.type
        catalog["stac_version"] = self.stac_version
        catalog["id"] = self.id
        catalog["description"] = self.description
        catalog["links"] = [link.to_dict() for link in self.links]

        if len(self.stac_extensions) > 0:
            catalog["stac_extensions"] = self.stac_extensions

        if len(self.stac_extensions_properties) > 0:
            catalog.update(self.stac_extensions_properties)

        if self.title is not None:
            catalog["title"] = self.title

        return catalog

    def notify(self, observable, *args, **kwargs):
        """Get the notification

        Args:
            observable ([type]): Observable
        """
        if args[0] == "save":
            filename: str = f"{self.directory}{self.path}/{self.id}.json"
            os.makedirs(self.directory + self.path, exist_ok=True)
            logger.debug(f"Saving in {filename}")
            with open(filename, "w") as outfile:
                json.dump(self.to_json(), outfile, indent=4)
        elif args[0] == "tree":
            if self.parent is None:
                print(f"Root directory: {self.directory}")
            print(f"\t {self.type} {self.id} : {self.path}/{self.id}.json")

    def __str__(self):
        return f"{self.to_json()}"

    def __repr__(self):
        return f"StacCatalog[id='{self.id}']"


class StacCollection(StacCatalog):
    """The Collection entity shares most fields with the Catalog entity but has
    a number of additional fields: license, extent (spatial and temporal),
    providers, keywords and summaries. Every Item in a Collection links back to
    their Collection, so clients can easily find fields like the license. Thus
    every Item implicitly shares the fields described in their parent
    Collection. Collection entities can be used just like Catalog entities to
    provide structure, as they provide all the same options for linking and
    organizing.
    """

    def __init__(
        self,
        directory: str,
        id: str,
        path: str,
        description: str,
        license: LicenseType,
        extent: ExtentObject,
        stac_version: str = "1.0.0",
        *args,
        **kwargs,
    ):
        """Create the STAC collection

        Args:
            directory (str): Root directory where STAC files are stored
            id (str): Identifier for the Collection that is unique across the provider.
            path (str): Location in the STAC tree using (REST like)
            description (str): Detailed multi-line description to fully explain the Collection. CommonMark 0.29 syntax MAY be used for rich text representation.
            license (LicenseType): Collection's license(s)
            extent (ExtentObject): Spatial and temporal extents.
            stac_version (str, optional): The STAC version the Collection implements.. Defaults to "1.0.0".
        """
        super().__init__(
            directory, id, path, description, stac_version, *args, **kwargs
        )
        self.type = "Collection"
        self.__keywords: List[str] = list()
        self.__license: LicenseType = license
        self.__providers: List[Provider] = list()
        self.__extent: ExtentObject = extent
        self.__summaries: Optional[Dict[str, Union[RangeObject, Any]]] = None
        self.__assets: Optional[Dict[str, AssetObject]] = None

    def _validate_parent(
        self, parent: Optional[Union["StacCollection", StacCatalog]]
    ) -> Union["StacCollection", StacCatalog]:
        """Validate the parent's link

        Raises:
            ValueError: parent cannot be None in a collection
            TypeError: parent must be either a collection or a catalog in a collection

        Returns:
            [Union[StacCollection, StacCatalog]]: parent
        """
        if parent is None:
            raise ValueError("parent cannot be None in a collection")
        if not isinstance(parent, StacCatalog) and not isinstance(
            parent, StacCollection
        ):
            raise TypeError(
                f"parent must be either a collection or a catalog in a collection: {type(parent)}"
            )
        return parent

    @property
    def keywords(self):
        """List of keywords describing the Collection.

        :getter: Returns the list of keywords
        :type: List[str]
        """
        return self.__keywords

    @property
    def license(self):
        """Collection's license(s), either a SPDX License identifier.

        :getter: Returns the collection license
        :setter: Sets the license
        :type: LicenseType
        """
        return self.__license

    @license.setter
    def license(self, value: LicenseType):
        if not isinstance(value, LicenseType):
            raise TypeError(
                f"value has type {type(value)} but must have LicenseType type"
            )
        self.__license = value

    @property
    def providers(self):
        """A list of providers, which may include all organizations capturing
        or processing the data or the hosting provider. Providers should be
        listed in chronological order with the most recent provider being the
        last element of the list.

        :getter: Returns the list of providers
        :type: List[Provider]
        """
        return self.__providers

    @property
    def extent(self):
        """Spatial and temporal extents.

        :getter: Returns the list of providers
        :type: ExtentObject
        """
        return self.__extent

    @extent.setter
    def extent(self, value: ExtentObject):
        if not isinstance(value, ExtentObject):
            raise TypeError(
                f"value has type {type(value)} but must have ExtentObject type"
            )
        self.__extent = value

    @property
    def summaries(self):
        """A map of property summaries, either a set of values, a range of
        values or a JSON Schema

        :getter: Returns the map of property summaries
        :setter: Set the summaries
        :type: Union[Dict[str, Union[RangeObject, Any]], None]
        """
        return self.__summaries

    @summaries.setter
    def summaries(
        self, value: Union[Dict[str, Union[RangeObject, Any]], None]
    ):
        if not isinstance(value, Dict) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have dict type or None"
            )
        self.__summaries = value

    @property
    def assets(self):
        """Dictionary of asset objects that can be downloaded, each with a
        unique key.

        :getter: Returns the dictionary of asset objects
        :setter: Sets the dictionary of asset objects
        :type: Union[Dict[str, AssetObject], None]
        """
        return self.__assets

    @assets.setter
    def assets(self, value: Union[Dict[str, AssetObject], None]):
        if not isinstance(value, Dict) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have dict type or None"
            )
        self.__assets = value

    def to_json(self):
        """Convert to JSON as Dict

        Returns:
            [Dict]: The JSON output
        """
        collection = super().to_json()

        collection["license"] = self.license.value
        collection["extent"] = self.extent.to_dict()

        if len(self.keywords) > 0:
            collection["keywords"] = self.keywords
        if len(self.providers) > 0:
            collection["providers"] = [
                provider.to_dict() for provider in self.providers
            ]
        if self.summaries is not None:
            collection["summaries"] = self.summaries
        if self.assets is not None:
            collection["assets"] = dict(
                (key, self.assets[key].to_dict()) for key in self.assets
            )
        return collection

    def __str__(self):
        return f"{self.to_json()}"

    def __repr__(self):
        return f"StacCollection[id='{self.id}']"


class StacItem(Observer):
    """The STAC Item object is the most important object in a STAC system. An
    Item is the entity that contains metadata for a scene and links to the
    assets.

    Item objects are the leaf nodes for a graph of Catalog and Collection
    objects.

    The OpenAPI specification in item.json defines an Item object. The
    `Link basics <https://github.com/radiantearth/stac-spec/blob/master/item-spec/json-schema/basics.json>`_ ,
    `Link datetime <https://github.com/radiantearth/stac-spec/blob/master/item-spec/json-schema/datetime.json>`_ ,
    `Link instrument <https://github.com/radiantearth/stac-spec/blob/master/item-spec/json-schema/instrument.json>`_ ,
    `Link licensing <https://github.com/radiantearth/stac-spec/blob/master/item-spec/json-schema/licensing.json>`_ ,
    `Link provider <https://github.com/radiantearth/stac-spec/blob/master/item-spec/json-schema/provider.json>`_
    schemas validate additional fields defined in Common Metadata.
    """

    def __init__(
        self,
        directory: str,
        id: str,
        path: str,
        geometry: Union[
            Point,
            Polygon,
            MultiPoint,
            MultiPolygon,
            LineString,
            MultiLineString,
            None,
        ],
        properties: Properties,
        assets: Dict[str, AssetObject],
        stac_version: str = "1.0.0",
        *args,
        **kwargs,
    ):
        """Create a STAC item.

        Args:
            directory (str): Root directory
            id (str): Provider identifier. The ID should be unique within the Collection that contains the Item.
            path (str): location in STAC (use path /xxx/yyy/)
            geometry (Union[Point, Polygon, MultiPoint, MultiPolygon, LineString, MultiLineString, None]): Defines the full footprint of the asset represented by this item, formatted according to RFC 7946, section 3.1. The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on WGS 84.
            properties (Properties): A dictionary of additional metadata for the Item
            assets (Dict[str, AssetObject]): Dictionary of asset objects that can be downloaded, each with a unique key.
            stac_version (str, optional): The STAC version the Item implements. Defaults to "1.0.0".
        """
        self.__type: str = "Feature"
        self.__directory: str = Utils.fix_directory_syntax(directory)
        self.__id: str = id
        self.__path: str = Utils.fix_directory_syntax(path)
        self.__geometry: Union[
            Point,
            Polygon,
            MultiPoint,
            MultiPolygon,
            LineString,
            MultiLineString,
            None,
        ] = geometry
        self.__bbox: Optional[List[Tuple[float]]] = (
            [geometry.bounds] if geometry is not None else None
        )
        self.__stac_version: str = stac_version
        self.__stac_extensions: List[str] = list()
        self.__properties: Properties = properties
        self.__links: List[Link] = list()
        self.__assets: Dict[str, AssetObject] = assets
        self.__collection: Optional[str] = None
        self.__parent: Union[
            StacCollection, StacCatalog
        ] = self._validate_parent(kwargs.get("parent", None))
        self._create_links()

    def _validate_parent(
        self, parent: Optional[Union[StacCollection, StacCatalog]]
    ) -> Union[StacCollection, StacCatalog]:
        """Validate the parent of the item.

        Args:
            parent (Optional[Union[StacCollection, StacCatalog]]): the parent of the item

        Raises:
            ValueError: parent cannot be None for an item
            TypeError: parent must be a collection or a catalog for an item

        Returns:
            Union[StacCollection, StacCatalog]: the parent
        """
        if parent is None:
            raise ValueError("parent cannot be None for an item")
        if not isinstance(parent, StacCollection) and not isinstance(
            parent, StacCatalog
        ):
            raise TypeError(
                f"parent must be a collection or a catalog for an item: {type(self.__parent)}"
            )
        return parent

    def _create_root_link(self):
        """Create the root link"""
        root: str = [
            link.href
            for link in self.parent.links
            if link.rel == RelationTypes.ROOT
        ][0]
        filename: str = root.split("/")[-1]
        frags: List[str] = self.path.split("/")[1:-1]
        back: List[str] = [".." for i in range(0, len(frags) + 1)]
        back_path: str = "/".join(back) if len(back) > 0 else "."
        parentLink: Link = Link(back_path + "/" + filename, RelationTypes.ROOT)
        parentLink.type = MediaType.STAC_CATALOG
        self.__links.append(parentLink)

    def _create_self_link(self, catalog_name: str):
        """Create the self link.

        Args:
            catalog_name (str): name of this catalog or collection name
        """
        selfLink = Link(catalog_name, RelationTypes.SELF)
        selfLink.type = MediaType.STAC_ITEM
        selfLink.title = str(self.id)
        self.__links.append(selfLink)

    def _create_child_link(self, parent: Union[StacCatalog, StacCollection]):
        """Create the child links in the parent.

        Args:
            parent (Union[StacCatalog, StacCollection]): the parent to update
        """
        parent_path: str = parent.path
        child_path: str = self.path.replace(parent_path, "")
        childLink: Link = Link(
            f".{child_path}/{self.id}.json", RelationTypes.ITEM
        )
        childLink.type = MediaType.STAC_ITEM
        childLink.title = str(self.id)
        parent.links.append(childLink)

    def _create_parent_link(self, parent: Union[StacCatalog, StacCollection]):
        """Create the parent link.

        Args:
            parent (Union[StacCatalog, StacCollection]): update the parent link of the item

        Raises:
            TypeError: Unexpected type
        """
        parentLink: Link = Link(f"../{parent.id}.json", RelationTypes.PARENT)
        if parent.type == "Catalog":
            parentLink.type = MediaType.STAC_CATALOG
        elif parent.type == "Collection":
            parentLink.type = MediaType.STAC_COLLECTION
        else:
            raise TypeError(
                f"Unexpected type: {parent.type} for {type(parent)}"
            )

        if parent.title is not None:
            parentLink.title = parent.title

        self.links.append(parentLink)

    def _create_links(self):
        """Update the links."""
        self._create_root_link()
        self._create_self_link(f"{self.id}.json")
        self._create_child_link(self.parent)
        self._create_parent_link(self.parent)

    def notify(self, observable, *args, **kwargs):
        """Get the notification

        Args:
            observable ([type]): Observable
        """
        if args[0] == "save":
            filename: str = f"{self.directory}{self.path}/{self.id}.json"
            os.makedirs(self.directory + self.path, exist_ok=True)
            logger.debug(f"Saving in {filename}")
            with open(filename, "w") as outfile:
                json.dump(self.to_json(), outfile, indent=4)
        elif args[0] == "tree":
            print(f"\t {self.type} {self.id} : {self.path}/{self.id}.json")

    @property
    def directory(self):
        """The root directory

        :getter: Returns the root directory where the files are saved
        :type: str
        """
        return self.__directory

    @property
    def type(self):
        """Type of the GeoJSON Object.

        :getter: Returns the type of the GeoJSON Object
        :type: str
        """
        return self.__type

    @property
    def id(self):
        """Provider identifier. The ID should be unique within the Collection that contains the Item.

        :getter: Returns the provider identifier
        :type: str
        """
        return self.__id

    @property
    def path(self):
        """The path.

        :getter: Returns the path
        :type: str
        """
        return self.__path

    @property
    def geometry(self):
        """Defines the full footprint of the asset represented by this item,
        formatted according to RFC 7946, section 3.1. The footprint should be
        the default GeoJSON geometry, though additional geometries can be
        included. Coordinates are specified in Longitude/Latitude or
        Longitude/Latitude/Elevation based on WGS 84.

        :getter: Returns the geometry
        :type: Union[
            Point,
            Polygon,
            MultiPoint,
            MultiPolygon,
            LineString,
            MultiLineString,
            None,
        ]
        """
        return self.__geometry

    @property
    def bbox(self):
        """if geometry is not null. Bounding Box of the asset represented by
        this Item, formatted according to RFC 7946, section 5.

        :getter: Returns the bbox
        :type: Union[List[Tuple[float]], None]
        """
        return self.__bbox

    @property
    def stac_version(self):
        """The STAC version the Item implements.

        :getter: Returns the STAC version
        :type: str
        """
        return self.__stac_version

    @property
    def stac_extensions(self):
        """A list of extensions the Item implements.

        :getter: Returns the list of extensions
        :type: List[str]
        """
        return self.__stac_extensions

    @property
    def properties(self):
        """A dictionary of additional metadata for the Item.

        :getter: Returns the dictionary of additional metadata
        :type: Properties
        """
        return self.__properties

    @property
    def links(self):
        """List of link objects to resources and related URLs.

        :getter: Returns the list of links
        :type: List[Link]
        """
        return self.__links

    @property
    def assets(self):
        """Dictionary of asset objects that can be downloaded, each with a unique key.

        :getter: Returns the dictionary of asset objects
        :type: Dict[str, AssetObject]
        """
        return self.__assets

    @property
    def parent(self):
        """The parent of this item.

        :getter: Returns the parent of this item
        :type: Union[StacCollection, StacCatalog]
        """
        return self.__parent

    @property
    def collection(self):
        """The id of the STAC Collection this Item references to. This field is
        required if such a relation type is present and is not allowed
        otherwise. This field provides an easy way for a user to search for any
        Items that belong in a specified Collection. Must be a non-empty string.

        :getter: Returns the collection
        :setter: Sets the collection ID
        :type: Union[str, None]
        """
        return self.__collection

    @collection.setter
    def collection(self, value: Union[str, None]):
        if not isinstance(value, str) and value is not None:
            raise TypeError(
                f"value has type {type(value)} but must have str type or None"
            )
        self.__collection = value

    def to_json(self) -> Dict:
        """Convert to JSON as Dict

        Returns:
            [Dict]: The JSON output
        """
        item: Dict = dict()
        item["type"] = self.type
        item["stac_version"] = self.stac_version
        item["id"] = self.id
        if len(self.stac_extensions) > 0:
            item["stac_extensions"] = self.stac_extensions
        item["geometry"] = (
            shapely.geometry.mapping(self.geometry)
            if self.geometry is not None
            else None
        )
        item["bbox"] = self.bbox
        item["properties"] = self.properties.to_dict()
        item["links"] = [link.to_dict() for link in self.links]
        item["assets"] = dict(
            (key, self.assets[key].to_dict()) for key in self.assets
        )
        if self.collection is not None:
            item["collection"] = self.collection

        return item

    def __str__(self):
        return f"{self.to_json()}"

    def __repr__(self):
        return f"StacItem[id='{self.id}']"


class PystacLib(Observable):
    """The library"""

    def __init__(self, path_to_conf: str, directory: str, *args, **kwargs):
        super().__init__()
        # pylint: disable=unused-argument
        if "level" in kwargs:
            PystacLib._parse_level(kwargs["level"])

        self.__directory = Utils.fix_directory_syntax(directory)
        self.__config = configparser.ConfigParser()
        self.__config.optionxform = str  # type: ignore
        self.__config.read(path_to_conf)

    @staticmethod
    def _parse_level(level: str):
        """Parse level name and set the rigt level for the logger.
        If the level is not known, the INFO level is set

        Args:
            level (str): level name
        """
        logger_main = logging.getLogger(__name_soft__)
        if level == "INFO":
            logger_main.setLevel(logging.INFO)
        elif level == "DEBUG":
            logger_main.setLevel(logging.DEBUG)
        elif level == "WARNING":
            logger_main.setLevel(logging.WARNING)
        elif level == "ERROR":
            logger_main.setLevel(logging.ERROR)
        elif level == "CRITICAL":
            logger_main.setLevel(logging.CRITICAL)
        elif level == "TRACE":
            logger_main.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member
        else:
            logger_main.warning(
                "Unknown level name : %s - setting level to INFO", level
            )
            logger_main.setLevel(logging.INFO)

    @property
    def config(self) -> configparser.ConfigParser:
        """The configuration file.

        :getter: Returns the configuration file
        :type: configparser.ConfigParser
        """
        return self.__config

    @property
    def directory(self) -> str:
        """The root directory

        :getter: Returns the root directory where the files are saved
        :type: str
        """
        return self.__directory

    def create_catalog(
        self,
        id: str,
        path: str,
        description: str,
        stac_version: str = "1.0.0",
        *args,
        **kwargs,
    ) -> StacCatalog:
        stac_catalog = StacCatalog(
            self.directory,
            id,
            path,
            description,
            stac_version,
            *args,
            **kwargs,
        )
        self.subscribe(stac_catalog)
        return stac_catalog

    def create_collection(
        self,
        id: str,
        path: str,
        description: str,
        license: LicenseType,
        extent: ExtentObject,
        stac_version: str = "1.0.0",
        *args,
        **kwargs,
    ) -> StacCollection:
        stac_collection = StacCollection(
            self.directory,
            id,
            path,
            description,
            license,
            extent,
            stac_version,
            *args,
            **kwargs,
        )
        self.subscribe(stac_collection)
        return stac_collection

    def create_item(
        self,
        path: str,
        id: str,
        geometry: Union[
            Point,
            Polygon,
            MultiPoint,
            MultiPolygon,
            LineString,
            MultiLineString,
            None,
        ],
        properties: Properties,
        assets: Dict[str, AssetObject],
        stac_version: str = "1.0.0",
        *args,
        **kwargs,
    ) -> StacItem:
        stac_item = StacItem(
            self.directory,
            id,
            path,
            geometry,
            properties,
            assets,
            stac_version,
            *args,
            **kwargs,
        )
        self.subscribe(stac_item)
        return stac_item

    def save(self):
        self.notify_observers("save")

    def tree(self):
        self.notify_observers("tree")
