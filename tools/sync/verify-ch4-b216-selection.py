"""Verify Nate's exact-byte Chapter 4 B2-16 selection: four v02 fatal aftermath illustrations.

Art registration only. Four deathScreens records are added and selected; the v01 set stays
preserved as historical review artwork on the immutable review commit. Popup copy, narrative,
death-popup behavior and engine files are unchanged. Every earlier selection (including B2-13 and
B2-14), registry record and approved supplemental reference is unchanged. The only tooling edits are
the two QA count assertions that previously fixed death-art records at exactly nine.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "6a88153f1a41759def5d8e02fd04789db860ec1b"
REVIEW_REF = "art/ch4-b216-fatal-aftermaths-review-20261125"
REVIEW_HEAD = "0fbecaa28d3127faeb553b7847d13121834806a7"
SOURCE_COMMIT = "56fe286e427bba9020d9e38be326ca1d82ce400e"
V01_COMMIT = "1fdf2ce"
PKG = "tools/prologue-art-lab/assets/review/chapter-04-b216-fatal-aftermaths-2026-11-25/"
REPO = "InterstellarHarvest/CYOA-storyboard"
PR32_HEAD = "f320e63934c13e27fd13b9482d0cfba58911362d"

ASSETS = (  # id, key, fatal node, popup id, stem, v02 sha, v01 sha
    ("CH4-NEW-14", "final_occupancy", "fatal_stall_final_occupancy", "ch4_final_occupancy", "14-final-occupancy",
     "e65d321cac76af8e03dd57ba5cbe3aa2d7db454669b0dd36631c61e51e475b7a",
     "a079f2dd91f2cdfaf9f13d7caa754ae909c6f2e4c24587e033c7edf7e8a66dc9"),
    ("CH4-NEW-15", "pressed_and_steamed", "fatal_boiler_pressed_and_steamed", "ch4_pressed_and_steamed", "15-pressed-and-steamed",
     "f0cb0816a5639977634ef21b7d1d57ccfa136c5ef575aa2bb9fd006fc8097e56",
     "36f62d19b207626f8fdf11901e43a292316f3880c4e60cbdd26dedd2c65ca3cd"),
    ("CH4-NEW-16", "folded_for_convenience", "fatal_lot61_folded", "ch4_folded_for_convenience", "16-folded-for-convenience",
     "30490a4259b363879dc126e273dcc07bb979d96ad4f6534dd75cb7e3901ddc07",
     "4f64b7a41755553bd8d03a11568678ace298f81e08ebb7661ad3f105d05906db"),
    ("CH4-NEW-17", "made_to_measure", "fatal_bridal_made_to_measure", "ch4_made_to_measure", "17-made-to-measure",
     "d244595dd545551268143fc6a94e0d9d641d3825324b16db7791b5f0118b21bc",
     "1ed8f23a9dc93b7324a1cf9a4baf4ee06f98082d9b1d405e94897df5e17c919b"),
)
EARLIER = {  # completed B2-13 / B2-14 selections that must survive
    "focus:grand_bellevue/autofit_gown": "0e1a0d3cd73c087416a7e9a2502ae263a597f7da77476e4cd0219dd504d48095",
    "scenes:grand_bellevue/bridal_lavatory": "85fb565d8c2f79525a95ada44a9f9e3c05e2cee374712e520488c88153ee7480",
    "focus:grand_bellevue/three_seashells": "70f35ae3853883b4fe15293ae5e6fd5ede1e721ab54946d2bc7499ce94ac04c6",
}


def path_for(key):
    return f"assets/selected/pending-integration/deathScreens/grand_bellevue/{key}.png"


EXPECTED_CHANGES = {
    "story/artwork.draft.json", "story/artwork-preview.json",
    "tools/storyboard/qa-smoke.mjs", "tools/storyboard/qa-browser.js",
    "tools/sync/verify-ch4-b216-selection.py",
    "docs/148_CH4_B216_APPROVAL_COMPLETION_20261125.md",
    "docs/148_CH4_B216_VERIFICATION_20261125.json",
} | {path_for(a[1]) for a in ASSETS}
REPORT = ROOT / "docs/148_CH4_B216_VERIFICATION_20261125.json"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def at(commit, filename):
    return git("show", f"{commit}:{filename}")


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
    previous = json.loads(at(BASE, "story/artwork-preview.json"))["images"]
    nodes = json.loads((ROOT / "story/chapters/chapter-04.wip.json").read_text())["nodes"]
    base_nodes = json.loads(at(BASE, "story/chapters/chapter-04.wip.json"))["nodes"]
    manifest = json.loads(at(REVIEW_HEAD, PKG + "v02/manifest.json"))
    manifest_sha = {a["native"]["file"]: a["native"]["sha256"] for a in manifest["assets"]}

    check(git("merge-base", "--is-ancestor", SOURCE_COMMIT, REVIEW_HEAD) == b"",
          "v02 source commit is an ancestor of the approved review head")
    for uid, key, node_id, popup_id, stem, sha, v01_sha in ASSETS:
        full = "deathScreens:grand_bellevue/" + key
        src = f"v02/native/CH4-NEW-{stem}-v02.png"
        raw = (ROOT / path_for(key)).read_bytes()
        # Exact bytes, format, manifest and review-commit identity.
        check(digest(raw) == sha, f"Exact approved PNG hash: {uid}")
        with Image.open(BytesIO(raw)) as image:
            check(image.size == (314, 206) and image.mode == "RGB", f"Native 314x206 opaque RGB: {uid}")
        check(manifest_sha.get(src.split("v02/")[1]) == sha, f"Matches v02 review manifest: {uid}")
        for ref in (SOURCE_COMMIT, REVIEW_HEAD):
            check(at(ref, PKG + src) == raw, f"Byte-identical to review source at {ref[:7]}: {uid}")
        # v01 preserved as historical review artwork, never selected.
        v01 = at(REVIEW_HEAD, PKG + f"v01/native/CH4-NEW-{stem}-v01.png")
        check(digest(v01) == v01_sha and at(V01_COMMIT, PKG + f"v01/native/CH4-NEW-{stem}-v01.png") == v01,
              f"Superseded v01 preserved unchanged on review branch: {uid}")
        check(all(v["sha256"] != v01_sha for v in preview.values()), f"Superseded v01 not selected: {uid}")
        # Canonical selection metadata and registry record.
        check(full not in previous and preview[full] == {
            "file": path_for(key), "sha256": sha, "size": [314, 206], "alpha": "opaque",
            "source": {"repo": REPO, "ref": REVIEW_REF, "commit": SOURCE_COMMIT, "path": PKG + src},
        }, f"Approved artwork source metadata: {full}")
        rec = art["deathScreens"]["grand_bellevue/" + key]
        check(rec["kind"] == "death-screen" and rec["status"] == "approved" and rec["dimensions"] == "314x206"
              and rec["assetPath"] is None, f"Death-screen record approved, not integrated: {full}")
        check(sha in rec["notes"] and v01_sha in rec["notes"] and REVIEW_HEAD in rec["notes"],
              f"Approved hash, superseded v01 and review head recorded: {full}")
        # Fatal node and popup copy untouched and pointing at this record.
        n = nodes[node_id]
        check(n == base_nodes[node_id] and n["end"] is True and n["endingArt"] == "grand_bellevue/" + key
              and n["deathPopup"]["artRef"] == "grand_bellevue/" + key and n["deathPopup"]["id"] == popup_id,
              f"Fatal node and popup copy unchanged and mapped: {node_id}")

    check(len(preview) == len(previous) + 4, "Exactly four new canonical image selections")
    check(sorted(k for k in art["deathScreens"] if k.startswith("grand_bellevue/")) ==
          sorted("grand_bellevue/" + a[1] for a in ASSETS), "Chapter 4 death records are exactly the four approved")
    without_new = deepcopy(art)
    for a in ASSETS:
        del without_new["deathScreens"]["grand_bellevue/" + a[1]]
    check(without_new == json.loads(at(BASE, "story/artwork.draft.json")),
          "Only four registry records added; all earlier records, statuses and metadata untouched")
    for key, entry in previous.items():
        check(preview.get(key) == entry and digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"],
              "Earlier selected art and metadata unchanged: " + key)
    for key, sha in EARLIER.items():
        check(preview[key]["sha256"] == sha, "Completed B2-13/B2-14 selection preserved: " + key)
    check(git("ls-tree", "-r", "HEAD", "tools/prologue-art-lab/assets/approved/") ==
          git("ls-tree", "-r", BASE, "tools/prologue-art-lab/assets/approved/"),
          "Approved supplemental/conditional/inspection/retired references unchanged")
    changed = set(git("diff", "--name-only", BASE, "--").decode().split()) | \
        set(git("ls-files", "--others", "--exclude-standard").decode().split())
    check(changed <= EXPECTED_CHANGES, "Only registration files differ from canonical base: " + ", ".join(sorted(changed)))
    for filename in ("story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
                     "story/death-presentations.export.json", "story/game-integration.json",
                     "story/storyboard-manifest.json", "story/items.draft.json", "story/sync-contract.json"):
        check((ROOT / filename).read_bytes() == at(BASE, filename),
              "No narrative, popup, gameplay, item or runtime change: " + filename)
    pr32 = git("ls-remote", "origin", "refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124").split()[0].decode()
    check(pr32 == PR32_HEAD, "Draft PR #32 head unchanged")

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE,
        "approvedReviewHead": REVIEW_HEAD, "sourceCommit": SOURCE_COMMIT,
        "selected": {"deathScreens:grand_bellevue/" + a[1]: {"id": a[0], "file": path_for(a[1]), "sha256": a[5]} for a in ASSETS},
        "supersededV01HistoricalReviewArtwork": {a[0]: a[6] for a in ASSETS},
        "priorSelectedAssetsUnchanged": len(previous),
        "popupCopyOrBehaviorChanged": False, "textBakedIntoArtwork": False,
        "qaToolingChanged": ["tools/storyboard/qa-smoke.mjs", "tools/storyboard/qa-browser.js"],
        "sourceDerived": True, "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; 4 selected death screens; v01 preserved; "
          f"{len(previous)} prior selections unchanged; gameplay unchanged")


if __name__ == "__main__":
    main()
