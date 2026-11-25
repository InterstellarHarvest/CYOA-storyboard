"""Verify Nate's exact-byte B2-11 public corridor and flood approval.

Only the dry master becomes a selected artwork key. The approved flood frame is
preserved separately as a conditional production reference, without runtime
binding, new Focus IDs or other narrative/game changes.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "5a4290d672e1904b4b5ad361562f05168c328a50"
KEY = "scenes:grand_bellevue/public_corridor"
PRIMARY = "assets/selected/pending-integration/scenes/grand_bellevue/public_corridor.png"
PRIMARY_SHA = "86da5123204f65c43ed23f418fe0edcf987dbdb3d000821367c36c8f30c390ec"
FLOOD = (
    "tools/prologue-art-lab/assets/approved/conditional-production-references/"
    "chapter-04/b2-11/CH4-NEW-04-public-corridor-flood-v04.png"
)
FLOOD_SHA = "f802ff0c9aa345147f6039779df8b49403cc96add6be89b13f2ef9396727212f"
REVIEW_COMMIT = "6475c943f7383ea796e118c6d84b8760d0ccc12e"
REVIEW_REF = "art/ch4-b211-public-corridor-review-20261124"
REVIEW_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/"
REPORT = ROOT / "docs/144_CH4_B211_VERIFICATION_20261125.json"


def at_base(filename):
    return subprocess.check_output(["git", "show", f"{BASE}:{filename}"], cwd=ROOT)


def digest(data):
    return sha256(data).hexdigest()


def main():
    checks = []

    def check(truth, label):
        if not truth:
            raise AssertionError(label)
        checks.append(label)

    art = json.loads((ROOT / "story/artwork.draft.json").read_text())
    preview = json.loads((ROOT / "story/artwork-preview.json").read_text())["images"]
    previous = json.loads(at_base("story/artwork-preview.json"))["images"]
    nodes = json.loads((ROOT / "story/chapters/chapter-04.wip.json").read_text())["nodes"]

    for path, expected, description in (
        (PRIMARY, PRIMARY_SHA, "Dry v02 primary"),
        (FLOOD, FLOOD_SHA, "Flood v04 supplemental"),
    ):
        raw = (ROOT / path).read_bytes()
        check(digest(raw) == expected, "Pinned approved PNG hash: " + description)
        with Image.open(BytesIO(raw)) as image:
            check(image.size == (314, 206) and image.mode == "RGB",
                  "Native opaque 314x206 scene format: " + description)

    check(len(preview) == len(previous) + 1 and KEY not in previous,
          "Exactly one new primary selection")
    check(preview[KEY] == {
        "file": PRIMARY,
        "sha256": PRIMARY_SHA,
        "size": [314, 206],
        "alpha": "opaque",
        "source": {
            "repo": "InterstellarHarvest/CYOA-storyboard",
            "ref": REVIEW_REF,
            "commit": REVIEW_COMMIT,
            "path": REVIEW_ROOT + "v02/native/CH4-NEW-04-public-corridor-v02.png",
        },
    }, "Primary source provenance and selected metadata")
    check(not any(value["file"] == FLOOD for value in preview.values()),
          "Flood frame has no primary selection key")

    record = art["scenes"]["grand_bellevue/public_corridor"]
    check(record["status"] == "approved" and record["assetPath"] is None and
          record["kind"] == "scene" and record["dimensions"] == "314x206",
          "Approved scene, not runtime-integrated")
    check(PRIMARY_SHA in record["notes"] and FLOOD_SHA in record["notes"] and
          REVIEW_COMMIT in record["notes"], "Both approved hashes and source in registry")
    for node in ("hotel_stall_public_corridor_walk", "hotel_flooded_public_corridor"):
        check(node in nodes and nodes[node]["scene"] == "grand_bellevue/public_corridor",
              "Approved nodes reuse one canonical scene: " + node)

    for key, entry in previous.items():
        check(preview.get(key) == entry and
              digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"],
              "Prior selected artwork and metadata unchanged: " + key)

    without_new = deepcopy(art)
    del without_new["scenes"]["grand_bellevue/public_corridor"]
    check(without_new == json.loads(at_base("story/artwork.draft.json")),
          "All earlier artwork records unchanged")
    for filename in (
        "story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
        "story/game-integration.json", "story/storyboard-manifest.json",
        "story/items.draft.json", "story/sync-contract.json",
    ):
        check((ROOT / filename).read_bytes() == at_base(filename),
              "No narrative, flag, layout or engine change: " + filename)

    report = {
        "passed": True,
        "checksPassed": len(checks),
        "selectedPrimaryCount": 1,
        "approvedPreservedConditionalCount": 1,
        "preservedPreviousSelections": len(previous),
        "primarySha256": PRIMARY_SHA,
        "floodSha256": FLOOD_SHA,
        "sourceCommit": REVIEW_COMMIT,
        "canonicalBase": BASE,
        "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; one selected dry primary, one preserved flood "
          f"reference; {len(previous)} previous selections unchanged; no integration")


if __name__ == "__main__":
    main()
