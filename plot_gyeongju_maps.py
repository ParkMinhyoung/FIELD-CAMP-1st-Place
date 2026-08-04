#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
경주 AI 데이터센터 입지 — 4패널 통합 지도

필요 입력: CSV 3개
  1) terrain_grid_100m.csv  — 격자 데이터
       i, j, lon, lat, elevation_m, slope_deg,
       inside_gyeongju      (경주 경계 내부=1)
       population           (인구)
       in_heritage_buffer   (유물 완충구역=1)   → 유물 구역 표시에 사용
  2) substation_locations.csv    — 변전소·풍력단지 (name, type, lon, lat)
       type: 'substation' → 파란 네모 / 'wind_farm' → 빨간 별
  3) gyeongju_boundary.csv       — 경주시 경계 윤곽 (ring, lon, lat)

패널:
  좌상: 경주시 지도   우상: 표고
  좌하: 평균 경사도   우하: 인구 분포

출력: gyeongju_combined_100m.png
"""
import math, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib.patches import Rectangle
import matplotlib.font_manager as fm

# ---------------------------------------------------------------- 경로
FP  = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
OUT = "/mnt/user-data/outputs"

kf = fm.FontProperties(fname=FP); fm.fontManager.addfont(FP)
plt.rcParams["font.family"] = kf.get_name()
plt.rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------------- 1) 격자 CSV
g  = pd.read_csv(f"{OUT}/terrain_grid_100m.csv")
NC = int(math.isqrt(len(g)))
print(f"격자 {NC}x{NC} = {len(g):,}셀")

def grid2d(col):
    return g.pivot(index='i', columns='j', values=col).values

ELEV  = grid2d('elevation_m')
SLOPE = grid2d('slope_deg')
POP   = grid2d('population')
INS   = grid2d('inside_gyeongju').astype(bool)     # 경계 내부
HERI  = grid2d('in_heritage_buffer').astype(bool)  # 유물 완충구역

lon_min, lon_max = g['lon'].min(), g['lon'].max()
lat_min, lat_max = g['lat'].min(), g['lat'].max()
ext = [lon_min, lon_max, lat_min, lat_max]

# 격자 좌표축 (contour용)
LONS = np.sort(g['lon'].unique())
LATS = np.sort(g['lat'].unique())

# ---------------------------------------------------------------- 2) 변전소·풍력 CSV
loc = pd.read_csv(f"{OUT}/substation_locations.csv")
SUBS = loc[loc['type'] == 'substation']
WFS  = loc[loc['type'] == 'wind_farm']
SUB_COLOR = "#1565c0"   # 변전소: 파랑
WF_COLOR  = "#c0392b"   # 풍력단지: 빨강
print(f"변전소 {len(SUBS)}개소, 풍력단지 {len(WFS)}개소")

# ---------------------------------------------------------------- 3) 경계 CSV
bnd = pd.read_csv(f"{OUT}/gyeongju_boundary.csv")
BND_RINGS = [grp[['lon','lat']].values for _, grp in bnd.groupby('ring')]
print(f"경계 링 {len(BND_RINGS)}개, 총 {len(bnd):,}점")

ASP = 1 / math.cos(math.radians(35.80))
def mask(a):
    return np.where(INS, a, np.nan)

def boundary(ax, lw=1.2, color="#33691e", fill=None):
    """경계 CSV의 실제 좌표로 경주시 윤곽선 그리기"""
    for r in BND_RINGS:
        if fill is not None:
            ax.fill(r[:,0], r[:,1], color=fill, zorder=1)
        ax.plot(r[:,0], r[:,1], color=color, lw=lw, zorder=6)

def heritage(ax, alpha=0.55):
    """유물 완충구역을 보라색으로 표시"""
    h = np.where(HERI, 1.0, np.nan)
    ax.imshow(h, origin="lower", extent=ext, aspect="auto",
              cmap=plt.matplotlib.colors.ListedColormap(["purple"]),
              alpha=alpha, zorder=5, interpolation="nearest")

def markers(ax, s_sub=100, s_wf=13, label=False):
    """변전소=파란 네모, 풍력단지=빨간 별 (CSV의 type 컬럼으로 구분)"""
    for _, row in SUBS.iterrows():
        ax.scatter(row['lon'], row['lat'], s=s_sub, marker="s", color=SUB_COLOR,
                   edgecolor="w", lw=.7, zorder=8)
        if label:
            ax.annotate(row['name'], (row['lon'], row['lat']), fontproperties=kf,
                        fontsize=7.5, xytext=(6, 3), textcoords="offset points", zorder=9)
    for _, row in WFS.iterrows():
        ax.plot(row['lon'], row['lat'], "*", color=WF_COLOR, ms=s_wf,
                markeredgecolor="w", mew=.6, zorder=8)
        if label:
            ax.annotate(row['name'], (row['lon'], row['lat']), fontproperties=kf,
                        fontsize=7.5, xytext=(6, -9), textcoords="offset points", zorder=9)

def axes_labels(ax):
    ax.set_xlabel("lon (경도)", fontproperties=kf, fontsize=9)
    ax.set_ylabel("lat (위도)", fontproperties=kf, fontsize=9)

# ---------------------------------------------------------------- 도화
fig = plt.figure(figsize=(15, 14))
gs  = fig.add_gridspec(2, 2, hspace=0.20, wspace=0.18)
axTL = fig.add_subplot(gs[0, 0]); axTR = fig.add_subplot(gs[0, 1])
axBL = fig.add_subplot(gs[1, 0]); axBR = fig.add_subplot(gs[1, 1])

# ============ 좌상: 경주시 지도 (정사각형) ============
TL_LON = (128.95, 129.57)   # 동해 축소 → 정사각형 비율
TL_LAT = (35.60, 36.10)

axTL.axvspan(129.53, TL_LON[1], color="#dbeef7", alpha=.6, zorder=0)   # 동해
boundary(axTL, lw=1.5, fill="#eef4e1")   # 경주 전체 윤곽 + 채우기
heritage(axTL, alpha=0.7)
axTL.add_patch(Rectangle((lon_min, lat_min), lon_max-lon_min, lat_max-lat_min,
                         fill=False, edgecolor="crimson", lw=1.8, zorder=4))
axTL.annotate("검토영역 30×30km", ((lon_min+lon_max)/2, lat_max), fontproperties=kf,
              fontsize=8.5, color="crimson", ha="center",
              xytext=(0, 4), textcoords="offset points", zorder=7)
markers(axTL, s_sub=110, s_wf=14, label=True)
for lo, la, t in [(129.55, 35.80, "동해"), (129.10, 36.05, "포항 방면"),
                  (129.24, 35.62, "울산 방면")]:
    axTL.annotate(t, (lo, la), fontproperties=kf, fontsize=7.5,
                  color="#546e7a", ha="center", zorder=5)
axTL.set_xlim(*TL_LON); axTL.set_ylim(*TL_LAT)
axTL.set_aspect(1/math.cos(math.radians(35.85)))
axTL.grid(alpha=.25)
axes_labels(axTL)
axTL.set_title("경주시 지도", fontproperties=kf, fontsize=12)

def zoom(ax):
    ax.set_xlim(lon_min, lon_max); ax.set_ylim(lat_min, lat_max)
    ax.set_aspect(ASP)
    axes_labels(ax)

# ============ 우상: 표고 ============
ls = LightSource(azdeg=315, altdeg=45)
shaded = ls.shade(np.nan_to_num(ELEV, nan=np.nanmin(ELEV)), cmap=plt.cm.terrain,
                  blend_mode="soft", vert_exag=2, dx=100, dy=100)
alpha = np.where(INS, 1.0, 0.12)[..., None]
rgba  = np.concatenate([shaded[..., :3], alpha], axis=2)
axTR.imshow(rgba, origin="lower", extent=ext, aspect="auto", zorder=1)
boundary(axTR); markers(axTR); zoom(axTR)
axTR.set_title("표고", fontproperties=kf, fontsize=12)
sm = plt.cm.ScalarMappable(cmap=plt.cm.terrain,
        norm=plt.Normalize(np.nanmin(mask(ELEV)), np.nanmax(mask(ELEV)))); sm.set_array([])
fig.colorbar(sm, ax=axTR, fraction=.046, pad=.02).set_label("표고(m)", fontproperties=kf, fontsize=9)

# ============ 좌하: 평균 경사도 ============
crgb = {"preferred": (46,125,50), "conditional": (192,202,51),
        "risky": (239,108,0),     "excluded": (183,28,28)}
def cls_arr(s):
    """경사도 → 4등급 RGBA (<5 / 5-10 / 10-15 / >15도)"""
    out = np.empty(s.shape + (4,))
    for idx in np.ndindex(s.shape):
        v = s[idx]
        k = ("preferred"   if v < 5   else
             "conditional" if v <= 10 else
             "risky"       if v <= 15 else "excluded")
        a = 1.0 if INS[idx] else 0.12
        out[idx] = [*(np.array(crgb[k])/255), a]
    return out
axBL.imshow(cls_arr(SLOPE), origin="lower", extent=ext, aspect="auto", zorder=1)
boundary(axBL); markers(axBL); zoom(axBL)
axBL.set_title("평균 경사도", fontproperties=kf, fontsize=12)

# ============ 우하: 인구 분포 ============
im = axBR.imshow(mask(POP), origin="lower", extent=ext, cmap="YlOrRd",
                 aspect="auto", interpolation="nearest", zorder=1)
boundary(axBR); markers(axBR); zoom(axBR)
axBR.set_title("인구 분포", fontproperties=kf, fontsize=12)
fig.colorbar(im, ax=axBR, fraction=.046, pad=.02).set_label("인구수(명)", fontproperties=kf, fontsize=9)

plt.savefig(f"{OUT}/gyeongju_combined_100m.png", dpi=125, bbox_inches="tight")
print("저장: gyeongju_combined_100m.png")
