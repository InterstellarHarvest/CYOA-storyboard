"""Verify B2-12 approved production choices and no gameplay/UI integration.

Two primary PNGs are canonically selected. The other three preferred states
are approved, preserved reference art awaiting later conditional engine wiring.
The two superseded v01 square images remain immutable historical masters.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "13ea9b57ee3b5c670a3ab0ff0f160896559ce2ef"
REVIEW_REF = "art/ch4-b212-bridal-privacy-review-20261125"
REVIEW_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/"
SCENE_KEY = "scenes:grand_bellevue/bridal_dressing_room"
FOCUS_KEY = "focus:grand_bellevue/bridal_privacy_panel"
SCENE_SHA = "f2718d729a28138a88cf51b6ef3c511bdf6d7de0d500654d975b1ab0249bdf49"
LOCKED_SHA = "d4c260fb9b4c55e647cecb58bb6fed196f9f056fd3cf291f1862889ff8035520"
PROVISIONAL_SHA = "b7d8014313519b67d3ebe8c72772ed0d01b4dbbb88748c9e5b0e7f589d669272"
INSPECT_LOCKED_SHA = "b571f3215be27ab7e86bdb67530a86d33e20ed6a0638842f88227fdbc06ec0e3"
INSPECT_PROVISIONAL_SHA = "fa4d465cd6c25b7591ff97caf2713e4b521ef3c2dba6243c5a571685f17660e9"
MASTER_LOCKED_SHA = "072e30b905014a3856e21190551307eab0b0298dd0624e831f5395951d3b7afb"
MASTER_PROVISIONAL_SHA = "e546f7eb4d6de3a319548ee7759ab9ca83e415caa7293fb29322ca6f98ef44b3"
SCENE = "assets/selected/pending-integration/scenes/grand_bellevue/bridal_dressing_room.png"
FOCUS = "assets/selected/pending-integration/focus/grand_bellevue/bridal_privacy_panel.png"
PROVISIONAL = ("tools/prologue-art-lab/assets/approved/conditional-production-references/"
               "chapter-04/b2-12/CH4-NEW-07-focus-provisional-v02.png")
INSPECT_LOCKED = ("tools/prologue-art-lab/assets/approved/inspection-references/"
                  "chapter-04/b2-12/CH4-NEW-07-inspect-locked-v03.png")
INSPECT_PROVISIONAL = ("tools/prologue-art-lab/assets/approved/inspection-references/"
                       "chapter-04/b2-12/CH4-NEW-07-inspect-provisional-v03.png")
MASTER_LOCKED = ("tools/prologue-art-lab/assets/approved/visual-design-masters/"
                 "chapter-04/b2-12/CH4-NEW-07-locked-design-master-565x451-v01.png")
MASTER_PROVISIONAL = ("tools/prologue-art-lab/assets/approved/visual-design-masters/"
                      "chapter-04/b2-12/CH4-NEW-07-provisional-design-master-565x451-v01.png")
REPORT = ROOT / "docs/145_CH4_B212_VERIFICATION_20261126.json"


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

    images = (
        (SCENE, SCENE_SHA, (314, 206), "Scene v01 selected"),
        (FOCUS, LOCKED_SHA, (564, 278), "Focus locked v02 selected"),
        (PROVISIONAL, PROVISIONAL_SHA, (564, 278), "Focus provisional v02 preserved"),
        (INSPECT_LOCKED, INSPECT_LOCKED_SHA, (565, 451), "INSPECT locked v03 preserved"),
        (INSPECT_PROVISIONAL, INSPECT_PROVISIONAL_SHA, (565, 451), "INSPECT provisional v03 preserved"),
        (MASTER_LOCKED, MASTER_LOCKED_SHA, (565, 451), "Superseded locked v01 preserved"),
        (MASTER_PROVISIONAL, MASTER_PROVISIONAL_SHA, (565, 451), "Superseded provisional v01 preserved"),
    )
    for name, expected_sha, dimensions, label in images:
        raw = (ROOT / name).read_bytes()
        check(digest(raw) == expected_sha, "Exact approved/preserved PNG hash: " + label)
        with Image.open(BytesIO(raw)) as image:
            check(image.size == dimensions and image.mode == "RGB", "Native opaque RGB: " + label)

    check(len(preview) == len(previous) + 2 and
          SCENE_KEY not in previous and FOCUS_KEY not in previous,
          "Exactly two new canonical image selections")
    for key, filename, sha, size, commit, source in (
        (SCENE_KEY, SCENE, SCENE_SHA, [314, 206],
         "1261658ed882bff7340405e91f5d44f4e5404012",
         "v01/native/CH4-NEW-01-bridal-dressing-room-v01.png"),
        (FOCUS_KEY, FOCUS, LOCKED_SHA, [564, 278],
         "a944f9aeff110ddc66301840c2d415f1ba9bc357",
         "v02/native/CH4-NEW-07-focus-locked-v02.png"),
    ):
        check(preview[key] == {
            "file": filename, "sha256": sha, "size": size, "alpha": "opaque",
            "source": {"repo": "InterstellarHarvest/CYOA-storyboard", "ref": REVIEW_REF,
                       "commit": commit, "path": REVIEW_ROOT + source},
        }, "Approved primary artwork source metadata: " + key)

    for supplemental in (PROVISIONAL, INSPECT_LOCKED, INSPECT_PROVISIONAL,
                         MASTER_LOCKED, MASTER_PROVISIONAL):
        check(not any(v["file"] == supplemental for v in preview.values()),
              "Reference-only art has no independent selected runtime key: " + supplemental)

    scene = art["scenes"]["grand_bellevue/bridal_dressing_room"]
    focus = art["focus"]["grand_bellevue/bridal_privacy_panel"]
    check(scene["kind"] == "scene" and scene["status"] == "approved" and
          scene["dimensions"] == "314x206" and scene["assetPath"] is None,
          "Selected room is approved, not integrated")
    check(focus["kind"] == "focus" and focus["status"] == "approved" and
          focus["dimensions"] == "564x278" and focus["assetPath"] is None,
          "Selected Focus retains exact old widescreen contract, not integrated")
    check(SCENE_SHA in scene["notes"] and
          all(x in focus["notes"] for x in (LOCKED_SHA, PROVISIONAL_SHA,
              INSPECT_LOCKED_SHA, INSPECT_PROVISIONAL_SHA)),
          "Owner-approved production hashes recorded in art registry")

    focus_node = nodes["hotel_bridal_door_focus"]
    check(focus_node["mode"] == "focus" and
          focus_node["scene"] == "grand_bellevue/bridal_dressing_room" and
          focus_node["focus"] == "grand_bellevue/bridal_privacy_panel",
          "Existing bridal door node uses exact approved Focus key")
    check({x["id"] for x in focus_node["choices"]} == {
        "door_ask_bridal_criteria", "door_request_override", "door_show_ring",
        "door_inspect_gown", "door_leave"}, "All five pre-existing bridal choice IDs intact")
    check(focus_node["effects"]["set"].get("ch4_bridal_door_inspected") is True,
          "Existing bridal panel inspection flag remains authored")

    for key, entry in previous.items():
        check(preview.get(key) == entry and
              digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"],
              "All earlier selected art and metadata unchanged: " + key)

    without_new = deepcopy(art)
    del without_new["scenes"]["grand_bellevue/bridal_dressing_room"]
    del without_new["focus"]["grand_bellevue/bridal_privacy_panel"]
    check(without_new == json.loads(at_base("story/artwork.draft.json")),
          "All previous artwork records, statuses and metadata untouched")
    for filename in (
        "story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
        "story/game-integration.json", "story/storyboard-manifest.json",
        "story/items.draft.json", "story/sync-contract.json",
    ):
        check((ROOT / filename).read_bytes() == at_base(filename),
              "No narrative, gameplay, item, flag or runtime change: " + filename)

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE,
        "selectedPrimaryCount": 2, "approvedPreservedReferenceCount": 3,
        "historicalDesignMastersPreserved": 2,
        "priorSelectedAssetsUnchanged": len(previous),
        "ownerReviewCommits": ["1261658ed882bff7340405e91f5d44f4e5404012",
                               "a944f9aeff110ddc66301840c2d415f1ba9bc357",
                               "43490eeabeb4edb619903ecb4836b0da8d9a4446"],
        "sourceDerived": True, "gameplayIntegrationPerformed": False,
        "squareInspectorEngineFeatureImplemented": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; 2 selected canonical assets; "
          f"3 preserved production references; {len(previous)} prior selections unchanged; "
          "gameplay unchanged")


if __name__ == "__main__":
    main()
