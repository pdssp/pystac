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
from enum import Enum

from .exception import ValueNotFindInEnumError


class DocEnum(Enum):
    """Enum where we can add documentation."""

    def __new__(cls, value, doc=None):
        self = object.__new__(
            cls
        )  # calling super().__new__(value) here would fail
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self


def extend_docenum(inherited_enum):
    """Extends an doc enum.

    Example:
    @extend_docenum(MediaType)
    class Animals(DocEnum):
        TOTO = ("my value", "my doc")
    """

    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = (item.value, item.__doc__)
        for item in added_enum:
            joined[item.name] = (item.value, item.__doc__)
        return DocEnum(added_enum.__name__, joined)

    return wrapper


class CommonMediaType(DocEnum):
    APPLICATION_X_EXECUTABLE = "application/x-executable"
    APPLICATION_GRAPHQL = "application/graphql"
    APPLICATION_JAVASCRIPT = "application/javascript"
    APPLICATION_JSON = "application/json"
    APPLICATION_LD_JSON = "application/ld+json"
    APPLICATION_FEED_JSON = "application/feed+json"
    APPLICATION_MSWORD = "application/msword"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_SQM = "application/sql"
    APPLICATION_VND_API_JSON = "application/vnd.api+json"
    APPLICATION_MS_EXCEL = "application/vnd.ms-excel"
    APPLICATION_VND_MS_POWERPOINT = "application/vnd.ms-powerpoint"
    APPLICATION_ODT = "application/vnd.oasis.opendocument.text"
    APPLICATION_POWER_POINT = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    APPLICATION_EXCEL = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    APPLICATION_WORD = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    APPLICATION_FORM = "application/x-www-form-urlencoded"
    APPLICATION_XML = "application/xml"
    APPLICATION_ZIP = "application/zip"
    APPLICATION_ZSTD = "application/zstd"
    APPLICATION_MAC_BINARY = "application/macbinary"
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    IMAGE_APNG = "image/apng"
    IMAGE_AVIF = "image/avif"
    IMAGE_FLIF = "image/flif"
    IMAGE_GIF = "image/gif"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_JXL = "image/jxl"
    IMAGE_PNG = "image/png"
    IMAGE_SVG_XML = "image/svg+xml"
    IMAGE_WEBP = "image/webp"
    IMAGE_X_MNG = "image/x-mng"
    MULIPART = "multipart/form-data"
    TEXT_CSS = "text/css"
    TEXT_CSV = "text/csv"
    TEXT_HTML = "text/html"
    TEXT_PHP = "text/php"
    TEXT_PLAIN = "text/plain"
    TEXT_XML = "text/xml"

    @staticmethod
    def source():
        return {
            "last_updated": "2021-09-07",
            "source": "https://en.wikipedia.org/wiki/Media_type",
        }

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in CommonMediaType.__members__:
            val = str(CommonMediaType[pf_name].value)
            if val == name:
                result = CommonMediaType[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "CommonMediaType", f"Unknown enum value for {name}"
            )
        return result


class MediaType(DocEnum):
    STAC_ITEM = ("application/geo+json", "A STAC item")
    STAC_CATALOG = ("application/json", "A STAC catalog")
    STAC_COLLECTION = ("application/json", "A STAC collection")

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in MediaType.__members__:
            val = str(MediaType[pf_name].value)
            if val == name:
                result = MediaType[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "MediaType", f"Unknown enum value for {name}"
            )
        return result


class MediaTypeAsset(DocEnum):
    """The following table lists a number of commonly used media types in STAC.
    The first two (GeoTIFF and COG) are not fully standardized yet, but reflect
    the community consensus direction. The following table lists some of the
    most common ones you may encounter or use.

    Raises:
        ValueError: Unknown enum value for name

    Returns:
        [str]: Mime-type
    """

    GEOTIFF = (
        "image/tiff; application=geotiff",
        "GeoTIFF with standardized georeferencing metadata",
    )
    CLOUD_OPTIMIZED_GEOTIFF = (
        "image/tiff; application=geotiff; profile=cloud-optimized",
        "Cloud Optimized GeoTIFF (unofficial). Once there is an official media type it will be added and the custom media type here will be deprecated.",
    )
    JPEG_2000 = ("image/jp2", "JPEG 2000")
    Visual_PNG = ("image/png", "Visual PNGs (e.g. thumbnails)")
    Visual_JPEG = ("image/jpeg", "Visual JPEGs (e.g. thumbnails, oblique)")
    XML = ("text/xml", "XML metadata")
    JSON = ("application/json", "JSON file")
    PLAIN_TEXT = ("text/plain", "Plain text (often metadata)")
    GEOJSON = ("application/geo+json", "GeoJson file")
    GEOPACKAGE = ("application/geopackage+sqlite3", "GeoPackage file")
    HDF5 = ("application/x-hdf5", "Hierarchical Data Format version 5")
    HDF4 = (
        "application/x-hdf",
        "Hierarchical Data Format versions 4 and earlier.",
    )

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in MediaTypeAsset.__members__:
            val = str(MediaTypeAsset[pf_name].value)
            if val == name:
                result = MediaTypeAsset[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "MediaTypeAsset", f"Unknown enum value for {name}"
            )
        return result


class RelationTypes(DocEnum):
    SELF = (
        "self",
        "Absolute URL to the location that the Catalog file can be found online, if available. This is particularly useful when in a download package that includes metadata, so that the downstream user can know where the data has come from.",
    )
    ROOT = (
        "root",
        "URL to the root STAC Catalog or Collection. Catalogs should include a link to their root, even if it's the root and points to itself.",
    )
    PARENT = (
        "parent",
        "URL to the parent STAC entity (Catalog or Collection). Non-root Catalogs should include a link to their parent.",
    )
    CHILD = ("child", "URL to a child STAC entity (Catalog or Collection).")
    ITEM = ("item", "URL to a STAC Item")
    ALTERNATE = (
        "alternate",
        'It is recommended that STAC Items are also available as HTML, and should use this rel with "type" : "text/html" to tell clients where they can get a version of the Item or Collection to view in a browser. See STAC on the Web in Best Practices for more information.',
    )
    CANONICAL = (
        "canonical",
        "The URL of the canonical version of the Item or Collection. API responses and copies of catalogs should use this to inform users that they are direct copy of another STAC Item, using the canonical rel to refer back to the primary location.",
    )
    VIA = (
        "via",
        "The URL of the source metadata that this STAC Item or Collection is created from. Used similarly to canonical, but refers back to a non-STAC record (Landsat MTL, Sentinel tileInfo.json, etc)",
    )
    PREV = (
        "prev",
        "Indicates that the link's context is a part of a series, and that the previous in the series is the link target. Typically used in STAC by API's, to return smaller groups of Items or Catalogs/Collections.",
    )
    NEXT = (
        "next",
        "Indicates that the link's context is a part of a series, and that the next in the series is the link target. Typically used in STAC by API's, to return smaller groups of Items or Catalogs/Collections.",
    )
    PREVIEW = (
        "preview",
        "Refers to a resource that serves as a preview (see RFC 6903, sec. 3), usually a lower resolution thumbnail. In STAC this would usually be the same URL as the thumbnail asset, but adding it as a link in addition enables OGC API clients that can't read assets to make use of it. It also adds support for thumbnails to STAC Catalogs as they can't list assets.",
    )

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in RelationTypes.__members__:
            val = str(RelationTypes[pf_name].value)
            if val == name:
                result = RelationTypes[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "RelationTypes", f"Unknown enum value for {name}"
            )
        return result


