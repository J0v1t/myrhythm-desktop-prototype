from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_supplied_dashboard_banners_are_packaged():
    for name in ("banner1.webp", "banner2.webp", "banner3.webp"):
        assert (PROJECT_ROOT / "media" / name).is_file()
