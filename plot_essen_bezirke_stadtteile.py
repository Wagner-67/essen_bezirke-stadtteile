import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import math

BASE_DIR = Path(__file__).resolve().parent

BEZIRKE_FILE = BASE_DIR / "stadtbezirke.geojson"
STADTTEILE_FILE = BASE_DIR / "stadtteile.geojson"

# Lade GeoJSONs
bezirk_gdf = gpd.read_file(BEZIRKE_FILE)
stadtteil_gdf = gpd.read_file(STADTTEILE_FILE)

# Zeige Spalten an, um richtige Namens-Spalten zu erkennen
print("Bezirke Spalten:", bezirk_gdf.columns)
print("Stadtteile Spalten:", stadtteil_gdf.columns)

# Heuristik für Namensfelder
bezirk_name_field = next((c for c in bezirk_gdf.columns if "name" in c.lower() or "bezirk" in c.lower()), None)
stadtteil_name_field = next((c for c in stadtteil_gdf.columns if "name" in c.lower() or "stadtteil" in c.lower()), None)

# Falls keine gefunden -> Index verwenden
if bezirk_name_field is None:
    bezirk_gdf["__bname"] = bezirk_gdf.index.astype(str)
    bezirk_name_field = "__bname"
if stadtteil_name_field is None:
    stadtteil_gdf["__tname"] = stadtteil_gdf.index.astype(str)
    stadtteil_name_field = "__tname"

# Optional CRS in Web-Mercator für bessere Darstellung
TARGET_CRS = "EPSG:3857"
bezirk_gdf = bezirk_gdf.to_crs(TARGET_CRS)
stadtteil_gdf = stadtteil_gdf.to_crs(TARGET_CRS)

fig, ax = plt.subplots(figsize=(12, 12))

# Stadtteile (gefüllt, leicht transparent)
stadtteil_gdf.plot(ax=ax, edgecolor="#444444", linewidth=0.4, alpha=0.6, column=None)

# Bezirke (nur Grenzen)
bezirk_gdf.boundary.plot(ax=ax, edgecolor="black", linewidth=1.4)

# Namen der Bezirke
for _, row in bezirk_gdf.iterrows():
    p = row.geometry.representative_point()
    ax.text(p.x, p.y, str(row[bezirk_name_field]), fontsize=10, fontweight="bold",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6, ec="none"))

# Namen der Stadtteile
for _, row in stadtteil_gdf.iterrows():
    p = row.geometry.representative_point()
    ax.text(p.x, p.y, str(row[stadtteil_name_field]), fontsize=6, ha="center", va="center", alpha=0.9)

# Titel und Achsen ausblenden
ax.set_title("Essen — Stadtbezirke (schwarz) und Stadtteile (gefüllt) mit Namen", fontsize=14)
ax.set_axis_off()

# Optional: einfache Skalierungsleiste
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm

x0, x1 = ax.get_xlim()
view_width = x1 - x0
approx = view_width / 8.0 if view_width > 0 else 1000
exp = math.floor(math.log10(approx)) if approx > 0 else 3
base = 10 ** exp
nice = round(approx / base) * base
if nice == 0:
    nice = 1000
label = f"{nice/1000:.0f} km" if nice >= 1000 else f"{nice:.0f} m"
fontprops = fm.FontProperties(size=9)
scalebar = AnchoredSizeBar(ax.transData, size=nice, label=label, loc='lower left',
                           pad=0.4, borderpad=0.5, sep=6, prop=fontprops, frameon=True)
ax.add_artist(scalebar)

plt.tight_layout()
out_png = BASE_DIR / "essen_bezirke_stadtteile.png"
out_pdf = BASE_DIR / "essen_bezirke_stadtteile.pdf"
plt.savefig(out_png, dpi=300, bbox_inches="tight")
plt.savefig(out_pdf, dpi=300, bbox_inches="tight")
print(f"Saved: {out_png} and {out_pdf}")

plt.show()
