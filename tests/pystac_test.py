# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import pytest

import pystac
from pystac.constants import LicenseType
from pystac.constants import MediaType
from pystac.constants import RelationTypes
from pystac.pystac import AssetObject
from pystac.pystac import ExtentObject
from pystac.pystac import Properties
from pystac.pystac import SpatialExtentObject
from pystac.pystac import TemporalExtentObject


def test_name():
    name = pystac.__name_soft__
    assert name == "pystac"


def test_logger():
    loggers = [logging.getLogger()]
    loggers = loggers + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]
    assert loggers[0].name == "root"


def test_create_simple_catalog():
    stac = pystac.PySTAC("conf/pystac.cong", "/tmp")
    catalog = stac.create_catalog("first_cat", "/", "My first catalog")
    json = catalog.to_json()
    assert catalog.path == ""
    assert json["id"] == "first_cat"
    assert json["description"] == "My first catalog"


def test_create_simple_collection():
    stac = pystac.PySTAC("conf/pystac.cong", "/tmp")
    catalog = stac.create_catalog("first_cat", "/", "My first catalog")
    spatial_extent = SpatialExtentObject([[-180, -90, 180, 90]])
    temporal_extent = TemporalExtentObject([[datetime.now(), None]])
    extent = ExtentObject(spatial_extent, temporal_extent)
    collection = stac.create_collection(
        "first_coll",
        "/first_cat/first_coll",
        "My first collection",
        LicenseType.ADSL,
        extent,
        parent=catalog,
    )
    json = collection.to_json()
    assert collection.path == "/first_cat/first_coll"
    assert json["id"] == "first_coll"
    assert json["description"] == "My first collection"
    assert json["license"] == LicenseType.ADSL.value
    assert json["extent"] == extent.to_dict()
    assert json["links"][0]["href"] == "../../first_cat.json"
    assert json["links"][1]["href"] == "first_coll.json"
    assert json["links"][2]["href"] == "../first_cat.json"


def test_create_error_simple_collection():
    stac = pystac.PySTAC("conf/pystac.cong", "/tmp")
    stac.create_catalog("first_cat", "/", "My first catalog")
    spatial_extent = SpatialExtentObject([[-180, -90, 180, 90]])
    temporal_extent = TemporalExtentObject([[None]])
    extent = ExtentObject(spatial_extent, temporal_extent)

    with pytest.raises(ValueError):
        stac.create_collection(
            "first_coll",
            "/first_cat/first_coll",
            "My first collection",
            LicenseType.ADSL,
            extent,
        )


def test_create_simple_item_coll():
    stac = pystac.PySTAC("conf/pystac.cong", "/tmp")
    catalog = stac.create_catalog("first_cat", "/", "My first catalog")
    spatial_extent = SpatialExtentObject([[-180, -90, 180, 90]])
    temporal_extent = TemporalExtentObject([[datetime.now(), None]])
    extent = ExtentObject(spatial_extent, temporal_extent)
    collection = stac.create_collection(
        "first_coll",
        "/first_cat/first_coll",
        "My first collection",
        LicenseType.ADSL,
        extent,
        parent=catalog,
    )
    collection.title = "First collection"
    stac.create_item(
        "/first_cat/first_coll",
        "1st_item_coll",
        None,
        Properties(None),
        {"test": AssetObject("http://toto.test")},
        parent=collection,
    )

    stac.create_item(
        "/first_cat",
        "1st_item",
        None,
        Properties(None),
        {"test": AssetObject("http://toto.test")},
        parent=catalog,
    )
    json = collection.to_json()
    assert collection.path == "/first_cat/first_coll"
    assert json["id"] == "first_coll"
    assert json["description"] == "My first collection"
    assert json["license"] == LicenseType.ADSL.value
    assert json["extent"] == extent.to_dict()
    assert json["title"] == "First collection"
    assert json["links"][0]["href"] == "../../first_cat.json"
    assert json["links"][0]["rel"] == RelationTypes.ROOT.value
    assert json["links"][0]["type"] == MediaType.STAC_CATALOG.value
    assert json["links"][1]["href"] == "first_coll.json"
    assert json["links"][1]["rel"] == RelationTypes.SELF.value
    assert json["links"][1]["type"] == MediaType.STAC_COLLECTION.value
    assert json["links"][2]["href"] == "../first_cat.json"
    assert json["links"][2]["rel"] == RelationTypes.PARENT.value
    assert json["links"][2]["type"] == MediaType.STAC_CATALOG.value

    json = catalog.to_json()
    assert json["links"][0]["href"] == "./first_cat.json"
    assert json["links"][0]["rel"] == RelationTypes.ROOT.value
    assert json["links"][0]["type"] == MediaType.STAC_CATALOG.value

    assert json["links"][1]["href"] == "first_cat.json"
    assert json["links"][1]["rel"] == RelationTypes.SELF.value
    assert json["links"][1]["type"] == MediaType.STAC_CATALOG.value
    assert json["links"][1]["title"] == "first_cat"

    assert json["links"][2]["href"] == "./first_cat/first_coll/first_coll.json"
    assert json["links"][2]["rel"] == RelationTypes.CHILD.value
    assert json["links"][2]["type"] == MediaType.STAC_COLLECTION.value
    assert json["links"][2]["title"] == "First collection"

    assert json["links"][3]["href"] == "./first_cat/1st_item.json"
    assert json["links"][3]["rel"] == RelationTypes.ITEM.value
    assert json["links"][3]["type"] == MediaType.STAC_ITEM.value
    assert json["links"][3]["title"] == "1st_item"


def test_extension_collection():
    stac = pystac.PySTAC("conf/pystac.cong", "/tmp")
    catalog = stac.create_catalog("first_cat", "/", "My first catalog")
    spatial_extent = SpatialExtentObject([[-180, -90, 180, 90]])
    temporal_extent = TemporalExtentObject([[datetime.now(), None]])
    extent = ExtentObject(spatial_extent, temporal_extent)
    collection = stac.create_collection(
        "first_coll",
        "/first_cat/first_coll",
        "My first collection",
        LicenseType.ADSL,
        extent,
        parent=catalog,
    )
    collection.title = "First collection"

    collection.add_stac_extension(
        "https://raw.githubusercontent.com/thareUSGS/ssys/main/json-schema/schema.json",
        {"ssys:targets": ["Mars"]},
    )

    json = collection.to_json()
    assert (
        "https://raw.githubusercontent.com/thareUSGS/ssys/main/json-schema/schema.json"
        in json["stac_extensions"]
    )
    assert "ssys:targets" in json and json["ssys:targets"][0] == "Mars"


def test_create_simple_item_coll_tree():
    import sys

    stac = pystac.PySTAC("conf/pystac.cong", "/tmp")
    catalog = stac.create_catalog("first_cat", "/", "My first catalog")
    spatial_extent = SpatialExtentObject([[-180, -90, 180, 90]])
    temporal_extent = TemporalExtentObject([[None]])
    extent = ExtentObject(spatial_extent, temporal_extent)
    collection = stac.create_collection(
        "first_coll",
        "/first_cat/first_coll",
        "My first collection",
        LicenseType.ADSL,
        extent,
        parent=catalog,
    )
    collection.title = "First collection"
    stac.create_item(
        "/first_cat/first_coll",
        "1st_item_coll",
        None,
        Properties(None),
        {"test": AssetObject("http://toto.test")},
        parent=collection,
    )

    stac.create_item(
        "/first_cat",
        "1st_item",
        None,
        Properties(None),
        {"test": AssetObject("http://toto.test")},
        parent=catalog,
    )

    stac.tree()
