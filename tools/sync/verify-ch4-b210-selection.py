"""Verify Nate's exact-byte Chapter 4 B2-10 upper-salvage selection.

Art selection only: existing scene selections, narrative and engine integration
must remain unchanged relative to the pinned canonical base.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "b8a8e4ea3c6d13141b2e33d281ba864c3b2aec42"
KEY = "scenes:grand_bellevue/upper_salvage"
FILE = "assets/selected/pending-integration/scenes/grand_bellevue/upper_salvage.png"
SHA = "1030e04f9b32d2c0fc4394e9f00a4a70ba162db1c9eeed4f2772068cf9ce3207"
SOURCE_COMMIT = "7963f507568a6e6f9a50ffda3755103f9674bdd3"
SOURCE_REF = "art/ch4-b210-upper-salvage-review-20261124"
SOURCE_PATH = (
    "tools/prologue-art-lab/assets/review/"
    "chapter-04-b210-upper-salvage-2026-11-24/v03/native/"
    "CH4-NEW-03-upper-salvage-v03.png"
)
REPORT = ROOT / "docs/143_CH4_B210_VERIFICATION_20261124.json"


def at_base(filename):
    return subprocess.check_output(["git", "show", f"{BASE}:{filename}"], cwd=ROOT)


def main():
    checks = []

    def check(value, description):
        if not value:
            raise AssertionError(description)
        checks.append(description)

    art = json.loads((ROOT / "story/artwork.draft.json").read_text())
    preview = json.loads((ROOT / "story/artwork-preview.json").read_text())["images"]
    previous = json.loads(at_base("story/artwork-preview.json"))["images"]
    raw = (ROOT / FILE).read_bytes()

    check(sha256(raw).hexdigest() == SHA, "Approved v03 pixels retain SHA-256")
    with Image.open(BytesIO(raw)) as image:
        check(image.size == (314, 206) and image.mode == "RGB",
              "Approved native scene is opaque RGB, 314x206")
    check(len(preview) == len(previous) + 1 and KEY not in previous,
          "Exactly one new selected key")
    check(preview[KEY] == {
        "file": FILE,
        "sha256": SHA,
        "size": [314, 206],
        "alpha": "opaque",
        "source": {
            "repo": "InterstellarHarvest/CYOA-storyboard",
            "ref": SOURCE_REF,
            "commit": SOURCE_COMMIT,
            "path": SOURCE_PATH,
        },
    }, "Selected metadata and immutable source provenance")

    record = art["scenes"]["grand_bellevue/upper_salvage"]
    check(record["status"] == "approved" and record["assetPath"] is None,
          "Owner-approved, not engine-integrated")
    check(record["dimensions"] == "314x206" and record["kind"] == "scene",
          "Scene registry contract")
    check(SHA in record["notes"] and SOURCE_COMMIT in record["notes"],
          "Provenance pinned in artwork notes")
    nodes = json.loads((ROOT / "story/chapters/chapter-04.wip.json").read_text())["nodes"]
    for node in ("hotel_upper_salvage_arrival", "hotel_upper_salvage_clerk_directions",
                 "hotel_freight_wc_misunderstanding"):
        check(node in nodes, "Canonical Chapter 4 node exists: " + node)

    for key, entry in previous.items():
        check(preview.get(key) == entry and
              sha256((ROOT / entry["file"]).read_bytes()).hexdigest() == entry["sha256"],
              "Prior selected metadata and PNG bytes preserved: " + key)

    without_new = deepcopy(art)
    del without_new["scenes"]["grand_bellevue/upper_salvage"]
    check(without_new == json.loads(at_base("story/artwork.draft.json")),
          "All existing artwork records unchanged")
    for filename in (
        "story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
        "story/game-integration.json", "story/storyboard-manifest.json",
        "story/items.draft.json", "story/sync-contract.json",
    ):
        check((ROOT / filename).read_bytes() == at_base(filename),
              "No narrative, flag, layout or runtime changes: " + filename)

    report = {
        "passed": True,
        "checksPassed": len(checks),
        "selectedPrimaryCount": 1,
        "preservedPreviousSelections": len(previous),
        "approvedFile": FILE,
        "sha256": SHA,
        "sourceCommit": SOURCE_COMMIT,
        "canonicalBase": BASE,
        "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; exact B2-10 v03 selected; "
          f"{len(previous)} previous selections unchanged; no integration")


if __name__ == "__main__":
    main()
