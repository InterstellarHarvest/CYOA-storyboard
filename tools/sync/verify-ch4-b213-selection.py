"""Verify Nate's exact-byte Chapter 4 B2-13 selection (AutoFit gown v01 + preserved manual-slack reference).

Art registration only. One primary Focus image is canonically selected; the closer manual-slack
reference is APPROVED / PRESERVED with no key or binding. Every earlier selection (including the
completed B2-14 registration), artwork record, narrative and engine-facing file must be unchanged.
The only documentation edit outside docs/147 is a purely additive, dated correction in docs/146.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "8fc6d196846a25f3a303a1a7ed53d120e07f13df"
REVIEW_REF = "art/ch4-b213-autofit-gown-review-20261125"
REVIEW_HEAD = "7a74fc38c1b0533e01425738433ff7be0c917b4e"
SOURCE_COMMIT = "144a2a6b53408c495a8ee9a51a79f1be719fe462"
REVIEW_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b213-autofit-gown-2026-11-25/v01/native/"
REPO = "InterstellarHarvest/CYOA-storyboard"
PR32_HEAD = "f320e63934c13e27fd13b9482d0cfba58911362d"

KEY = "focus:grand_bellevue/autofit_gown"
PRIMARY = "assets/selected/pending-integration/focus/grand_bellevue/autofit_gown.png"
PRIMARY_SHA = "0e1a0d3cd73c087416a7e9a2502ae263a597f7da77476e4cd0219dd504d48095"
PRIMARY_SRC = "CH4-NEW-08-autofit-gown-v01.png"
SLACK = ("tools/prologue-art-lab/assets/approved/conditional-production-references/"
         "chapter-04/b2-13/CH4-NEW-08-manual-slack-revealed-v01.png")
SLACK_SHA = "592bc3e6a237745d9a066fe5d7424d1cb5f520caffbc0af2491eaf76d83bb98d"
SLACK_SRC = "CH4-NEW-08-manual-slack-revealed-v01.png"
B214 = {"scenes:grand_bellevue/bridal_lavatory": "85fb565d8c2f79525a95ada44a9f9e3c05e2cee374712e520488c88153ee7480",
        "focus:grand_bellevue/three_seashells": "70f35ae3853883b4fe15293ae5e6fd5ede1e721ab54946d2bc7499ce94ac04c6"}
DOC146 = "docs/146_CH4_B214_APPROVAL_COMPLETION_20261125.md"
EXPECTED_CHANGES = {
    "story/artwork.draft.json", "story/artwork-preview.json", PRIMARY, SLACK, DOC146,
    "tools/sync/verify-ch4-b213-selection.py",
    "docs/147_CH4_B213_APPROVAL_COMPLETION_20261125.md",
    "docs/147_CH4_B213_VERIFICATION_20261125.json",
}
REPORT = ROOT / "docs/147_CH4_B213_VERIFICATION_20261125.json"


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

    # 1. Exact bytes and identity with the immutable review commits.
    for name, sha, src, label in ((PRIMARY, PRIMARY_SHA, PRIMARY_SRC, "AutoFit gown v01 selected"),
                                  (SLACK, SLACK_SHA, SLACK_SRC, "Manual-slack v01 preserved")):
        raw = (ROOT / name).read_bytes()
        check(digest(raw) == sha, "Exact approved PNG hash: " + label)
        with Image.open(BytesIO(raw)) as image:
            check(image.size == (564, 278) and image.mode == "RGB", "Native 564x278 opaque RGB: " + label)
        for ref in (SOURCE_COMMIT, REVIEW_HEAD):
            check(at(ref, REVIEW_ROOT + src) == raw, f"Byte-identical to review source at {ref[:7]}: " + label)
    check(git("merge-base", "--is-ancestor", SOURCE_COMMIT, REVIEW_HEAD) == b"",
          "Source commit is an ancestor of the approved review head")

    # 2. Exactly one new selection with exact provenance; supplemental has no key.
    check(len(preview) == len(previous) + 1 and KEY not in previous, "Exactly one new canonical image selection")
    check(preview[KEY] == {
        "file": PRIMARY, "sha256": PRIMARY_SHA, "size": [564, 278], "alpha": "opaque",
        "source": {"repo": REPO, "ref": REVIEW_REF, "commit": SOURCE_COMMIT, "path": REVIEW_ROOT + PRIMARY_SRC},
    }, "Approved artwork source metadata: " + KEY)
    check(all(v["sha256"] != SLACK_SHA and v["file"] != SLACK for v in preview.values()),
          "Manual-slack reference has no selected runtime key")
    rec = art["focus"]["grand_bellevue/autofit_gown"]
    check(rec["kind"] == "focus" and rec["status"] == "approved" and rec["dimensions"] == "564x278" and
          rec["assetPath"] is None, "AutoFit gown record approved on the Focus A contract, not integrated")
    check(PRIMARY_SHA in rec["notes"] and SLACK_SHA in rec["notes"] and REVIEW_HEAD in rec["notes"],
          "Approved and preserved hashes plus review head recorded in registry notes")
    without_new = deepcopy(art)
    del without_new["focus"]["grand_bellevue/autofit_gown"]
    check(without_new == json.loads(at(BASE, "story/artwork.draft.json")),
          "Only one registry record added; no manual-slack Focus key; all earlier records untouched")

    # 3. Existing nodes already carry the approved key; motor node stays narrative.
    focus_node, motor = nodes["hotel_bridal_gown_focus"], nodes["hotel_bridal_gown_motor"]
    check(focus_node["mode"] == "focus" and focus_node["focus"] == "grand_bellevue/autofit_gown" and
          focus_node["scene"] == "grand_bellevue/bridal_dressing_room",
          "hotel_bridal_gown_focus uses the selected Focus key")
    check([c["id"] for c in focus_node["choices"]] ==
          ["gown_examine_motor", "gown_try_on", "gown_hold_camera", "gown_leave_alone"],
          "All four gown Focus choices intact")
    check(motor["mode"] == "narrative" and "focus" not in motor and
          motor["effects"]["set"] == {"ch4_autofit_release_located": True} and
          [c["id"] for c in motor["choices"]] == ["motor_try_gown", "motor_hold_camera", "motor_return_door", "motor_leave"],
          "hotel_bridal_gown_motor stays narrative mode with its authored flag and choices")

    # 4. Everything earlier unchanged, including the completed B2-14 registration.
    for key, entry in previous.items():
        check(preview.get(key) == entry and digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"],
              "Earlier selected art and metadata unchanged: " + key)
    for key, sha in B214.items():
        check(preview[key]["sha256"] == sha, "Completed B2-14 selection preserved: " + key)
    before = set(git("ls-tree", "-r", BASE, "tools/prologue-art-lab/assets/approved/").decode().splitlines())
    after = set(git("ls-tree", "-r", "HEAD", "tools/prologue-art-lab/assets/approved/").decode().splitlines()) \
        if git("rev-parse", "HEAD").decode().strip() != BASE else before
    worktree_new = {SLACK}
    check(before <= after and all(line.split("\t")[1] in worktree_new for line in after - before),
          "Existing approved/conditional/inspection/retired references unchanged (B2-13 reference only added)")
    changed = set(git("diff", "--name-only", BASE, "--").decode().split()) | \
        set(git("ls-files", "--others", "--exclude-standard").decode().split())
    check(changed <= EXPECTED_CHANGES, "Only registration files differ from canonical base: " + ", ".join(sorted(changed)))
    old146, new146 = at(BASE, DOC146).decode(), (ROOT / DOC146).read_text()
    check(all(line in new146.splitlines() for line in old146.splitlines()) and "Correction (2026-11-25" in new146,
          "docs/146 keeps every original line and gains a dated correction only")
    for filename in ("story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
                     "story/game-integration.json", "story/storyboard-manifest.json",
                     "story/items.draft.json", "story/sync-contract.json"):
        check((ROOT / filename).read_bytes() == at(BASE, filename),
              "No narrative, gameplay, item, flag or runtime change: " + filename)
    pr32 = git("ls-remote", "origin", "refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124").split()[0].decode()
    check(pr32 == PR32_HEAD, "Draft PR #32 head unchanged")

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE,
        "approvedReviewHead": REVIEW_HEAD, "sourceCommit": SOURCE_COMMIT,
        "ownerApproval": "Nate, Chapter 4 Artwork PMO conversation, 2026-11-25, before B2-14 production",
        "selected": {KEY: {"file": PRIMARY, "sha256": PRIMARY_SHA}},
        "approvedPreservedReference": {"file": SLACK, "sha256": SLACK_SHA, "node": "hotel_bridal_gown_motor",
                                       "focusKey": None, "runtimeBinding": None},
        "priorSelectedAssetsUnchanged": len(previous),
        "docs146Correction": "additive, dated",
        "sourceDerived": True, "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; 1 selected + 1 preserved; {len(previous)} prior selections unchanged; "
          "gameplay unchanged")


if __name__ == "__main__":
    main()
