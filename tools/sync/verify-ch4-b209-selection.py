"""Verify Nate's consolidated Chapter 4 B2-09 exact-byte selection.

This is registration-only: no story, runtime, Focus or integration changes.
The published imagegen sources, native layers and exact-4x previews remain
immutable on the separately pinned review branch.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
COMPLETION = ROOT / "docs/142_CH4_B209_APPROVAL_COMPLETION_20261124.json"
OUTPUT = ROOT / "docs/142_CH4_B209_VERIFICATION_20261124.json"


def git_base(commit, filename):
    return subprocess.check_output(["git", "show", f"{commit}:{filename}"], cwd=ROOT)


def digest(data):
    return sha256(data).hexdigest()


def main():
    d = json.loads(COMPLETION.read_text())
    base = d["canonicalBase"]
    art = json.loads((ROOT / "story/artwork.draft.json").read_text())
    preview = json.loads((ROOT / "story/artwork-preview.json").read_text())["images"]
    earlier = json.loads(git_base(base, "story/artwork-preview.json"))["images"]
    nodes = json.loads((ROOT / "story/chapters/chapter-04.wip.json").read_text())["nodes"]
    checks = []

    def check(truth, label):
        if not truth:
            raise AssertionError(label)
        checks.append(label)

    check(len(d["primary"]) == 3 and len(d["supplementalReferences"]) == 4,
          "Exactly three selected primaries and four supplemental references")

    for item in d["primary"]:
        raw = (ROOT / item["canonicalSelectedPath"]).read_bytes()
        check(digest(raw) == item["sha256"], "Pinned selected PNG hash: " + item["id"])
        with Image.open(BytesIO(raw)) as im:
            check(list(im.size) == item["dimensions"] and im.mode == item["mode"],
                  "Native dimensions and mode: " + item["id"])
            if im.mode == "RGBA":
                alpha = set(im.getchannel("A").tobytes())
                check(alpha == {0, 255}, "Binary transparent silhouette: " + item["id"])
        p = preview[item["registryKey"]]
        check(p["file"] == item["canonicalSelectedPath"] and p["sha256"] == item["sha256"],
              "Selected metadata: " + item["id"])
        check(p["source"]["commit"] == d["approvalSourceCommit"] and
              p["source"]["ref"] == d["reviewBranch"] and
              p["source"]["path"] == d["sourceRoot"] + item["sourceFilename"],
              "Immutable review provenance: " + item["id"])
        group, key = item["registryKey"].split(":", 1)
        record = art[group][key.split("#")[0]]
        record = record["portraitBackground"] if "#" in key else record
        check(record["status"] == "approved" and record["assetPath"] is None and
              record["suggestedFilename"] == item["suggestedEngineDestination"],
              "Approved but not integrated: " + item["id"])
        check(all(node in nodes for node in item["storyNodeIds"]),
              "All canonical node IDs exist: " + item["id"])
        if "portraitBackgroundScene" in item:
            check(record["portraitBackgroundScene"] == item["portraitBackgroundScene"],
                  "Default closer room: " + item["id"])

    for item in d["supplementalReferences"]:
        raw = (ROOT / item["preservedPath"]).read_bytes()
        check(digest(raw) == item["sha256"], "Pinned supplemental PNG hash: " + item["id"])
        with Image.open(BytesIO(raw)) as im:
            check(im.size == (564, 278) and im.mode == "RGB",
                  "No-alpha 564x278 conditional frame: " + item["id"])
        check(all(node in nodes for node in item["nodeIds"]),
              "Conditional node IDs exist: " + item["id"])
        check(not any(item["preservedPath"] == p["file"] for p in preview.values()),
              "Supplement never selected as canonical key: " + item["id"])

    shared = (ROOT / d["primary"][2]["canonicalSelectedPath"]).read_bytes()
    removed = (ROOT / d["supplementalReferences"][1]["preservedPath"]).read_bytes()
    check(shared == removed, "Wheel-removed state is byte-identical to approved neutral background")
    check(all(d["supplementalPolicy"][k] is None for k in
              ["canonicalKey", "runtimeBinding", "newFocusId", "newFlags", "newNodes"]),
          "Conditional states introduce no keys, runtime binding, Focus ID, flag or node")

    check(len(preview) == len(earlier) + 3, "Exactly three added selections")
    for key, p in earlier.items():
        check(preview.get(key) == p and digest((ROOT / p["file"]).read_bytes()) == p["sha256"],
              "Prior selection metadata and bytes unchanged: " + key)

    reduced = deepcopy(art)
    del reduced["portraits"]["hotel_commodore_bixby:delighted"]
    del reduced["portraits"]["hotel_wedding_organizer:urgent"]
    del reduced["scenes"]["grand_bellevue/ballroom"]["portraitBackground"]
    check(reduced == json.loads(git_base(base, "story/artwork.draft.json")),
          "All previous artwork records and approved selections unchanged")

    for path in ["story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
                 "story/game-integration.json", "story/storyboard-manifest.json",
                 "story/items.draft.json", "story/sync-contract.json"]:
        check((ROOT / path).read_bytes() == git_base(base, path),
              "No story, game, flag or layout modifications: " + path)

    for item in d["primary"]:
        check(not any(item["id"] == key for key in earlier),
              "New unit does not overwrite an old selected key: " + item["id"])

    report = {
        "passed": True,
        "checksPassed": len(checks),
        "selectedPrimaryCount": 3,
        "preservedSupplementalCount": 4,
        "preservedPreviousSelections": len(earlier),
        "sourceCommit": d["approvalSourceCommit"],
        "canonicalBase": base,
        "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; 3 primaries selected, 4 supplemental refs preserved, "
          f"{len(earlier)} earlier selections unchanged; no integration")


if __name__ == "__main__":
    main()