class IANARelationTypes(DocEnum):

    ABOUT = (
        "about",
        "Refers to a resource that is the subject of the link's context.",
    )
    ALTERNATE = ("alternate", "Refers to a substitute for this context")
    AMPHTML = (
        "amphtml",
        "Used to reference alternative content that uses the AMP profile of the HTML format.",
    )
    APPENDIX = ("appendix", "Refers to an appendix.")
    APPLE_TOUCH_ICON = (
        "apple-touch-icon",
        "Refers to an icon for the context. Synonym for icon.",
    )
    APPLE_TOUCH_STARTUP_IMAGE = (
        "apple-touch-startup-image",
        "Refers to a launch screen for the context.",
    )
    ARCHIVES = (
        "archives",
        "Refers to a collection of records, documents, or other materials of historical interest.",
    )
    AUTHOR = ("author", "Refers to the context's author.")
    BLOCKED_BY = (
        "blocked-by",
        "Identifies the entity that blocks access to a resource following receipt of a legal demand.",
    )
    BOOKMARK = (
        "bookmark",
        "Gives a permanent link to use for bookmarking purposes.",
    )
    CANONICAL = (
        "canonical",
        "Designates the preferred version of a resource (the IRI and its contents).",
    )
    CHAPTER = ("chapter", "Refers to a chapter in a collection of resources.")
    CITE_AS = (
        "cite-as",
        "Indicates that the link target is preferred over the link context for the purpose of permanent citation.",
    )
    COLLECTION = (
        "collection",
        "The target IRI points to a resource which represents the collection resource for the context IRI.",
    )
    CONTENTS = ("contents", "Refers to a table of contents.")
    CONVERTEDFROM = (
        "convertedFrom",
        'The document linked to was later converted to the document that contains this link relation.  For example, an RFC can have a link to the Internet-Draft that became the RFC; in that case, the link relation would be "convertedFrom".',
    )
    COPYRIGHT = (
        "copyright",
        "Refers to a copyright statement that applies to the link's context.",
    )
    CREATE_FORM = (
        "create-form",
        "The target IRI points to a resource where a submission form can be obtained.",
    )
    CURRENT = (
        "current",
        "Refers to a resource containing the most recent item(s) in a collection of resources.",
    )
    DESCRIBEDBY = (
        "describedby",
        "Refers to a resource providing information about the link's context.",
    )
    DESCRIBES = (
        "describes",
        "The relationship A 'describes' B asserts that resource A provides a description of resource B. There are no constraints on the format or representation of either A or B, neither are there any further constraints on either resource.",
    )
    DISCLOSURE = (
        "disclosure",
        "Refers to a list of patent disclosures made with respect to material for which 'disclosure' relation is specified.",
    )
    DNS_PREFETCH = (
        "dns-prefetch",
        "Used to indicate an origin that will be used to fetch required resources for the link context, and that the user agent ought to resolve as early as possible.",
    )
    DUPLICATE = (
        "duplicate",
        "Refers to a resource whose available representations are byte-for-byte identical with the corresponding representations of the context IRI.",
    )
    EDIT = (
        "edit",
        "Refers to a resource that can be used to edit the link's context.",
    )
    EDIT_FORM = (
        "edit-form",
        "The target IRI points to a resource where a submission form for editing associated resource can be obtained.",
    )
    EDIT_MEDIA = (
        "edit-media",
        "Refers to a resource that can be used to edit media associated with the link's context.",
    )
    ENCLOSURE = (
        "enclosure",
        "Identifies a related resource that is potentially large and might require special handling.",
    )
    EXTERNAL = (
        "external",
        "Refers to a resource that is not part of the same site as the current context.",
    )
    FIRST = (
        "first",
        "An IRI that refers to the furthest preceding resource in a series of resources.",
    )
    GLOSSARY = ("glossary", "Refers to a glossary of terms.")
    HELP = ("help", "Refers to context-sensitive help.")
    HOSTS = (
        "hosts",
        "Refers to a resource hosted by the server indicated by the link context.",
    )
    HUB = (
        "hub",
        "Refers to a hub that enables registration for notification of updates to the context.",
    )
    ICON = ("icon", "Refers to an icon representing the link's context.")
    INDEX = ("index", "Refers to an index.")
    INTERVALAFTER = (
        "intervalAfter",
        "refers to a resource associated with a time interval that ends before the beginning of the time interval associated with the context resource",
    )
    INTERVALBEFORE = (
        "intervalBefore",
        "refers to a resource associated with a time interval that begins after the end of the time interval associated with the context resource",
    )
    INTERVALCONTAINS = (
        "intervalContains",
        "refers to a resource associated with a time interval that begins after the beginning of the time interval associated with the context resource, and ends before the end of the time interval associated with the context resource",
    )
    INTERVALDISJOINT = (
        "intervalDisjoint",
        "refers to a resource associated with a time interval that begins after the end of the time interval associated with the context resource, or ends before the beginning of the time interval associated with the context resource",
    )
    INTERVALDURING = (
        "intervalDuring",
        "refers to a resource associated with a time interval that begins before the beginning of the time interval associated with the context resource, and ends after the end of the time interval associated with the context resource",
    )
    INTERVALEQUALS = (
        "intervalEquals",
        "refers to a resource associated with a time interval whose beginning coincides with the beginning of the time interval associated with the context resource, and whose end coincides with the end of the time interval associated with the context resource",
    )
    INTERVALFINISHEDBY = (
        "intervalFinishedBy",
        "refers to a resource associated with a time interval that begins after the beginning of the time interval associated with the context resource, and whose end coincides with the end of the time interval associated with the context resource",
    )
    INTERVALFINISHES = (
        "intervalFinishes",
        "refers to a resource associated with a time interval that begins before the beginning of the time interval associated with the context resource, and whose end coincides with the end of the time interval associated with the context resource",
    )
    INTERVALIN = (
        "intervalIn",
        "refers to a resource associated with a time interval that begins before or is coincident with the beginning of the time interval associated with the context resource, and ends after or is coincident with the end of the time interval associated with the context resource",
    )
    INTERVALMEETS = (
        "intervalMeets",
        "refers to a resource associated with a time interval whose beginning coincides with the end of the time interval associated with the context resource",
    )
    INTERVALMETBY = (
        "intervalMetBy",
        "refers to a resource associated with a time interval whose end coincides with the beginning of the time interval associated with the context resource",
    )
    INTERVALOVERLAPPEDBY = (
        "intervalOverlappedBy",
        "refers to a resource associated with a time interval that begins before the beginning of the time interval associated with the context resource, and ends after the beginning of the time interval associated with the context resource",
    )
    INTERVALOVERLAPS = (
        "intervalOverlaps",
        "refers to a resource associated with a time interval that begins before the end of the time interval associated with the context resource, and ends after the end of the time interval associated with the context resource",
    )
    INTERVALSTARTEDBY = (
        "intervalStartedBy",
        "refers to a resource associated with a time interval whose beginning coincides with the beginning of the time interval associated with the context resource, and ends before the end of the time interval associated with the context resource",
    )
    INTERVALSTARTS = (
        "intervalStarts",
        "refers to a resource associated with a time interval whose beginning coincides with the beginning of the time interval associated with the context resource, and ends after the end of the time interval associated with the context resource",
    )
    ITEM = (
        "item",
        "The target IRI points to a resource that is a member of the collection represented by the context IRI.",
    )
    LAST = (
        "last",
        "An IRI that refers to the furthest following resource in a series of resources.",
    )
    LATEST_VERSION = (
        "latest-version",
        "Points to a resource containing the latest (e.g., current) version of the context.",
    )
    LICENSE = ("license", "Refers to a license associated with this context.")
    LRDD = (
        "lrdd",
        'Refers to further information about the link\'s context, expressed as a LRDD ("Link-based Resource Descriptor Document") resource.  See [RFC6415] for information about processing this relation type in host-meta documents. When used elsewhere, it refers to additional links and other metadata. Multiple instances indicate additional LRDD resources. LRDD resources MUST have an "application/xrd+xml" representation, and MAY have others.',
    )
    MANIFEST = ("manifest", "Links to a manifest file for the context.")
    MASK_ICON = (
        "mask-icon",
        "Refers to a mask that can be applied to the icon for the context.",
    )
    MEDIA_FEED = (
        "media-feed",
        "Refers to a feed of personalised media recommendations relevant to the link context.",
    )
    MEMENTO = (
        "memento",
        "The Target IRI points to a Memento, a fixed resource that will not change state anymore.",
    )
    MICROPUB = ("micropub", "Links to the context's Micropub endpoint.")
    MODULEPRELOAD = (
        "modulepreload",
        "Refers to a module that the user agent is to preemptively fetch and store for use in the current context.",
    )
    MONITOR = (
        "monitor",
        "Refers to a resource that can be used to monitor changes in an HTTP resource.",
    )
    MONITOR_GROUP = (
        "monitor-group",
        "Refers to a resource that can be used to monitor changes in a specified group of HTTP resources.",
    )
    NEXT = (
        "next",
        "Indicates that the link's context is a part of a series, and that the next in the series is the link target.",
    )
    NEXT_ARCHIVE = (
        "next-archive",
        "Refers to the immediately following archive resource.",
    )
    NOFOLLOW = (
        "nofollow",
        "Indicates that the context’s original author or publisher does not endorse the link target.",
    )
    NOOPENER = (
        "noopener",
        "Indicates that any newly created top-level browsing context which results from following the link will not be an auxiliary browsing context.",
    )
    NOREFERRER = (
        "noreferrer",
        "Indicates that no referrer information is to be leaked when following the link.",
    )
    OPENER = (
        "opener",
        "Indicates that any newly created top-level browsing context which results from following the link will be an auxiliary browsing context.",
    )
    OPENID2_LOCAL_ID = (
        "openid2.local_id",
        "Refers to an OpenID Authentication server on which the context relies for an assertion that the end user controls an Identifier.",
    )
    OPENID2_PROVIDER = (
        "openid2.provider",
        "Refers to a resource which accepts OpenID Authentication protocol messages for the context.",
    )
    ORIGINAL = ("original", "The Target IRI points to an Original Resource.")
    P3PV1 = ("P3Pv1", "Refers to a P3P privacy policy for the context.")
    PAYMENT = ("payment", "Indicates a resource where payment is accepted.")
    PINGBACK = (
        "pingback",
        "Gives the address of the pingback resource for the link context.",
    )
    PRECONNECT = (
        "preconnect",
        "Used to indicate an origin that will be used to fetch required resources for the link context. Initiating an early connection, which includes the DNS lookup, TCP handshake, and optional TLS negotiation, allows the user agent to mask the high latency costs of establishing a connection.",
    )
    PREDECESSOR_VERSION = (
        "predecessor-version",
        "Points to a resource containing the predecessor version in the version history.",
    )
    PREFETCH = (
        "prefetch",
        "The prefetch link relation type is used to identify a resource that might be required by the next navigation from the link context, and that the user agent ought to fetch, such that the user agent can deliver a faster response once the resource is requested in the future.",
    )
    PRELOAD = (
        "preload",
        "Refers to a resource that should be loaded early in the processing of the link's context, without blocking rendering.",
    )
    PRERENDER = (
        "prerender",
        "Used to identify a resource that might be required by the next navigation from the link context, and that the user agent ought to fetch and execute, such that the user agent can deliver a faster response once the resource is requested in the future.",
    )
    PREV = (
        "prev",
        "Indicates that the link's context is a part of a series, and that the previous in the series is the link target.",
    )
    PREVIEW = (
        "preview",
        "Refers to a resource that provides a preview of the link's context.",
    )
    PREVIOUS = (
        "previous",
        'Refers to the previous resource in an ordered series of resources.  Synonym for "prev".',
    )
    PREV_ARCHIVE = (
        "prev-archive",
        "Refers to the immediately preceding archive resource.",
    )
    PRIVACY_POLICY = (
        "privacy-policy",
        "Refers to a privacy policy associated with the link's context.",
    )
    PROFILE = (
        "profile",
        "Identifying that a resource representation conforms to a certain profile, without affecting the non-profile semantics of the resource representation.",
    )
    PUBLICATION = (
        "publication",
        "Links to a publication manifest. A manifest represents structured information about a publication, such as informative metadata, a list of resources, and a default reading order.",
    )
    RELATED = ("related", "Identifies a related resource.")
    RESTCONF = (
        "restconf",
        'Identifies the root of RESTCONF API as configured on this HTTP server. The "restconf" relation defines the root of the API defined in RFC8040. Subsequent revisions of RESTCONF will use alternate relation values to support protocol versioning.',
    )
    REPLIES = (
        "replies",
        "Identifies a resource that is a reply to the context of the link.",
    )
    RULEINPUT = (
        "ruleinput",
        "The resource identified by the link target provides an input value to an instance of a rule, where the resource which represents the rule instance is identified by the link context.",
    )
    SEARCH = (
        "search",
        "Refers to a resource that can be used to search through the link's context and related resources.",
    )
    SECTION = ("section", "Refers to a section in a collection of resources.")
    SELF = ("self", "Conveys an identifier for the link's context.")
    SERVICE = (
        "service",
        "Indicates a URI that can be used to retrieve a service document.",
    )
    SERVICE_DESC = (
        "service-desc",
        "Identifies service description for the context that is primarily intended for consumption by machines.",
    )
    SERVICE_DOC = (
        "service-doc",
        "Identifies service documentation for the context that is primarily intended for human consumption.",
    )
    SERVICE_META = (
        "service-meta",
        "Identifies general metadata for the context that is primarily intended for consumption by machines.",
    )
    SPONSORED = (
        "sponsored",
        "Refers to a resource that is within a context that is sponsored (such as advertising or another compensation agreement).",
    )
    START = (
        "start",
        "Refers to the first resource in a collection of resources.",
    )
    STATUS = (
        "status",
        "Identifies a resource that represents the context's status.",
    )
    STYLESHEET = ("stylesheet", "Refers to a stylesheet.")
    SUBSECTION = (
        "subsection",
        "Refers to a resource serving as a subsection in a collection of resources.",
    )
    SUCCESSOR_VERSION = (
        "successor-version",
        "Points to a resource containing the successor version in the version history.",
    )
    SUNSET = (
        "sunset",
        "Identifies a resource that provides information about the context's retirement policy.",
    )
    TAG = (
        "tag",
        "Gives a tag (identified by the given address) that applies to the current document.",
    )
    TERMS_OF_SERVICE = (
        "terms-of-service",
        "Refers to the terms of service associated with the link's context.",
    )
    TIMEGATE = (
        "timegate",
        "The Target IRI points to a TimeGate for an Original Resource.",
    )
    TIMEMAP = (
        "timemap",
        "The Target IRI points to a TimeMap for an Original Resource.",
    )
    TYPE = (
        "type",
        "Refers to a resource identifying the abstract semantic type of which the link's context is considered to be an instance.",
    )
    UGC = (
        "ugc",
        "Refers to a resource that is within a context that is User Generated Content.",
    )
    UP = ("up", "Refers to a parent document in a hierarchy of documents.")
    VERSION_HISTORY = (
        "version-history",
        "Points to a resource containing the version history for the context.",
    )
    VIA = (
        "via",
        "Identifies a resource that is the source of the information in the link's context.",
    )
    WEBMENTION = (
        "webmention",
        "Identifies a target URI that supports the Webmention protocol. This allows clients that mention a resource in some form of publishing process to contact that endpoint and inform it that this resource has been mentioned.",
    )
    WORKING_COPY = (
        "working-copy",
        "Points to a working copy for this resource.",
    )
    WORKING_COPY_OF = (
        "working-copy-of",
        "Points to the versioned resource from which this working copy was obtained.",
    )

    @staticmethod
    def source():
        return {
            "last_updated": "2020-11-16",
            "source": "https://www.iana.org/assignments/link-relations/link-relations-1.csv",
        }

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in IANARelationTypes.__members__:
            val = str(IANARelationTypes[pf_name].value)
            if val == name:
                result = IANARelationTypes[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "IANARelationTypes", f"Unknown enum value for {name}"
            )
        return result


