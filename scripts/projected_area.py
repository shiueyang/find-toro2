"""
由 CAD 網格（STL）計算衛星在隨機翻滾下的平均投影面積，以及各主軸方向的投影面積。

方法：在網格表面均勻取樣大量點（含內部零件也無妨，它們的投影落在外殼投影之內），
對每個觀察方向把點投影到垂直平面、以 pitch 大小的像素格計數，被佔用像素數 × pitch² = 該方向的投影面積
（即輪廓面積，正確處理帆板與本體的互相遮蔽）。方向在球面上均勻取樣（Fibonacci 球）。
同時給出「總表面積 / 4」與「凸包表面積 / 4」兩個近似值供比較。

用法：python scripts/projected_area.py <mesh.stl> [--mass 11] [--pitch-mm 1.5] [--n-dirs 600] [--n-points 6000000] [--out results/toro2_projected_area.md]
"""
import argparse, os, sys, json, time
import numpy as np
import trimesh

sys.stdout.reconfigure(encoding="utf-8")


def fibonacci_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], axis=1)


def basis_for(d):
    d = d / np.linalg.norm(d)
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(d, a); u /= np.linalg.norm(u)
    v = np.cross(d, u)
    return u, v


def projected_area(points, d, pitch):
    u, v = basis_for(d)
    x = points @ u; y = points @ v
    ix = np.floor((x - x.min()) / pitch).astype(np.int64)
    iy = np.floor((y - y.min()) / pitch).astype(np.int64)
    key = ix * (iy.max() + 1) + iy
    return np.unique(key).size * pitch * pitch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mesh")
    ap.add_argument("--mass", type=float, default=11.0)
    ap.add_argument("--pitch-mm", type=float, default=1.5)
    ap.add_argument("--n-dirs", type=int, default=600)
    ap.add_argument("--n-points", type=int, default=6_000_000)
    ap.add_argument("--label", default="TORO-2")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    t0 = time.time()
    m = trimesh.load(a.mesh, force="mesh")
    print(f"mesh: {len(m.faces)} triangles, bbox {m.bounds[0]} .. {m.bounds[1]} (units assumed mm)")
    ext = m.extents
    area_total = m.area / 1e6
    hull = m.convex_hull
    area_hull = hull.area / 1e6
    print(f"total surface area (all triangles, incl. internal) {area_total:.4f} m²;  convex hull area {area_hull:.4f} m²")

    pts, _ = trimesh.sample.sample_surface(m, a.n_points)
    pts = np.asarray(pts, dtype=np.float64)
    print(f"sampled {len(pts)} surface points in {time.time()-t0:.0f}s; pitch {a.pitch_mm} mm")

    # 主軸方向
    axes = {"+X": [1, 0, 0], "+Y": [0, 1, 0], "+Z": [0, 0, 1]}
    ax_area = {k: projected_area(pts, np.array(v, float), a.pitch_mm) / 1e6 for k, v in axes.items()}
    # 隨機方向（球面均勻）
    dirs = fibonacci_sphere(a.n_dirs)
    areas = np.array([projected_area(pts, d, a.pitch_mm) for d in dirs]) / 1e6
    mean_A = float(areas.mean())
    res = dict(label=a.label, mesh=os.path.basename(a.mesh), triangles=int(len(m.faces)), extents_mm=[float(x) for x in ext],
               mass_kg=a.mass, pitch_mm=a.pitch_mm, n_dirs=a.n_dirs, n_points=a.n_points,
               area_total_m2=area_total, area_hull_m2=area_hull,
               proj_mean_m2=mean_A, proj_min_m2=float(areas.min()), proj_max_m2=float(areas.max()),
               proj_axes_m2=ax_area,
               am_tumbling=mean_A / a.mass, am_hull_over4=area_hull / 4 / a.mass, am_total_over4=area_total / 4 / a.mass,
               am_min=float(areas.min()) / a.mass, am_max=float(areas.max()) / a.mass)
    print(json.dumps(res, indent=1, ensure_ascii=False))

    md = [f"# {a.label} 投影面積（來源網格 {res['mesh']}，{res['triangles']} 個三角形）\n",
          f"外形包絡 {ext[0]:.0f} × {ext[1]:.0f} × {ext[2]:.0f} mm；質量 {a.mass:.1f} kg；像素 {a.pitch_mm} mm；{a.n_dirs} 個均勻方向、{a.n_points:,} 個表面取樣點。\n",
          "| 量 | 面積 m² | A/m m²/kg |", "|--|--|--|",
          f"| **隨機翻滾平均投影面積（輪廓法）** | **{mean_A:.4f}** | **{mean_A / a.mass:.4f}** |",
          f"| 最小投影面積 | {areas.min():.4f} | {areas.min() / a.mass:.4f} |",
          f"| 最大投影面積 | {areas.max():.4f} | {areas.max() / a.mass:.4f} |"]
    md += [f"| 沿 {k} 軸投影 | {v:.4f} | {v / a.mass:.4f} |" for k, v in ax_area.items()]
    md += [f"| 凸包表面積 / 4 | {area_hull / 4:.4f} | {area_hull / 4 / a.mass:.4f} |",
           f"| 全部三角形面積 / 4（含內部零件，僅供參考） | {area_total / 4:.4f} | {area_total / 4 / a.mass:.4f} |", ""]
    if a.out:
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        open(a.out, "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
        json.dump(res, open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("->", a.out)
    print("\n".join(md))


if __name__ == "__main__":
    main()
