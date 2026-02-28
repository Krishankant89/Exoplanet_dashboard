import requests
import pandas as pd
import io

NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

COLUMNS = [
    "pl_name",       # Planet name
    "hostname",      # Host star name
    "discoverymethod",
    "disc_year",
    "pl_rade",       # Planet radius (Earth radii)
    "pl_masse",      # Planet mass (Earth masses)
    "pl_orbsmax",    # Orbital semi-major axis (AU)
    "st_teff",       # Star effective temperature (K)
    "st_rad",        # Star radius
    "sy_dist",       # Distance from Earth (parsecs)
]

def fetch_exoplanets() -> pd.DataFrame:
    """
    Fetch confirmed exoplanet data from the NASA Exoplanet Archive TAP service.
    Returns a cleaned pandas DataFrame.
    """
    query = f"""
        SELECT {', '.join(COLUMNS)}
        FROM ps
        WHERE default_flag = 1
        AND disc_year IS NOT NULL
        AND pl_rade IS NOT NULL
    """

    params = {
        "QUERY": query,
        "FORMAT": "csv",
        "REQUEST": "doQuery",
        "LANG": "ADQL"
    }

    try:
        response = requests.get(NASA_TAP_URL, params=params, timeout=30)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        print(f"[nasa_api] Error fetching data: {e}")
        return pd.DataFrame()

    # Clean up
    df["disc_year"] = pd.to_numeric(df["disc_year"], errors="coerce")
    df["pl_rade"] = pd.to_numeric(df["pl_rade"], errors="coerce")
    df["pl_masse"] = pd.to_numeric(df["pl_masse"], errors="coerce")
    df["pl_orbsmax"] = pd.to_numeric(df["pl_orbsmax"], errors="coerce")
    df["st_teff"] = pd.to_numeric(df["st_teff"], errors="coerce")

    df = df.dropna(subset=["pl_name", "disc_year", "pl_rade"])
    df["disc_year"] = df["disc_year"].astype(int)

    return df