class RoleType(DocEnum):
    LICENSOR = (
        "licensor",
        "The organization that is licensing the dataset under the license specified in the Collection's license field",
    )
    PRODUCER = (
        "producer",
        "The producer of the data is the provider that initially captured and processed the source data",
    )
    PROCESSOR = (
        "processor",
        "A processor is any provider who processed data to a derived product.",
    )
    HOST = (
        "host",
        "The host is the actual provider offering the data on their storage. There should be no more than one host, specified as last element of the list.",
    )

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in RoleType.__members__:
            val = str(RoleType[pf_name].value)
            if val == name:
                result = RoleType[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "RoleType", f"Unknown enum value for {name}"
            )
        return result


class RoleAsset(DocEnum):
    THUMBNAIL = (
        "thumbnail",
        "An asset that represents a thumbnail of the Item, typically a true color image (for Items with assets in the visible wavelengths), lower-resolution (typically smaller 600x600 pixels), and typically a JPEG or PNG (suitable for display in a web browser). Multiple assets may have this purpose, but it recommended that the type and roles be unique tuples. For example, Sentinel-2 L2A provides thumbnail images in both JPEG and JPEG2000 formats, and would be distinguished by their media types.",
    )
    OVERVIEW = (
        "overview",
        "An asset that represents a possibly larger view than the thumbnail of the Item, for example, a true color composite of multi-band data.",
    )
    DATA = (
        "data",
        "The data itself. This is a suggestion for a common role for data files to be used in case data providers don't come up with their own names and semantics.",
    )
    METADATA = (
        "metadata",
        "A metadata sidecar file describing the data in this Item, for example the Landsat-8 MTL file.",
    )
    VISUAL = (
        "visual",
        "An asset that is a full resolution version of the data, processed for visual use (RGB only, often sharpened (pan-sharpened and/or using an unsharp mask)).",
    )
    DATE = (
        "date",
        "An asset that provides per-pixel acquisition timestamps, typically serving as metadata to another asset",
    )
    GRAPHIC = (
        "graphic",
        "Supporting plot, illustration, or graph associated with the Item",
    )
    DATA_MASK = (
        "data-mask",
        "File indicating if corresponding pixels have Valid data and various types of invalid data",
    )
    SNOW_ICE = (
        "snow-ice",
        "Points to a file that indicates whether a pixel is assessed as being snow/ice or not.",
    )
    LAND_WATER = (
        "land-water",
        "Points to a file that indicates whether a pixel is assessed as being land or water.",
    )
    WATER_MASK = (
        "water-mask",
        "Points to a file that indicates whether a pixel is assessed as being water (e.g. flooding map).",
    )
    ISO19115 = ("iso-19115", "Points to an ISO 19115 metadata file")

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in RoleAsset.__members__:
            val = str(RoleAsset[pf_name].value)
            if val == name:
                result = RoleAsset[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "RoleAsset", f"Unknown enum value for {name}"
            )
        return result


