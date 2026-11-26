"""Verify Nate's exact-byte Chapter 4 B2-14 selection (bridal lavatory v02 + three seashells v01).

Art selection only. Two primary images are canonically selected; the superseded lavatory v01 stays
preserved as historical review artwork on the immutable review commit; the separate Claude
alternatives from the B2-14 agent collision are NOT approved and must not appear anywhere.
Every earlier selection, artwork record, narrative and engine-facing file must be unchanged.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "436e83f43c01b0a64620056d44aabf14c61fb444"
REVIEW_REF = "art/ch4-b214-native-review-20261125"
REVIEW_HEAD = "fbad7b3620f0043752868215bea046bccc259e05"
REVIEW_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b214-bridal-lavatory-2026-11-25/"
REPO = "InterstellarHarvest/CYOA-storyboard"
PR32_HEAD = "f320e63934c13e27fd13b9482d0cfba58911362d"

SCENE_KEY = "scenes:grand_bellevue/bridal_lavatory"
FOCUS_KEY = "focus:grand_bellevue/three_seashells"
SCENE = "assets/selected/pending-integration/scenes/grand_bellevue/bridal_lavatory.png"
FOCUS = "assets/selected/pending-integration/focus/grand_bellevue/three_seashells.png"
SCENE_SHA = "85fb565d8c2f79525a95ada44a9f9e3c05e2cee374712e520488c88153ee7480"
FOCUS_SHA = "70f35ae3853883b4fe15293ae5e6fd5ede1e721ab54946d2bc7499ce94ac04c6"
SCENE_SRC = ("100debcb0940f330b7237da93c05e99c6bf7d89e", "v02/native/CH4-NEW-02-bridal-lavatory-v02.png")
FOCUS_SRC = ("04a920c08f06d1bf62d63eaaf5f52cddd99c38b9", "v01/native/CH4-NEW-09-three-seashells-v01.png")
SUPERSEDED_V01 = ("v01/native/CH4-NEW-02-bridal-lavatory-v01.png",
                  "522cc6a4c2e2d45f1aae7b3897a05380b86a2c70fccdba767576aa1520cabc04")
# Second-agent alternatives from the B2-14 collision: never approved, never registered.
UNAPPROVED_ALTERNATIVES = ("ebc3287c7e3090b5f28da765452140150aa38967526794657f4fe355fff169bb",
                           "8a4f53436611f4bbae17298220efc3bb1a454a330cb748e9d99b3a06c68181d6")
EXPECTED_CHANGES = {
    "story/artwork.draft.json", "story/artwork-preview.json", SCENE, FOCUS,
    "tools/sync/verify-ch4-b214-selection.py",
    "docs/146_CH4_B214_APPROVAL_COMPLETION_20261125.md",
    "docs/146_CH4_B214_VERIFICATION_20261125.json",
}
SEASHELL_SCENE_NODES = ("hotel_seashell_room", "hotel_seashell_inspect", "hotel_seashell_first_attempt",
                        "hotel_seashell_instructions", "hotel_seashell_complaint",
                        "hotel_seashell_second_attempt", "hotel_seashell_assessment_appeal")
REPORT = ROOT / "docs/146_CH4_B214_VERIFICATION_20261125.json"


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

    # 1. Exact selected bytes, format, and identity with the immutable review sources.
    for name, sha, size, (commit, src), label in (
        (SCENE, SCENE_SHA, (314, 206), SCENE_SRC, "Lavatory v02 selected"),
        (FOCUS, FOCUS_SHA, (564, 278), FOCUS_SRC, "Three seashells v01 selected"),
    ):
        raw = (ROOT / name).read_bytes()
        check(digest(raw) == sha, "Exact approved PNG hash: " + label)
        with Image.open(BytesIO(raw)) as image:
            check(image.size == size and image.mode == "RGB", "Native opaque RGB: " + label)
        for ref in (commit, REVIEW_HEAD):
            check(at(ref, REVIEW_ROOT + src) == raw,
                  f"Byte-identical to review source at {ref[:7]}: " + label)

    # 2. Superseded lavatory v01 preserved as historical review artwork, never selected.
    v01 = at(REVIEW_HEAD, REVIEW_ROOT + SUPERSEDED_V01[0])
    check(digest(v01) == SUPERSEDED_V01[1], "Superseded lavatory v01 preserved at approved review head")
    check(at(FOCUS_SRC[0], REVIEW_ROOT + SUPERSEDED_V01[0]) == v01,
          "Superseded lavatory v01 unchanged since its original review commit")
    check(all(v["sha256"] != SUPERSEDED_V01[1] for v in preview.values()),
          "Superseded lavatory v01 is not a selected image")
    check(git("merge-base", "--is-ancestor", SCENE_SRC[0], REVIEW_HEAD) == b"" and
          git("merge-base", "--is-ancestor", FOCUS_SRC[0], REVIEW_HEAD) == b"",
          "Both source commits are ancestors of the approved review head")

    # 3. Unapproved collision alternatives are absent from canon.
    selected_hashes = {digest((ROOT / v["file"]).read_bytes()) for v in preview.values()}
    for alt in UNAPPROVED_ALTERNATIVES:
        check(alt not in selected_hashes and all(v["sha256"] != alt for v in preview.values()),
              "Unapproved Claude collision alternative not registered: " + alt[:12])

    # 4. Exactly two new selections with exact provenance.
    check(len(preview) == len(previous) + 2 and SCENE_KEY not in previous and FOCUS_KEY not in previous,
          "Exactly two new canonical image selections")
    for key, filename, sha, size, (commit, src) in (
        (SCENE_KEY, SCENE, SCENE_SHA, [314, 206], SCENE_SRC),
        (FOCUS_KEY, FOCUS, FOCUS_SHA, [564, 278], FOCUS_SRC),
    ):
        check(preview[key] == {
            "file": filename, "sha256": sha, "size": size, "alpha": "opaque",
            "source": {"repo": REPO, "ref": REVIEW_REF, "commit": commit, "path": REVIEW_ROOT + src},
        }, "Approved artwork source metadata: " + key)

    # 5. Registry records: approved, not integrated, hashes recorded.
    scene = art["scenes"]["grand_bellevue/bridal_lavatory"]
    focus = art["focus"]["grand_bellevue/three_seashells"]
    check(scene["kind"] == "scene" and scene["status"] == "approved" and
          scene["dimensions"] == "314x206" and scene["assetPath"] is None,
          "Lavatory record approved, not integrated")
    check(focus["kind"] == "focus" and focus["status"] == "approved" and
          focus["dimensions"] == "564x278" and focus["assetPath"] is None,
          "Seashell Focus record approved on the 564x278 Focus A contract, not integrated")
    check(SCENE_SHA in scene["notes"] and SUPERSEDED_V01[1] in scene["notes"] and
          FOCUS_SHA in focus["notes"] and REVIEW_HEAD in scene["notes"] and REVIEW_HEAD in focus["notes"],
          "Owner-approved hashes, superseded v01 and review head recorded in registry notes")
    bathroom_ai = art["portraits"]["bathroom_ai:neutral"]
    check(bathroom_ai.get("format") == "voice-only" and bathroom_ai.get("assetPath") is None and
          "portraits:bathroom_ai:neutral" not in preview,
          "Bathroom AI remains an approved voice-only record with no image")

    # 6. Story nodes already use the approved keys; nothing about them changes.
    for node_id in SEASHELL_SCENE_NODES:
        check(nodes[node_id]["scene"] == "grand_bellevue/bridal_lavatory",
              "Existing node uses the selected lavatory scene key: " + node_id)
    inspect = nodes["hotel_seashell_inspect"]
    check(inspect["mode"] == "focus" and inspect["focus"] == "grand_bellevue/three_seashells",
          "hotel_seashell_inspect uses the selected Focus key")
    check({c["id"] for c in inspect["choices"]} ==
          {"shell_focus_try", "shell_focus_ask", "shell_focus_complain", "shell_focus_leave"},
          "All four seashell Focus choice IDs intact")

    # 7. Everything earlier is unchanged.
    for key, entry in previous.items():
        check(preview.get(key) == entry and digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"],
              "Earlier selected art and metadata unchanged: " + key)
    without_new = deepcopy(art)
    del without_new["scenes"]["grand_bellevue/bridal_lavatory"]
    del without_new["focus"]["grand_bellevue/three_seashells"]
    check(without_new == json.loads(at(BASE, "story/artwork.draft.json")),
          "All previous artwork records, statuses and metadata untouched")
    check("focus:grand_bellevue/autofit_gown" not in preview and
          "grand_bellevue/autofit_gown" not in art["focus"],
          "B2-13 is not registered on the canonical base; nothing B2-13 is added or removed")
    changed = set(git("diff", "--name-only", BASE, "--").decode().split()) | \
        set(git("ls-files", "--others", "--exclude-standard").decode().split())
    check(changed <= EXPECTED_CHANGES,
          "Only the registration files differ from canonical base: " + ", ".join(sorted(changed)))
    for filename in (
        "story/chapters/chapter-04.wip.json", "story/chapter-04.wip-review-layout.json",
        "story/game-integration.json", "story/storyboard-manifest.json",
        "story/items.draft.json", "story/sync-contract.json",
    ):
        check((ROOT / filename).read_bytes() == at(BASE, filename),
              "No narrative, gameplay, item, flag or runtime change: " + filename)
    approved_tree = git("ls-tree", "-r", "HEAD", "tools/prologue-art-lab/assets/approved/")
    check(approved_tree == git("ls-tree", "-r", BASE, "tools/prologue-art-lab/assets/approved/"),
          "Preserved approved/conditional/inspection/retired references unchanged")
    pr32 = git("ls-remote", "origin", "refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124").split()[0].decode()
    check(pr32 == PR32_HEAD, "Draft PR #32 head unchanged")

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE,
        "approvedReviewHead": REVIEW_HEAD, "selectedPrimaryCount": 2,
        "selected": {SCENE_KEY: {"file": SCENE, "sha256": SCENE_SHA, "sourceCommit": SCENE_SRC[0]},
                     FOCUS_KEY: {"file": FOCUS, "sha256": FOCUS_SHA, "sourceCommit": FOCUS_SRC[0]}},
        "supersededHistoricalReviewArtwork": {"path": REVIEW_ROOT + SUPERSEDED_V01[0], "sha256": SUPERSEDED_V01[1],
                                              "commit": REVIEW_HEAD, "selected": False},
        "unapprovedCollisionAlternativesRegistered": 0,
        "priorSelectedAssetsUnchanged": len(previous),
        "b213RegisteredOnBase": False,
        "sourceDerived": True, "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(checks)} checks passed; 2 selected canonical assets; superseded v01 preserved; "
          f"{len(previous)} prior selections unchanged; gameplay unchanged")


if __name__ == "__main__":
    main()
