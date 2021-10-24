# -*- coding: utf-8 -*-
import logging

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
    assert catalog.id == "first_cat"
    assert catalog.path == ""
    assert catalog.description == "My first catalog"


def test_create_simple_collection():
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
    assert collection.id == "first_coll"
    assert collection.path == "/first_cat/first_coll"
    assert collection.description == "My first collection"
    assert collection.license == LicenseType.ADSL
    assert collection.extent == extent
    assert collection.links[0].href == "../../first_cat.json"
    assert collection.links[1].href == "first_coll.json"
    assert collection.links[2].href == "../first_cat.json"
    assert catalog.links[0].href == "./first_cat.json"
    assert catalog.links[1].href == "first_cat.json"
    assert catalog.links[2].href == "./first_cat/first_coll/first_coll.json"


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
    assert collection.id == "first_coll"
    assert collection.path == "/first_cat/first_coll"
    assert collection.description == "My first collection"
    assert collection.license == LicenseType.ADSL
    assert collection.extent == extent
    assert collection.title == "First collection"
    assert collection.links[0].href == "../../first_cat.json"
    assert collection.links[0].rel == RelationTypes.ROOT
    assert collection.links[0].type == MediaType.STAC_CATALOG
    assert collection.links[1].href == "first_coll.json"
    assert collection.links[1].rel == RelationTypes.SELF
    assert collection.links[1].type == MediaType.STAC_COLLECTION
    assert collection.links[2].href == "../first_cat.json"
    assert collection.links[2].rel == RelationTypes.PARENT
    assert collection.links[2].type == MediaType.STAC_CATALOG

    assert catalog.links[0].href == "./first_cat.json"
    assert catalog.links[0].rel == RelationTypes.ROOT
    assert catalog.links[0].type == MediaType.STAC_CATALOG
    assert catalog.links[0].title is None

    assert catalog.links[1].href == "first_cat.json"
    assert catalog.links[1].rel == RelationTypes.SELF
    assert catalog.links[1].type == MediaType.STAC_CATALOG
    assert catalog.links[1].title == "first_cat"

    assert catalog.links[2].href == "./first_cat/first_coll/first_coll.json"
    assert catalog.links[2].rel == RelationTypes.CHILD
    assert catalog.links[2].type == MediaType.STAC_COLLECTION
    assert catalog.links[2].title == "First collection"

    assert catalog.links[3].href == "./first_cat/1st_item.json"
    assert catalog.links[3].rel == RelationTypes.ITEM
    assert catalog.links[3].type == MediaType.STAC_ITEM
    assert catalog.links[3].title == "1st_item"


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