class LicenseType(DocEnum):
    AAL = ("AAL", "Attribution Assurance License")
    ABSTYLES = ("Abstyles", "Abstyles License")
    OBSD = ("0BSD", "BSD Zero Clause License")
    ADOBE_2006 = (
        "Adobe-2006",
        "Adobe Systems Incorporated Source Code License Agreement",
    )
    ADOBE_GLYPH = ("Adobe-Glyph", "Adobe Glyph List License")
    ADSL = ("ADSL", "Amazon Digital Services License")
    AFL_1_1 = ("AFL-1.1", "Academic Free License v1.1")
    AFL_1_2 = ("AFL-1.2", "Academic Free License v1.2")
    AFL_2_0 = ("AFL-2.0", "Academic Free License v2.0")
    AFL_2_1 = ("AFL-2.1", "Academic Free License v2.1")
    AFL_3_0 = ("AFL-3.0", "Academic Free License v3.0")
    AFMPARSE = ("Afmparse", "Afmparse License")
    AGPL_1_0_ONLY = (
        "AGPL-1.0-only",
        "Affero General Public License v1.0 only",
    )
    AGPL_1_0_OR_LATER = (
        "AGPL-1.0-or-later",
        "Affero General Public License v1.0 or later",
    )
    AGPL_3_0_ONLY = (
        "AGPL-3.0-only",
        "GNU Affero General Public License v3.0 only",
    )
    AGPL_3_0_OR_LATER = (
        "AGPL-3.0-or-later",
        "GNU Affero General Public License v3.0 or later",
    )
    ALADDIN = ("Aladdin", "Aladdin Free Public License")
    AMDPLPA = ("AMDPLPA", "AMD's plpa_map.c License")
    AML = ("AML", "Apple MIT License")
    AMPAS = ("AMPAS", "Academy of Motion Picture Arts and Sciences BSD")
    ANTLR_PD = ("ANTLR-PD", "ANTLR Software Rights Notice")
    ANTLR_PD_FALLBACK = (
        "ANTLR-PD-fallback",
        "ANTLR Software Rights Notice with license fallback",
    )
    APACHE_1_0 = ("Apache-1.0", "Apache License 1.0")
    APACHE_1_1 = ("Apache-1.1", "Apache License 1.1")
    APACHE_2_0 = ("Apache-2.0", "Apache License 2.0")
    APAFML = ("APAFML", "Adobe Postscript AFM License")
    APL_1_0 = ("APL-1.0", "Adaptive Public License 1.0")
    APSL_1_0 = ("APSL-1.0", "Apple Public Source License 1.0")
    APSL_1_1 = ("APSL-1.1", "Apple Public Source License 1.1")
    APSL_1_2 = ("APSL-1.2", "Apple Public Source License 1.2")
    APSL_2_0 = ("APSL-2.0", "Apple Public Source License 2.0")
    ARTISTIC_1_0 = ("Artistic-1.0", "Artistic License 1.0")
    ARTISTIC_1_0_CL8 = ("Artistic-1.0-cl8", "Artistic License 1.0 w/clause 8")
    ARTISTIC_1_0_PERL = ("Artistic-1.0-Perl", "Artistic License 1.0 (Perl)")
    ARTISTIC_2_0 = ("Artistic-2.0", "Artistic License 2.0")
    BAHYPH = ("Bahyph", "Bahyph License")
    BARR = ("Barr", "Barr License")
    BEERWARE = ("Beerware", "Beerware License")
    BITTORRENT_1_0 = ("BitTorrent-1.0", "BitTorrent Open Source License v1.0")
    BITTORRENT_1_1 = ("BitTorrent-1.1", "BitTorrent Open Source License v1.1")
    BLESSING = ("blessing", "SQLite Blessing")
    BLUEOAK_1_0_0 = ("BlueOak-1.0.0", "Blue Oak Model License 1.0.0")
    BORCEUX = ("Borceux", "Borceux license")
    BSD_1_CLAUSE = ("BSD-1-Clause", "BSD 1-Clause License")
    BSD_2_CLAUSE = ("BSD-2-Clause", 'BSD 2-Clause "Simplified" License')
    BSD_2_CLAUSE_PATENT = (
        "BSD-2-Clause-Patent",
        "BSD-2-Clause Plus Patent License",
    )
    BSD_2_CLAUSE_VIEWS = (
        "BSD-2-Clause-Views",
        "BSD 2-Clause with views sentence",
    )
    BSD_3_CLAUSE = ("BSD-3-Clause", 'BSD 3-Clause "New" or "Revised" License')
    BSD_3_CLAUSE_ATTRIBUTION = (
        "BSD-3-Clause-Attribution",
        "BSD with attribution",
    )
    BSD_3_CLAUSE_CLEAR = ("BSD-3-Clause-Clear", "BSD 3-Clause Clear License")
    BSD_3_CLAUSE_LBNL = (
        "BSD-3-Clause-LBNL",
        "Lawrence Berkeley National Labs BSD variant license",
    )
    BSD_3_CLAUSE_MODIFICATION = (
        "BSD-3-Clause-Modification",
        "BSD 3-Clause Modification",
    )
    BSD_3_CLAUSE_NO_MILITARY_LICENSE = (
        "BSD-3-Clause-No-Military-License",
        "BSD 3-Clause No Military License",
    )
    BSD_3_CLAUSE_NO_NUCLEAR_LICENSE = (
        "BSD-3-Clause-No-Nuclear-License",
        "BSD 3-Clause No Nuclear License",
    )
    BSD_3_CLAUSE_NO_NUCLEAR_LICENSE_2014 = (
        "BSD-3-Clause-No-Nuclear-License-2014",
        "BSD 3-Clause No Nuclear License 2014",
    )
    BSD_3_CLAUSE_NO_NUCLEAR_WARRANTY = (
        "BSD-3-Clause-No-Nuclear-Warranty",
        "BSD 3-Clause No Nuclear Warranty",
    )
    BSD_3_CLAUSE_OPEN_MPI = (
        "BSD-3-Clause-Open-MPI",
        "BSD 3-Clause Open MPI variant",
    )
    BSD_4_CLAUSE = ("BSD-4-Clause", 'BSD 4-Clause "Original" or "Old" License')
    BSD_4_CLAUSE_SHORTENED = (
        "BSD-4-Clause-Shortened",
        "BSD 4 Clause Shortened",
    )
    BSD_4_CLAUSE_UC = (
        "BSD-4-Clause-UC",
        "BSD-4-Clause (University of California-Specific)",
    )
    BSD_PROTECTION = ("BSD-Protection", "BSD Protection License")
    BSD_SOURCE_CODE = ("BSD-Source-Code", "BSD Source Code Attribution")
    BSL_1_0 = ("BSL-1.0", "Boost Software License 1.0")
    BUSL_1_1 = ("BUSL-1.1", "Business Source License 1.1")
    BZIP2_1_0_5 = ("bzip2-1.0.5", "bzip2 and libbzip2 License v1.0.5")
    BZIP2_1_0_6 = ("bzip2-1.0.6", "bzip2 and libbzip2 License v1.0.6")
    C_UDA_1_0 = ("C-UDA-1.0", "Computational Use of Data Agreement v1.0")
    CAL_1_0 = ("CAL-1.0", "Cryptographic Autonomy License 1.0")
    CAL_1_0_COMBINED_WORK_EXCEPTION = (
        "CAL-1.0-Combined-Work-Exception",
        "Cryptographic Autonomy License 1.0 (Combined Work Exception)",
    )
    CALDERA = ("Caldera", "Caldera License")
    CATOSL_1_1 = (
        "CATOSL-1.1",
        "Computer Associates Trusted Open Source License 1.1",
    )
    CC_BY_1_0 = ("CC-BY-1.0", "Creative Commons Attribution 1.0 Generic")
    CC_BY_2_0 = ("CC-BY-2.0", "Creative Commons Attribution 2.0 Generic")
    CC_BY_2_5 = ("CC-BY-2.5", "Creative Commons Attribution 2.5 Generic")
    CC_BY_2_5_AU = (
        "CC-BY-2.5-AU",
        "Creative Commons Attribution 2.5 Australia",
    )
    CC_BY_3_0 = ("CC-BY-3.0", "Creative Commons Attribution 3.0 Unported")
    CC_BY_3_0_AT = ("CC-BY-3.0-AT", "Creative Commons Attribution 3.0 Austria")
    CC_BY_3_0_DE = ("CC-BY-3.0-DE", "Creative Commons Attribution 3.0 Germany")
    CC_BY_3_0_NL = (
        "CC-BY-3.0-NL",
        "Creative Commons Attribution 3.0 Netherlands",
    )
    CC_BY_3_0_US = (
        "CC-BY-3.0-US",
        "Creative Commons Attribution 3.0 United States",
    )
    CC_BY_4_0 = ("CC-BY-4.0", "Creative Commons Attribution 4.0 International")
    CC_BY_NC_1_0 = (
        "CC-BY-NC-1.0",
        "Creative Commons Attribution Non Commercial 1.0 Generic",
    )
    CC_BY_NC_2_0 = (
        "CC-BY-NC-2.0",
        "Creative Commons Attribution Non Commercial 2.0 Generic",
    )
    CC_BY_NC_2_5 = (
        "CC-BY-NC-2.5",
        "Creative Commons Attribution Non Commercial 2.5 Generic",
    )
    CC_BY_NC_3_0 = (
        "CC-BY-NC-3.0",
        "Creative Commons Attribution Non Commercial 3.0 Unported",
    )
    CC_BY_NC_3_0_DE = (
        "CC-BY-NC-3.0-DE",
        "Creative Commons Attribution Non Commercial 3.0 Germany",
    )
    CC_BY_NC_4_0 = (
        "CC-BY-NC-4.0",
        "Creative Commons Attribution Non Commercial 4.0 International",
    )
    CC_BY_NC_ND_1_0 = (
        "CC-BY-NC-ND-1.0",
        "Creative Commons Attribution Non Commercial No Derivatives 1.0 Generic",
    )
    CC_BY_NC_ND_2_0 = (
        "CC-BY-NC-ND-2.0",
        "Creative Commons Attribution Non Commercial No Derivatives 2.0 Generic",
    )
    CC_BY_NC_ND_2_5 = (
        "CC-BY-NC-ND-2.5",
        "Creative Commons Attribution Non Commercial No Derivatives 2.5 Generic",
    )
    CC_BY_NC_ND_3_0 = (
        "CC-BY-NC-ND-3.0",
        "Creative Commons Attribution Non Commercial No Derivatives 3.0 Unported",
    )
    CC_BY_NC_ND_3_0_DE = (
        "CC-BY-NC-ND-3.0-DE",
        "Creative Commons Attribution Non Commercial No Derivatives 3.0 Germany",
    )
    CC_BY_NC_ND_3_0_IGO = (
        "CC-BY-NC-ND-3.0-IGO",
        "Creative Commons Attribution Non Commercial No Derivatives 3.0 IGO",
    )
    CC_BY_NC_ND_4_0 = (
        "CC-BY-NC-ND-4.0",
        "Creative Commons Attribution Non Commercial No Derivatives 4.0 International",
    )
    CC_BY_NC_SA_1_0 = (
        "CC-BY-NC-SA-1.0",
        "Creative Commons Attribution Non Commercial Share Alike 1.0 Generic",
    )
    CC_BY_NC_SA_2_0 = (
        "CC-BY-NC-SA-2.0",
        "Creative Commons Attribution Non Commercial Share Alike 2.0 Generic",
    )
    CC_BY_NC_SA_2_0_FR = (
        "CC-BY-NC-SA-2.0-FR",
        "Creative Commons Attribution-NonCommercial-ShareAlike 2.0 France",
    )
    CC_BY_NC_SA_2_0_UK = (
        "CC-BY-NC-SA-2.0-UK",
        "Creative Commons Attribution Non Commercial Share Alike 2.0 England and Wales",
    )
    CC_BY_NC_SA_2_5 = (
        "CC-BY-NC-SA-2.5",
        "Creative Commons Attribution Non Commercial Share Alike 2.5 Generic",
    )
    CC_BY_NC_SA_3_0 = (
        "CC-BY-NC-SA-3.0",
        "Creative Commons Attribution Non Commercial Share Alike 3.0 Unported",
    )
    CC_BY_NC_SA_3_0_DE = (
        "CC-BY-NC-SA-3.0-DE",
        "Creative Commons Attribution Non Commercial Share Alike 3.0 Germany",
    )
    CC_BY_NC_SA_3_0_IGO = (
        "CC-BY-NC-SA-3.0-IGO",
        "Creative Commons Attribution Non Commercial Share Alike 3.0 IGO",
    )
    CC_BY_NC_SA_4_0 = (
        "CC-BY-NC-SA-4.0",
        "Creative Commons Attribution Non Commercial Share Alike 4.0 International",
    )
    CC_BY_ND_1_0 = (
        "CC-BY-ND-1.0",
        "Creative Commons Attribution No Derivatives 1.0 Generic",
    )
    CC_BY_ND_2_0 = (
        "CC-BY-ND-2.0",
        "Creative Commons Attribution No Derivatives 2.0 Generic",
    )
    CC_BY_ND_2_5 = (
        "CC-BY-ND-2.5",
        "Creative Commons Attribution No Derivatives 2.5 Generic",
    )
    CC_BY_ND_3_0 = (
        "CC-BY-ND-3.0",
        "Creative Commons Attribution No Derivatives 3.0 Unported",
    )
    CC_BY_ND_3_0_DE = (
        "CC-BY-ND-3.0-DE",
        "Creative Commons Attribution No Derivatives 3.0 Germany",
    )
    CC_BY_ND_4_0 = (
        "CC-BY-ND-4.0",
        "Creative Commons Attribution No Derivatives 4.0 International",
    )
    CC_BY_SA_1_0 = (
        "CC-BY-SA-1.0",
        "Creative Commons Attribution Share Alike 1.0 Generic",
    )
    CC_BY_SA_2_0 = (
        "CC-BY-SA-2.0",
        "Creative Commons Attribution Share Alike 2.0 Generic",
    )
    CC_BY_SA_2_0_UK = (
        "CC-BY-SA-2.0-UK",
        "Creative Commons Attribution Share Alike 2.0 England and Wales",
    )
    CC_BY_SA_2_1_JP = (
        "CC-BY-SA-2.1-JP",
        "Creative Commons Attribution Share Alike 2.1 Japan",
    )
    CC_BY_SA_2_5 = (
        "CC-BY-SA-2.5",
        "Creative Commons Attribution Share Alike 2.5 Generic",
    )
    CC_BY_SA_3_0 = (
        "CC-BY-SA-3.0",
        "Creative Commons Attribution Share Alike 3.0 Unported",
    )
    CC_BY_SA_3_0_AT = (
        "CC-BY-SA-3.0-AT",
        "Creative Commons Attribution Share Alike 3.0 Austria",
    )
    CC_BY_SA_3_0_DE = (
        "CC-BY-SA-3.0-DE",
        "Creative Commons Attribution Share Alike 3.0 Germany",
    )
    CC_BY_SA_4_0 = (
        "CC-BY-SA-4.0",
        "Creative Commons Attribution Share Alike 4.0 International",
    )
    CC_PDDC = (
        "CC-PDDC",
        "Creative Commons Public Domain Dedication and Certification",
    )
    CC0_1_0 = ("CC0-1.0", "Creative Commons Zero v1.0 Universal")
    CDDL_1_0 = ("CDDL-1.0", "Common Development and Distribution License 1.0")
    CDDL_1_1 = ("CDDL-1.1", "Common Development and Distribution License 1.1")
    CDL_1_0 = ("CDL-1.0", "Common Documentation License 1.0")
    CDLA_PERMISSIVE_1_0 = (
        "CDLA-Permissive-1.0",
        "Community Data License Agreement Permissive 1.0",
    )
    CDLA_PERMISSIVE_2_0 = (
        "CDLA-Permissive-2.0",
        "Community Data License Agreement Permissive 2.0",
    )
    CDLA_SHARING_1_0 = (
        "CDLA-Sharing-1.0",
        "Community Data License Agreement Sharing 1.0",
    )
    CECILL_1_0 = ("CECILL-1.0", "CeCILL Free Software License Agreement v1.0")
    CECILL_1_1 = ("CECILL-1.1", "CeCILL Free Software License Agreement v1.1")
    CECILL_2_0 = ("CECILL-2.0", "CeCILL Free Software License Agreement v2.0")
    CECILL_2_1 = ("CECILL-2.1", "CeCILL Free Software License Agreement v2.1")
    CECILL_B = ("CECILL-B", "CeCILL-B Free Software License Agreement")
    CECILL_C = ("CECILL-C", "CeCILL-C Free Software License Agreement")
    CERN_OHL_1_1 = ("CERN-OHL-1.1", "CERN Open Hardware Licence v1.1")
    CERN_OHL_1_2 = ("CERN-OHL-1.2", "CERN Open Hardware Licence v1.2")
    CERN_OHL_P_2_0 = (
        "CERN-OHL-P-2.0",
        "CERN Open Hardware Licence Version 2 - Permissive",
    )
    CERN_OHL_S_2_0 = (
        "CERN-OHL-S-2.0",
        "CERN Open Hardware Licence Version 2 - Strongly Reciprocal",
    )
    CERN_OHL_W_2_0 = (
        "CERN-OHL-W-2.0",
        "CERN Open Hardware Licence Version 2 - Weakly Reciprocal",
    )
    CLARTISTIC = ("ClArtistic", "Clarified Artistic License")
    CNRI_JYTHON = ("CNRI-Jython", "CNRI Jython License")
    CNRI_PYTHON = ("CNRI-Python", "CNRI Python License")
    CNRI_PYTHON_GPL_COMPATIBLE = (
        "CNRI-Python-GPL-Compatible",
        "CNRI Python Open Source GPL Compatible License Agreement",
    )
    CONDOR_1_1 = ("Condor-1.1", "Condor Public License v1.1")
    COPYLEFT_NEXT_0_3_0 = ("copyleft-next-0.3.0", "copyleft-next 0.3.0")
    COPYLEFT_NEXT_0_3_1 = ("copyleft-next-0.3.1", "copyleft-next 0.3.1")
    CPAL_1_0 = ("CPAL-1.0", "Common Public Attribution License 1.0")
    CPL_1_0 = ("CPL-1.0", "Common Public License 1.0")
    CPOL_1_02 = ("CPOL-1.02", "Code Project Open License 1.02")
    CROSSWORD = ("Crossword", "Crossword License")
    CRYSTALSTACKER = ("CrystalStacker", "CrystalStacker License")
    CUA_OPL_1_0 = ("CUA-OPL-1.0", "CUA Office Public License v1.0")
    CUBE = ("Cube", "Cube License")
    CURL = ("curl", "curl License")
    D_FSL_1_0 = ("D-FSL-1.0", "Deutsche Freie Software Lizenz")
    DIFFMARK = ("diffmark", "diffmark license")
    DOC = ("DOC", "DOC License")
    DOTSEQN = ("Dotseqn", "Dotseqn License")
    DRL_1_0 = ("DRL-1.0", "Detection Rule License 1.0")
    DSDP = ("DSDP", "DSDP License")
    DVIPDFM = ("dvipdfm", "dvipdfm License")
    ECL_1_0 = ("ECL-1.0", "Educational Community License v1.0")
    ECL_2_0 = ("ECL-2.0", "Educational Community License v2.0")
    EFL_1_0 = ("EFL-1.0", "Eiffel Forum License v1.0")
    EFL_2_0 = ("EFL-2.0", "Eiffel Forum License v2.0")
    EGENIX = ("eGenix", "eGenix.com Public License 1.1.0")
    ENTESSA = ("Entessa", "Entessa Public License v1.0")
    EPICS = ("EPICS", "EPICS Open License")
    EPL_1_0 = ("EPL-1.0", "Eclipse Public License 1.0")
    EPL_2_0 = ("EPL-2.0", "Eclipse Public License 2.0")
    ERLPL_1_1 = ("ErlPL-1.1", "Erlang Public License v1.1")
    ETALAB_2_0 = ("etalab-2.0", "Etalab Open License 2.0")
    EUDATAGRID = ("EUDatagrid", "EU DataGrid Software License")
    EUPL_1_0 = ("EUPL-1.0", "European Union Public License 1.0")
    EUPL_1_1 = ("EUPL-1.1", "European Union Public License 1.1")
    EUPL_1_2 = ("EUPL-1.2", "European Union Public License 1.2")
    EUROSYM = ("Eurosym", "Eurosym License")
    FAIR = ("Fair", "Fair License")
    FRAMEWORX_1_0 = ("Frameworx-1.0", "Frameworx Open License 1.0")
    FREEBSD_DOC = ("FreeBSD-DOC", "FreeBSD Documentation License")
    FREEIMAGE = ("FreeImage", "FreeImage Public License v1.0")
    FSFAP = ("FSFAP", "FSF All Permissive License")
    FSFUL = ("FSFUL", "FSF Unlimited License")
    FSFULLR = ("FSFULLR", "FSF Unlimited License (with License Retention)")
    FTL = ("FTL", "Freetype Project License")
    GD = ("GD", "GD License")
    GFDL_1_1_INVARIANTS_ONLY = (
        "GFDL-1.1-invariants-only",
        "GNU Free Documentation License v1.1 only - invariants",
    )
    GFDL_1_1_INVARIANTS_OR_LATER = (
        "GFDL-1.1-invariants-or-later",
        "GNU Free Documentation License v1.1 or later - invariants",
    )
    GFDL_1_1_NO_INVARIANTS_ONLY = (
        "GFDL-1.1-no-invariants-only",
        "GNU Free Documentation License v1.1 only - no invariants",
    )
    GFDL_1_1_NO_INVARIANTS_OR_LATER = (
        "GFDL-1.1-no-invariants-or-later",
        "GNU Free Documentation License v1.1 or later - no invariants",
    )
    GFDL_1_1_ONLY = (
        "GFDL-1.1-only",
        "GNU Free Documentation License v1.1 only",
    )
    GFDL_1_1_OR_LATER = (
        "GFDL-1.1-or-later",
        "GNU Free Documentation License v1.1 or later",
    )
    GFDL_1_2_INVARIANTS_ONLY = (
        "GFDL-1.2-invariants-only",
        "GNU Free Documentation License v1.2 only - invariants",
    )
    GFDL_1_2_INVARIANTS_OR_LATER = (
        "GFDL-1.2-invariants-or-later",
        "GNU Free Documentation License v1.2 or later - invariants",
    )
    GFDL_1_2_NO_INVARIANTS_ONLY = (
        "GFDL-1.2-no-invariants-only",
        "GNU Free Documentation License v1.2 only - no invariants",
    )
    GFDL_1_2_NO_INVARIANTS_OR_LATER = (
        "GFDL-1.2-no-invariants-or-later",
        "GNU Free Documentation License v1.2 or later - no invariants",
    )
    GFDL_1_2_ONLY = (
        "GFDL-1.2-only",
        "GNU Free Documentation License v1.2 only",
    )
    GFDL_1_2_OR_LATER = (
        "GFDL-1.2-or-later",
        "GNU Free Documentation License v1.2 or later",
    )
    GFDL_1_3_INVARIANTS_ONLY = (
        "GFDL-1.3-invariants-only",
        "GNU Free Documentation License v1.3 only - invariants",
    )
    GFDL_1_3_INVARIANTS_OR_LATER = (
        "GFDL-1.3-invariants-or-later",
        "GNU Free Documentation License v1.3 or later - invariants",
    )
    GFDL_1_3_NO_INVARIANTS_ONLY = (
        "GFDL-1.3-no-invariants-only",
        "GNU Free Documentation License v1.3 only - no invariants",
    )
    GFDL_1_3_NO_INVARIANTS_OR_LATER = (
        "GFDL-1.3-no-invariants-or-later",
        "GNU Free Documentation License v1.3 or later - no invariants",
    )
    GFDL_1_3_ONLY = (
        "GFDL-1.3-only",
        "GNU Free Documentation License v1.3 only",
    )
    GFDL_1_3_OR_LATER = (
        "GFDL-1.3-or-later",
        "GNU Free Documentation License v1.3 or later",
    )
    GIFTWARE = ("Giftware", "Giftware License")
    GL2PS = ("GL2PS", "GL2PS License")
    GLIDE = ("Glide", "3dfx Glide License")
    GLULXE = ("Glulxe", "Glulxe License")
    GLWTPL = ("GLWTPL", "Good Luck With That Public License")
    GNUPLOT = ("gnuplot", "gnuplot License")
    GPL_1_0_ONLY = ("GPL-1.0-only", "GNU General Public License v1.0 only")
    GPL_1_0_OR_LATER = (
        "GPL-1.0-or-later",
        "GNU General Public License v1.0 or later",
    )
    GPL_2_0_ONLY = ("GPL-2.0-only", "GNU General Public License v2.0 only")
    GPL_2_0_OR_LATER = (
        "GPL-2.0-or-later",
        "GNU General Public License v2.0 or later",
    )
    GPL_3_0_ONLY = ("GPL-3.0-only", "GNU General Public License v3.0 only")
    GPL_3_0_OR_LATER = (
        "GPL-3.0-or-later",
        "GNU General Public License v3.0 or later",
    )
    GSOAP_1_3B = ("gSOAP-1.3b", "gSOAP Public License v1.3b")
    HASKELLREPORT = ("HaskellReport", "Haskell Language Report License")
    HIPPOCRATIC_2_1 = ("Hippocratic-2.1", "Hippocratic License 2.1")
    HPND = ("HPND", "Historical Permission Notice and Disclaimer")
    HPND_SELL_VARIANT = (
        "HPND-sell-variant",
        "Historical Permission Notice and Disclaimer - sell variant",
    )
    HTMLTIDY = ("HTMLTIDY", "HTML Tidy License")
    IBM_PIBS = ("IBM-pibs", "IBM PowerPC Initialization and Boot Software")
    ICU = ("ICU", "ICU License")
    IJG = ("IJG", "Independent JPEG Group License")
    IMAGEMAGICK = ("ImageMagick", "ImageMagick License")
    IMATIX = ("iMatix", "iMatix Standard Function Library Agreement")
    IMLIB2 = ("Imlib2", "Imlib2 License")
    INFO_ZIP = ("Info-ZIP", "Info-ZIP License")
    INTEL = ("Intel", "Intel Open Source License")
    INTEL_ACPI = ("Intel-ACPI", "Intel ACPI Software License Agreement")
    INTERBASE_1_0 = ("Interbase-1.0", "Interbase Public License v1.0")
    IPA = ("IPA", "IPA Font License")
    IPL_1_0 = ("IPL-1.0", "IBM Public License v1.0")
    ISC = ("ISC", "ISC License")
    JASPER_2_0 = ("JasPer-2.0", "JasPer License")
    JPNIC = ("JPNIC", "Japan Network Information Center License")
    JSON = ("JSON", "JSON License")
    LAL_1_2 = ("LAL-1.2", "Licence Art Libre 1.2")
    LAL_1_3 = ("LAL-1.3", "Licence Art Libre 1.3")
    LATEX2E = ("Latex2e", "Latex2e License")
    LEPTONICA = ("Leptonica", "Leptonica License")
    LGPL_2_0_ONLY = (
        "LGPL-2.0-only",
        "GNU Library General Public License v2 only",
    )
    LGPL_2_0_OR_LATER = (
        "LGPL-2.0-or-later",
        "GNU Library General Public License v2 or later",
    )
    LGPL_2_1_ONLY = (
        "LGPL-2.1-only",
        "GNU Lesser General Public License v2.1 only",
    )
    LGPL_2_1_OR_LATER = (
        "LGPL-2.1-or-later",
        "GNU Lesser General Public License v2.1 or later",
    )
    LGPL_3_0_ONLY = (
        "LGPL-3.0-only",
        "GNU Lesser General Public License v3.0 only",
    )
    LGPL_3_0_OR_LATER = (
        "LGPL-3.0-or-later",
        "GNU Lesser General Public License v3.0 or later",
    )
    LGPLLR = (
        "LGPLLR",
        "Lesser General Public License For Linguistic Resources",
    )
    LIBPNG = ("Libpng", "libpng License")
    LIBPNG_2_0 = ("libpng-2.0", "PNG Reference Library version 2")
    LIBSELINUX_1_0 = ("libselinux-1.0", "libselinux public domain notice")
    LIBTIFF = ("libtiff", "libtiff License")
    LILIQ_P_1_1 = (
        "LiLiQ-P-1.1",
        "Licence Libre du Québec – Permissive version 1.1",
    )
    LILIQ_R_1_1 = (
        "LiLiQ-R-1.1",
        "Licence Libre du Québec – Réciprocité version 1.1",
    )
    LILIQ_RPLUS_1_1 = (
        "LiLiQ-Rplus-1.1",
        "Licence Libre du Québec – Réciprocité forte version 1.1",
    )
    LINUX_OPENIB = (
        "Linux-OpenIB",
        "Linux Kernel Variant of OpenIB.org license",
    )
    LPL_1_0 = ("LPL-1.0", "Lucent Public License Version 1.0")
    LPL_1_02 = ("LPL-1.02", "Lucent Public License v1.02")
    LPPL_1_0 = ("LPPL-1.0", "LaTeX Project Public License v1.0")
    LPPL_1_1 = ("LPPL-1.1", "LaTeX Project Public License v1.1")
    LPPL_1_2 = ("LPPL-1.2", "LaTeX Project Public License v1.2")
    LPPL_1_3A = ("LPPL-1.3a", "LaTeX Project Public License v1.3a")
    LPPL_1_3C = ("LPPL-1.3c", "LaTeX Project Public License v1.3c")
    MAKEINDEX = ("MakeIndex", "MakeIndex License")
    MIROS = ("MirOS", "The MirOS Licence")
    MIT = ("MIT", "MIT License")
    MIT_0 = ("MIT-0", "MIT No Attribution")
    MIT_ADVERTISING = ("MIT-advertising", "Enlightenment License (e16)")
    MIT_CMU = ("MIT-CMU", "CMU License")
    MIT_ENNA = ("MIT-enna", "enna License")
    MIT_FEH = ("MIT-feh", "feh License")
    MIT_MODERN_VARIANT = ("MIT-Modern-Variant", "MIT License Modern Variant")
    MIT_OPEN_GROUP = ("MIT-open-group", "MIT Open Group variant")
    MITNFA = ("MITNFA", "MIT +no-false-attribs license")
    MOTOSOTO = ("Motosoto", "Motosoto License")
    MPICH2 = ("mpich2", "mpich2 License")
    MPL_1_0 = ("MPL-1.0", "Mozilla Public License 1.0")
    MPL_1_1 = ("MPL-1.1", "Mozilla Public License 1.1")
    MPL_2_0 = ("MPL-2.0", "Mozilla Public License 2.0")
    MPL_2_0_NO_COPYLEFT_EXCEPTION = (
        "MPL-2.0-no-copyleft-exception",
        "Mozilla Public License 2.0 (no copyleft exception)",
    )
    MS_PL = ("MS-PL", "Microsoft Public License")
    MS_RL = ("MS-RL", "Microsoft Reciprocal License")
    MTLL = ("MTLL", "Matrix Template Library License")
    MULANPSL_1_0 = (
        "MulanPSL-1.0",
        "Mulan Permissive Software License, Version 1",
    )
    MULANPSL_2_0 = (
        "MulanPSL-2.0",
        "Mulan Permissive Software License, Version 2",
    )
    MULTICS = ("Multics", "Multics License")
    MUP = ("Mup", "Mup License")
    NAIST_2003 = (
        "NAIST-2003",
        "Nara Institute of Science and Technology License (2003)",
    )
    NASA_1_3 = ("NASA-1.3", "NASA Open Source Agreement 1.3")
    NAUMEN = ("Naumen", "Naumen Public License")
    NBPL_1_0 = ("NBPL-1.0", "Net Boolean Public License v1")
    NCGL_UK_2_0 = ("NCGL-UK-2.0", "Non-Commercial Government Licence")
    NCSA = ("NCSA", "University of Illinois/NCSA Open Source License")
    NET_SNMP = ("Net-SNMP", "Net-SNMP License")
    NETCDF = ("NetCDF", "NetCDF license")
    NEWSLETR = ("Newsletr", "Newsletr License")
    NGPL = ("NGPL", "Nethack General Public License")
    NIST_PD = ("NIST-PD", "NIST Public Domain Notice")
    NIST_PD_FALLBACK = (
        "NIST-PD-fallback",
        "NIST Public Domain Notice with license fallback",
    )
    NLOD_1_0 = (
        "NLOD-1.0",
        "Norwegian Licence for Open Government Data (NLOD) 1.0",
    )
    NLOD_2_0 = (
        "NLOD-2.0",
        "Norwegian Licence for Open Government Data (NLOD) 2.0",
    )
    NLPL = ("NLPL", "No Limit Public License")
    NOKIA = ("Nokia", "Nokia Open Source License")
    NOSL = ("NOSL", "Netizen Open Source License")
    NOWEB = ("Noweb", "Noweb License")
    NPL_1_0 = ("NPL-1.0", "Netscape Public License v1.0")
    NPL_1_1 = ("NPL-1.1", "Netscape Public License v1.1")
    NPOSL_3_0 = ("NPOSL-3.0", "Non-Profit Open Software License 3.0")
    NRL = ("NRL", "NRL License")
    NTP = ("NTP", "NTP License")
    NTP_0 = ("NTP-0", "NTP No Attribution")
    O_UDA_1_0 = ("O-UDA-1.0", "Open Use of Data Agreement v1.0")
    OCCT_PL = ("OCCT-PL", "Open CASCADE Technology Public License")
    OCLC_2_0 = ("OCLC-2.0", "OCLC Research Public License 2.0")
    ODBL_1_0 = ("ODbL-1.0", "Open Data Commons Open Database License v1.0")
    ODC_BY_1_0 = ("ODC-By-1.0", "Open Data Commons Attribution License v1.0")
    OFL_1_0 = ("OFL-1.0", "SIL Open Font License 1.0")
    OFL_1_0_NO_RFN = (
        "OFL-1.0-no-RFN",
        "SIL Open Font License 1.0 with no Reserved Font Name",
    )
    OFL_1_0_RFN = (
        "OFL-1.0-RFN",
        "SIL Open Font License 1.0 with Reserved Font Name",
    )
    OFL_1_1 = ("OFL-1.1", "SIL Open Font License 1.1")
    OFL_1_1_NO_RFN = (
        "OFL-1.1-no-RFN",
        "SIL Open Font License 1.1 with no Reserved Font Name",
    )
    OFL_1_1_RFN = (
        "OFL-1.1-RFN",
        "SIL Open Font License 1.1 with Reserved Font Name",
    )
    OGC_1_0 = ("OGC-1.0", "OGC Software License, Version 1.0")
    OGDL_TAIWAN_1_0 = (
        "OGDL-Taiwan-1.0",
        "Taiwan Open Government Data License, version 1.0",
    )
    OGL_CANADA_2_0 = ("OGL-Canada-2.0", "Open Government Licence - Canada")
    OGL_UK_1_0 = ("OGL-UK-1.0", "Open Government Licence v1.0")
    OGL_UK_2_0 = ("OGL-UK-2.0", "Open Government Licence v2.0")
    OGL_UK_3_0 = ("OGL-UK-3.0", "Open Government Licence v3.0")
    OGTSL = ("OGTSL", "Open Group Test Suite License")
    OLDAP_1_1 = ("OLDAP-1.1", "Open LDAP Public License v1.1")
    OLDAP_1_2 = ("OLDAP-1.2", "Open LDAP Public License v1.2")
    OLDAP_1_3 = ("OLDAP-1.3", "Open LDAP Public License v1.3")
    OLDAP_1_4 = ("OLDAP-1.4", "Open LDAP Public License v1.4")
    OLDAP_2_0 = (
        "OLDAP-2.0",
        "Open LDAP Public License v2.0 (or possibly 2.0A and 2.0B)",
    )
    OLDAP_2_0_1 = ("OLDAP-2.0.1", "Open LDAP Public License v2.0.1")
    OLDAP_2_1 = ("OLDAP-2.1", "Open LDAP Public License v2.1")
    OLDAP_2_2 = ("OLDAP-2.2", "Open LDAP Public License v2.2")
    OLDAP_2_2_1 = ("OLDAP-2.2.1", "Open LDAP Public License v2.2.1")
    OLDAP_2_2_2 = ("OLDAP-2.2.2", "Open LDAP Public License 2.2.2")
    OLDAP_2_3 = ("OLDAP-2.3", "Open LDAP Public License v2.3")
    OLDAP_2_4 = ("OLDAP-2.4", "Open LDAP Public License v2.4")
    OLDAP_2_5 = ("OLDAP-2.5", "Open LDAP Public License v2.5")
    OLDAP_2_6 = ("OLDAP-2.6", "Open LDAP Public License v2.6")
    OLDAP_2_7 = ("OLDAP-2.7", "Open LDAP Public License v2.7")
    OLDAP_2_8 = ("OLDAP-2.8", "Open LDAP Public License v2.8")
    OML = ("OML", "Open Market License")
    OPENSSL = ("OpenSSL", "OpenSSL License")
    OPL_1_0 = ("OPL-1.0", "Open Public License v1.0")
    OPUBL_1_0 = ("OPUBL-1.0", "Open Publication License v1.0")
    OSET_PL_2_1 = ("OSET-PL-2.1", "OSET Public License version 2.1")
    OSL_1_0 = ("OSL-1.0", "Open Software License 1.0")
    OSL_1_1 = ("OSL-1.1", "Open Software License 1.1")
    OSL_2_0 = ("OSL-2.0", "Open Software License 2.0")
    OSL_2_1 = ("OSL-2.1", "Open Software License 2.1")
    OSL_3_0 = ("OSL-3.0", "Open Software License 3.0")
    PARITY_6_0_0 = ("Parity-6.0.0", "The Parity Public License 6.0.0")
    PARITY_7_0_0 = ("Parity-7.0.0", "The Parity Public License 7.0.0")
    PDDL_1_0 = (
        "PDDL-1.0",
        "Open Data Commons Public Domain Dedication & License 1.0",
    )
    PHP_3_0 = ("PHP-3.0", "PHP License v3.0")
    PHP_3_01 = ("PHP-3.01", "PHP License v3.01")
    PLEXUS = ("Plexus", "Plexus Classworlds License")
    POLYFORM_NONCOMMERCIAL_1_0_0 = (
        "PolyForm-Noncommercial-1.0.0",
        "PolyForm Noncommercial License 1.0.0",
    )
    POLYFORM_SMALL_BUSINESS_1_0_0 = (
        "PolyForm-Small-Business-1.0.0",
        "PolyForm Small Business License 1.0.0",
    )
    POSTGRESQL = ("PostgreSQL", "PostgreSQL License")
    PSF_2_0 = ("PSF-2.0", "Python Software Foundation License 2.0")
    PSFRAG = ("psfrag", "psfrag License")
    PSUTILS = ("psutils", "psutils License")
    PYTHON_2_0 = ("Python-2.0", "Python License 2.0")
    QHULL = ("Qhull", "Qhull License")
    QPL_1_0 = ("QPL-1.0", "Q Public License 1.0")
    RDISC = ("Rdisc", "Rdisc License")
    RHECOS_1_1 = ("RHeCos-1.1", "Red Hat eCos Public License v1.1")
    RPL_1_1 = ("RPL-1.1", "Reciprocal Public License 1.1")
    RPL_1_5 = ("RPL-1.5", "Reciprocal Public License 1.5")
    RPSL_1_0 = ("RPSL-1.0", "RealNetworks Public Source License v1.0")
    RSA_MD = ("RSA-MD", "RSA Message-Digest License")
    RSCPL = ("RSCPL", "Ricoh Source Code Public License")
    RUBY = ("Ruby", "Ruby License")
    SAX_PD = ("SAX-PD", "Sax Public Domain Notice")
    SAXPATH = ("Saxpath", "Saxpath License")
    SCEA = ("SCEA", "SCEA Shared Source License")
    SENDMAIL = ("Sendmail", "Sendmail License")
    SENDMAIL_8_23 = ("Sendmail-8.23", "Sendmail License 8.23")
    SGI_B_1_0 = ("SGI-B-1.0", "SGI Free Software License B v1.0")
    SGI_B_1_1 = ("SGI-B-1.1", "SGI Free Software License B v1.1")
    SGI_B_2_0 = ("SGI-B-2.0", "SGI Free Software License B v2.0")
    SHL_0_5 = ("SHL-0.5", "Solderpad Hardware License v0.5")
    SHL_0_51 = ("SHL-0.51", "Solderpad Hardware License, Version 0.51")
    SIMPL_2_0 = ("SimPL-2.0", "Simple Public License 2.0")
    SISSL = ("SISSL", "Sun Industry Standards Source License v1.1")
    SISSL_1_2 = ("SISSL-1.2", "Sun Industry Standards Source License v1.2")
    SLEEPYCAT = ("Sleepycat", "Sleepycat License")
    SMLNJ = ("SMLNJ", "Standard ML of New Jersey License")
    SMPPL = ("SMPPL", "Secure Messaging Protocol Public License")
    SNIA = ("SNIA", "SNIA Public License 1.1")
    SPENCER_86 = ("Spencer-86", "Spencer License 86")
    SPENCER_94 = ("Spencer-94", "Spencer License 94")
    SPENCER_99 = ("Spencer-99", "Spencer License 99")
    SPL_1_0 = ("SPL-1.0", "Sun Public License v1.0")
    SSH_OPENSSH = ("SSH-OpenSSH", "SSH OpenSSH license")
    SSH_SHORT = ("SSH-short", "SSH short notice")
    SSPL_1_0 = ("SSPL-1.0", "Server Side Public License, v 1")
    SUGARCRM_1_1_3 = ("SugarCRM-1.1.3", "SugarCRM Public License v1.1.3")
    SWL = ("SWL", "Scheme Widget Library (SWL) Software License Agreement")
    TAPR_OHL_1_0 = ("TAPR-OHL-1.0", "TAPR Open Hardware License v1.0")
    TCL = ("TCL", "TCL/TK License")
    TCP_WRAPPERS = ("TCP-wrappers", "TCP Wrappers License")
    TMATE = ("TMate", "TMate Open Source License")
    TORQUE_1_1 = ("TORQUE-1.1", "TORQUE v2.5+ Software License v1.1")
    TOSL = ("TOSL", "Trusster Open Source License")
    TU_BERLIN_1_0 = (
        "TU-Berlin-1.0",
        "Technische Universitaet Berlin License 1.0",
    )
    TU_BERLIN_2_0 = (
        "TU-Berlin-2.0",
        "Technische Universitaet Berlin License 2.0",
    )
    UCL_1_0 = ("UCL-1.0", "Upstream Compatibility License v1.0")
    UNICODE_DFS_2015 = (
        "Unicode-DFS-2015",
        "Unicode License Agreement - Data Files and Software (2015)",
    )
    UNICODE_DFS_2016 = (
        "Unicode-DFS-2016",
        "Unicode License Agreement - Data Files and Software (2016)",
    )
    UNICODE_TOU = ("Unicode-TOU", "Unicode Terms of Use")
    UNLICENSE = ("Unlicense", "The Unlicense")
    UPL_1_0 = ("UPL-1.0", "Universal Permissive License v1.0")
    VIM = ("Vim", "Vim License")
    VOSTROM = ("VOSTROM", "VOSTROM Public License for Open Source")
    VSL_1_0 = ("VSL-1.0", "Vovida Software License v1.0")
    W3C = ("W3C", "W3C Software Notice and License (2002-12-31)")
    W3C_19980720 = (
        "W3C-19980720",
        "W3C Software Notice and License (1998-07-20)",
    )
    W3C_20150513 = (
        "W3C-20150513",
        "W3C Software Notice and Document License (2015-05-13)",
    )
    WATCOM_1_0 = ("Watcom-1.0", "Sybase Open Watcom Public License 1.0")
    WSUIPA = ("Wsuipa", "Wsuipa License")
    WTFPL = ("WTFPL", "Do What The F*ck You Want To Public License")
    X11 = ("X11", "X11 License")
    XEROX = ("Xerox", "Xerox License")
    XFREE86_1_1 = ("XFree86-1.1", "XFree86 License 1.1")
    XINETD = ("xinetd", "xinetd License")
    XNET = ("Xnet", "X.Net License")
    XPP = ("xpp", "XPP License")
    XSKAT = ("XSkat", "XSkat License")
    YPL_1_0 = ("YPL-1.0", "Yahoo! Public License v1.0")
    YPL_1_1 = ("YPL-1.1", "Yahoo! Public License v1.1")
    ZED = ("Zed", "Zed License")
    ZEND_2_0 = ("Zend-2.0", "Zend License v2.0")
    ZIMBRA_1_3 = ("Zimbra-1.3", "Zimbra Public License v1.3")
    ZIMBRA_1_4 = ("Zimbra-1.4", "Zimbra Public License v1.4")
    ZLIB = ("Zlib", "zlib License")
    ZLIB_ACKNOWLEDGEMENT = (
        "zlib-acknowledgement",
        "zlib/libpng License with Acknowledgement",
    )
    ZPL_1_1 = ("ZPL-1.1", "Zope Public License 1.1")
    ZPL_2_0 = ("ZPL-2.0", "Zope Public License 2.0")
    ZPL_2_1 = ("ZPL-2.1", "Zope Public License 2.1")

    @staticmethod
    def find_enum(name: str):
        """Find enum based on its value
        Args:
            name (str): enum value
        Raises:
            ValueError: Unknown value
        Returns:
            SensorIdHrscDtm: Enum
        """
        result = None
        for pf_name in LicenseType.__members__:
            val = str(LicenseType[pf_name].value)
            if val == name:
                result = LicenseType[pf_name]
                break
        if result is None:
            raise ValueNotFindInEnumError(
                "LicenseType", f"Unknown enum value for {name}"
            )
        return result
