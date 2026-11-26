"""Verify Nate's exact-byte Chapter 4 B2-17 selection: dispute ticket and wedding ring, slot + inspection.

Art registration only. The four existing item art records (items:lot_53_dispute_ticket#slot/#inspect,
items:wedding_ring_lot31#slot/#inspect) are raised to approved and selected; assetPath stays null. Item
rules, narrative, flags and engine-facing files are unchanged. Every earlier selection (including the
B2-13, B2-14 and B2-16 registrations), registry record and approved supplemental reference is unchanged.
The only tooling edit is the qa-smoke assertion that previously required this item art to be not-started.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "301ab75a62500a83b20dfee292b1a7460e01e405"
REVIEW_REF = "art/ch4-b217-ticket-ring-review-20261125"
REVIEW_HEAD = "302c9c5304d555b50aa252200c45c30726123a46"
GALLERY_COMMIT = "c29eb9f73a659f9ad7ca40f5819521aebf86a5ae"
SOURCE_COMMIT = "e350a13794113ad7269074698fd021d10de957d3"
PKG_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b217-ticket-ring-2026-11-25/"
PKG = PKG_ROOT + "v01/"
REPO = "InterstellarHarvest/CYOA-storyboard"
PR32_HEAD = "f320e63934c13e27fd13b9482d0cfba58911362d"

ASSETS = (  # id, item, view, native stem, sha, size, alpha
    ("CH4-NEW-10", "lot_53_dispute_ticket", "slot", "CH4-NEW-10-dispute-ticket-slot-v01",
     "21543ddb40788ee4f994601b37397caa3173a082b851e569cccf79484c9741cd", (96, 96), "transparent"),
    ("CH4-NEW-11", "lot_53_dispute_ticket", "inspect", "CH4-NEW-11-dispute-ticket-inspection-v01",
     "493004874154a0037559aa3eb4393eb60d73fac4977577699245eb9154393eed", (565, 451), "opaque"),
    ("CH4-NEW-12", "wedding_ring_lot31", "slot", "CH4-NEW-12-wedding-ring-slot-v01",
     "e3a1d25cf2343302a6df8c660341879fa1e6a90f43629ac0706e50d2ba3e1ebe", (96, 96), "transparent"),
    ("CH4-NEW-13", "wedding_ring_lot31", "inspect", "CH4-NEW-13-wedding-ring-inspection-v01",
     "298d8e45f371f7cc3f95e14928cf153fbe1af50f1bfac941a569c4f844a067e8", (565, 451), "opaque"),
)
EARLIER = {  # completed B2-13 / B2-14 / B2-16 selections that must survive
    "focus:grand_bellevue/autofit_gown": "0e1a0d3cd73c087416a7e9a2502ae263a597f7da77476e4cd0219dd504d48095",
    "scenes:grand_bellevue/bridal_lavatory": "85fb565d8c2f79525a95ada44a9f9e3c05e2cee374712e520488c88153ee7480",
    "focus:grand_bellevue/three_seashells": "70f35ae3853883b4fe15293ae5e6fd5ede1e721ab54946d2bc7499ce94ac04c6",
    "deathScreens:grand_bellevue/final_occupancy": "e65d321cac76af8e03dd57ba5cbe3aa2d7db454669b0dd36631c61e51e475b7a",
    "deathScreens:grand_bellevue/pressed_and_steamed": "f0cb0816a5639977634ef21b7d1d57ccfa136c5ef575aa2bb9fd006fc8097e56",
    "deathScreens:grand_bellevue/folded_for_convenience": "30490a4259b363879dc126e273dcc07bb979d96ad4f6534dd75cb7e3901ddc07",
    "deathScreens:grand_bellevue/made_to_measure": "d244595dd545551268143fc6a94e0d9d641d3825324b16db7791b5f0118b21bc",
}
TICKET_WORDS = ("LOT 53", "LACK OF PRIVACY — CUSTOMER PRESENT", "HOLD FOR INSPECTION")
INSCRIPTION = "AS IS, WHERE IS."


def path_for(item, view):
    return f"assets/selected/pending-integration/items/{item}/{view}.png"


EXPECTED_CHANGES = {
    "story/artwork.draft.json", "story/artwork-preview.json", "tools/storyboard/qa-smoke.mjs",
    "tools/sync/verify-ch4-b217-selection.py",
    "docs/149_CH4_B217_APPROVAL_COMPLETION_20261126.md",
    "docs/149_CH4_B217_VERIFICATION_20261126.json",
} | {path_for(a[1], a[2]) for a in ASSETS}
REPORT = ROOT / "docs/149_CH4_B217_VERIFICATION_20261126.json"


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
    base_art = json.loads(at(BASE, "story/artwork.draft.json"))
    preview = json.loads((ROOT / "story/artwork-preview.json").read_text())["images"]
    previous = json.loads(at(BASE, "story/artwork-preview.json"))["images"]
    items = json.loads((ROOT / "story/items.draft.json").read_text())
    manifest = json.loads(at(REVIEW_HEAD, PKG + "manifest.json"))
    by_id = {a["id"]: a for a in manifest["assets"]}

    for older, newer in ((SOURCE_COMMIT, GALLERY_COMMIT), (GALLERY_COMMIT, REVIEW_HEAD)):
        check(git("merge-base", "--is-ancestor", older, newer) == b"",
              f"Review history {older[:7]} is an ancestor of {newer[:7]}")
    for uid, item, view, stem, sha, size, alpha in ASSETS:
        key = f"items:{item}#{view}"
        src = PKG + f"native/{stem}.png"
        raw = (ROOT / path_for(item, view)).read_bytes()
        # Exact bytes, format, manifest and review-commit identity.
        check(digest(raw) == sha, f"Exact approved PNG hash: {uid}")
        with Image.open(BytesIO(raw)) as image:
            if alpha == "transparent":
                histogram = image.getchannel("A").histogram()
                values = {level for level, count in enumerate(histogram) if count}
                check(image.size == size and image.mode == "RGBA" and values == {0, 255},
                      f"Native {size[0]}x{size[1]} RGBA with binary 0/255 alpha and transparent margin: {uid}")
            else:
                check(image.size == size and image.mode == "RGB", f"Native {size[0]}x{size[1]} opaque RGB: {uid}")
        m = by_id[uid]
        check(m["native"]["file"] == f"native/{stem}.png" and m["native"]["sha256"] == sha
              and m["itemId"] == item and m["view"] == view and list(m["native"]["dimensions"]) == list(size),
              f"Matches v01 review manifest (item, view, size, hash): {uid}")
        for ref in (SOURCE_COMMIT, GALLERY_COMMIT, REVIEW_HEAD):
            check(at(ref, src) == raw, f"Byte-identical to review source at {ref[:7]}: {uid}")
        # Canonical selection metadata and the existing registry record.
        check(key not in previous and preview[key] == {
            "file": path_for(item, view), "sha256": sha, "size": list(size), "alpha": alpha,
            "source": {"repo": REPO, "ref": REVIEW_REF, "commit": SOURCE_COMMIT, "path": src},
        }, f"Approved artwork source metadata: {key}")
        rec, old = art["items"][item][view], base_art["items"][item][view]
        check(old["status"] == "not-started" and rec["status"] == "approved" and rec["assetPath"] is None
              and rec["kind"] == ("item-" + view) and rec["dimensions"] == f"{size[0]}x{size[1]}",
              f"Existing record raised not-started -> approved, not integrated: {key}")
        check(sha in rec["notes"] and SOURCE_COMMIT in rec["notes"] and REVIEW_HEAD in rec["notes"]
              and rec["notes"].endswith(old["notes"]),
              f"Approval provenance recorded; earlier draft note kept verbatim: {key}")
        check({k: v for k, v in rec.items() if k not in ("status", "notes")} ==
              {k: v for k, v in old.items() if k not in ("status", "notes")},
              f"Record title, kind, size, prompt and paths unchanged: {key}")

    check(len(preview) == len(previous) + 4, "Exactly four new canonical image selections")
    restored = deepcopy(art)
    for _, item, view, *_ in ASSETS:
        for field in ("status", "notes"):
            restored["items"][item][view][field] = base_art["items"][item][view][field]
    check(restored == base_art, "Only the four records' status and notes changed; every other record untouched")
    for key, entry in previous.items():
        check(preview.get(key) == entry and digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"],
              "Earlier selected art and metadata unchanged: " + key)
    for key, sha in EARLIER.items():
        check(preview[key]["sha256"] == sha, "Completed B2-13/B2-14/B2-16 selection preserved: " + key)
    check(git("ls-tree", "-r", "HEAD", "tools/prologue-art-lab/assets/approved/") ==
          git("ls-tree", "-r", BASE, "tools/prologue-art-lab/assets/approved/"),
          "Approved supplemental/conditional/inspection/retired references unchanged")
    check(git("ls-tree", "-r", "--name-only", "HEAD", PKG_ROOT) == b"",
          "Review package (originals, prompts, layers, source) stays on the review branch, not copied to main")
    review_files = git("ls-tree", "-r", "--name-only", REVIEW_HEAD, PKG_ROOT).decode().split("\n")
    check(sum(f.startswith(PKG + "originals/") for f in review_files) == 4
          and sum(f.startswith(PKG + "prompts/") for f in review_files) == 4
          and PKG + "source/build.py" in review_files, "Originals, prompts and source preserved at the review head")
    # Item rules and canonical wording the art depicts are unchanged.
    check(all(w in items["lot_53_dispute_ticket"]["description"] for w in TICKET_WORDS),
          "Ticket lettering is canonical item wording")
    check(INSCRIPTION in json.dumps(items["wedding_ring_lot31"], ensure_ascii=False),
          "Ring inscription AS IS, WHERE IS. is canonical item text")
    changed = set(git("diff", "--name-only", BASE, "--").decode().split()) | \
        set(git("ls-files", "--others", "--exclude-standard").decode().split())
    check(changed <= EXPECTED_CHANGES, "Only registration files differ from canonical base: " + ", ".join(sorted(changed)))
    for filename in ("story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
                     "story/death-presentations.export.json", "story/game-integration.json",
                     "story/storyboard-manifest.json", "story/items.draft.json", "story/sync-contract.json",
                     "tools/storyboard/qa-browser.js"):
        check((ROOT / filename).read_bytes() == at(BASE, filename),
              "No narrative, item-rule, popup, gameplay or runtime change: " + filename)
    pr32 = git("ls-remote", "origin", "refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124").split()[0].decode()
    check(pr32 == PR32_HEAD, "Draft PR #32 head unchanged")

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE,
        "approvedReviewHead": REVIEW_HEAD, "galleryCommit": GALLERY_COMMIT, "sourceCommit": SOURCE_COMMIT,
        "selected": {f"items:{a[1]}#{a[2]}": {"id": a[0], "file": path_for(a[1], a[2]), "sha256": a[4],
                                               "size": list(a[5]), "alpha": a[6]} for a in ASSETS},
        "priorSelectedAssetsUnchanged": len(previous),
        "assetPathAssigned": False, "itemRulesChanged": False, "gameplayIntegrationPerformed": False,
        "qaToolingChanged": ["tools/storyboard/qa-smoke.mjs"], "sourceDerived": True,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(checks)} checks passed; 4 selected item views; "
          f"{len(previous)} prior selections unchanged; item rules and gameplay unchanged")


if __name__ == "__main__":
    main()
