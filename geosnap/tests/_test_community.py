from geosnap import Community, DataStore

import pytest
import os

datasets=DataStore()

try:
    LTDB = os.environ["LTDB_SAMPLE"]
    NCDB = os.environ["NCDB"]
except:
    LTDB=None
    NCDB=None

def test_Community_from_cbsa():

    la = Community.from_census(msa_fips="31080")
    assert la.gdf.shape == (7683, 195)


def test_Community_from_stcofips():

    mn = Community.from_census(state_fips="27", county_fips=["26001", "26002"])
    assert mn.gdf.shape == (3881, 195)


@pytest.mark.skipif(not NCDB, reason="unable to locate NCDB data")
def test_Community_from_indices():

    chi = Community.from_ncdb(fips=["17031", "17019"])
    assert chi.gdf.shape == (6797, 78)


def test_Community_from_boundary():
    msas = datasets.msas()

    reno = msas[msas["geoid"] == "39900"]
    rn = Community.from_census(boundary=reno)
    assert rn.gdf.shape == (234, 195)


def test_Community_from_census():
    assert Community.from_census(state_fips="24").gdf.shape == (3759, 195)


def test_Community_from_gdfs():

    t90 = datasets.tracts_1990()
    t90 = t90[t90.geoid.str.startswith("11")]
    t00 = datasets.tracts_2000()
    t00 = t00[t00.geoid.str.startswith("11")]

    assert Community.from_geodataframes([t90, t00]).gdf.shape == (380, 192)

def test_Community_from_gdfs_crs():

    t90 = datasets.tracts_1990()
    t00 = datasets.tracts_2000()
    t90 = t90.to_crs(4236)
    t00 = t00.to_crs(3857)
    try:
        Community.from_geodataframes([t90, t00])
    except AssertionError:
        print("From_gdfs constructor successfully detects inconsistent crs.")
        pass

def test_Community_from_lodes():
    de = Community.from_lodes(state_fips="10", years=[2008, 2015])
    assert de.gdf.shape == (41598, 58)
