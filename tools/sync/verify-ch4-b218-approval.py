"""Verify Nate's Chapter 4 B2-18 approval: five restroom conditional state references + one narrative fix.

Five v01 state references are APPROVED / PRESERVED byte-for-byte in the approved conditional-reference
folder, with no artwork key, Focus ID, flag or runtime binding. restroom-braced-main stays an UNSELECTED
alternative on the review branch only. The restroom master records gain only an appended dated note.
The only narrative change is the authorized hotel_upper_salvage_arrival correction: one description run
(empty stall enclosure hangs in the mezzanine, the toilet stays on the restroom floor) and the line
THE TOILET! -> THE STALL!. Every selection, record, choice, condition, flag and roll is otherwise unchanged.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "2af6606c25ce252752c65aa5c68c87ff84f804ae"
REVIEW_HEAD = "109e201bdd99418aae66a73efa29acfafee8be94"
REVIEW_HISTORY = ("be883d9", "760bdac", "74874c8", "c6a9dc8", REVIEW_HEAD)  # be883d9 introduced the PNGs
PKG_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/"
PKG = PKG_ROOT + "v01/"
DEST = "tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-18/"
APPROVED_ROOT = "tools/prologue-art-lab/assets/approved/"
PR32_HEAD = "f320e63934c13e27fd13b9482d0cfba58911362d"
CHAPTER = "story/chapters/chapter-04.wip.json"
NODE = "hotel_upper_salvage_arrival"

APPROVED = {  # name: (sha256, size, parent record)
    "restroom-active-leak-main": ("9a6243310bb7af1958854110af742c603275b2ebf9c889050c6c065737e57279", (314, 206), "scene"),
    "restroom-active-leak-close": ("35a8f8297da89038a0a7b30596363bfa6ad86e3edc6b02bf0efb360a4dc3a46a", (564, 278), "portraitBackground"),
    "restroom-contained-main": ("674cb60c905347e99c95b99ec87dfacc218cf15483abe89bc4e092d40b43ed1a", (314, 206), "scene"),
    "restroom-flood-onset-main": ("432ce64f5e7e0420f678774ec8cf2edb02ce745ff532d83b3e1723af9d90fb46", (314, 206), "scene"),
    "restroom-stall-lifting-main": ("84976c116d9fc87b6ce8f4cf5d7f316d7185fa308f889df6d1c76eafe6bc525e", (314, 206), "scene"),
}
UNSELECTED = ("restroom-braced-main", "dcbe6ebf8319e3fe0dabe9c30637494e51342303be9923aba29ccd71acca7fcd")
OLD_DESC = {"desc": "The toilet is still inside the stall. Its plumbing has been disconnected, and the whole arrangement hangs several feet above the floor."}
NEW_DESC = {"desc": "The stall is only an empty enclosure now. It hangs from the crane cables in the mezzanine, several feet above the floor. The toilet stayed downstairs, still fixed to the restroom floor."}
OLD_LINE, NEW_LINE = {"say": "THE TOILET!", "who": "you"}, {"say": "THE STALL!", "who": "you"}

EXPECTED_CHANGES = {
    "story/artwork.draft.json", CHAPTER, "tools/sync/verify-ch4-b218-approval.py",
    "docs/150_CH4_B218_APPROVAL_COMPLETION_20261126.md", "docs/150_CH4_B218_VERIFICATION_20261126.json",
} | {DEST + name + ".png" for name in APPROVED}
REPORT = ROOT / "docs/150_CH4_B218_VERIFICATION_20261126.json"


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

    manifest = json.loads(at(REVIEW_HEAD, PKG + "manifest.json"))
    candidates = {c["name"]: c for c in manifest["newCandidates"]}
    art, base_art = json.loads((ROOT / "story/artwork.draft.json").read_text()), json.loads(at(BASE, "story/artwork.draft.json"))
    preview = json.loads((ROOT / "story/artwork-preview.json").read_text())["images"]
    base_preview = json.loads(at(BASE, "story/artwork-preview.json"))["images"]

    for older, newer in zip(REVIEW_HISTORY, REVIEW_HISTORY[1:]):
        check(git("merge-base", "--is-ancestor", older, newer) == b"", f"Review history {older[:7]} precedes {newer[:7]}")
    check(set(candidates) == set(APPROVED) | {UNSELECTED[0]}, "Review manifest holds exactly the six B2-18 candidates")

    # Five approved references: exact bytes, format, manifest and review identity, no key or binding.
    selected_hashes = {e["sha256"] for e in preview.values()}
    for name, (sha, size, _) in APPROVED.items():
        raw = (ROOT / DEST / (name + ".png")).read_bytes()
        check(digest(raw) == sha, f"Exact approved PNG hash: {name}")
        with Image.open(BytesIO(raw)) as image:
            check(image.size == size and image.mode == "RGB", f"Native {size[0]}x{size[1]} opaque RGB: {name}")
        c = candidates[name]
        check(c["sha256"] == sha and list(c["dimensions"]) == list(size) and c["runtimeBinding"] is None
              and c["focusId"] is None and c["newStoryFlag"] is None,
              f"Matches review manifest; no runtime binding, Focus ID or new flag: {name}")
        for ref in REVIEW_HISTORY:
            check(at(ref, PKG + f"native/{name}.png") == raw, f"Byte-identical to review source at {ref[:7]}: {name}")
        check(sha not in selected_hashes, f"Reference only, not a selected canonical image: {name}")

    # Braced alternative: preserved UNSELECTED on the review branch, not copied or selected.
    name, sha = UNSELECTED
    check(digest(at(REVIEW_HEAD, PKG + f"native/{name}.png")) == sha == candidates[name]["sha256"],
          "Braced alternative preserved unchanged on the review branch")
    tracked = git("ls-files", "-s").decode().split("\n")
    braced_blob = subprocess.run(["git", "hash-object", "--stdin"], cwd=ROOT, input=at(REVIEW_HEAD, PKG + f"native/{name}.png"),
                                 capture_output=True, check=True).stdout.decode().strip()
    check(not any(braced_blob in line for line in tracked) and sha not in selected_hashes,
          "Braced alternative is not copied into main and not selected")

    # Approved tree: exactly the five new references were added; everything else unchanged.
    base_tree = {line.split("\t")[1]: line.split()[2] for line in git("ls-tree", "-r", BASE, APPROVED_ROOT).decode().splitlines()}
    work_paths = set(git("ls-files", "--cached", "--others", "--exclude-standard", APPROVED_ROOT).decode().splitlines())
    work_paths = {p for p in work_paths if (ROOT / p).exists()}
    work_tree = dict(zip(sorted(work_paths), git("hash-object", "--", *sorted(work_paths)).decode().split()))
    check(all(work_tree.get(p) == blob for p, blob in base_tree.items()) and
          sorted(set(work_tree) - set(base_tree)) == sorted(DEST + n + ".png" for n in APPROVED),
          "Approved reference tree gains exactly the five B2-18 files; every earlier reference unchanged")
    check(git("ls-tree", "-r", "--name-only", "HEAD", PKG_ROOT) == b"",
          "Review package (originals, prompts, layers, masks, held attempt) stays on the review branch")

    # Selections and registry: no new selection; only the two restroom master notes gain an appended line.
    check(preview == base_preview, "artwork-preview.json unchanged: no new canonical selection or key")
    for key, entry in base_preview.items():
        check(digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"], "Earlier selected art bytes unchanged: " + key)
    scene, base_scene = art["scenes"]["grand_bellevue/restroom"], base_art["scenes"]["grand_bellevue/restroom"]
    for record, base_record, label in ((scene, base_scene, "scene"),
                                       (scene["portraitBackground"], base_scene["portraitBackground"], "portraitBackground")):
        names = [n for n, v in APPROVED.items() if v[2] == label]
        check(record["notes"].startswith(base_record["notes"] + " | B2-18 ")
              and all(n in record["notes"] and APPROVED[n][0] in record["notes"] for n in names),
              f"Restroom {label} note keeps its text verbatim and appends the B2-18 references")
    check(UNSELECTED[1] in scene["notes"] and "UNSELECTED" in scene["notes"], "Braced alternative recorded as UNSELECTED")
    restored = deepcopy(art)
    restored["scenes"]["grand_bellevue/restroom"]["notes"] = base_scene["notes"]
    restored["scenes"]["grand_bellevue/restroom"]["portraitBackground"]["notes"] = base_scene["portraitBackground"]["notes"]
    check(restored == base_art, "Registry otherwise untouched: no new key, status, hash, prompt or path")

    # Narrative: exactly the two authorized runs in one node.
    chapter, base_chapter = json.loads((ROOT / CHAPTER).read_text()), json.loads(at(BASE, CHAPTER))
    node, base_node = chapter["nodes"][NODE], base_chapter["nodes"][NODE]
    check(base_node["text"][2] == OLD_DESC and node["text"][2] == NEW_DESC,
          "Description now: empty stall enclosure hangs in the mezzanine; toilet stays on the restroom floor")
    check(base_node["text"][6] == OLD_LINE and node["text"][6] == NEW_LINE, "Protagonist line THE TOILET! -> THE STALL!")
    check(len(node["text"]) == len(base_node["text"]) and all(
        a == b for i, (a, b) in enumerate(zip(node["text"], base_node["text"])) if i not in (2, 6)),
        "Every other run (joke, dialogue, speakers, closing description) unchanged")
    check({k: v for k, v in node.items() if k != "text"} == {k: v for k, v in base_node.items() if k != "text"},
          "Choice IDs, targets, conditions, effects, flags, scene, speaker and notes unchanged")
    restored_chapter = deepcopy(chapter)
    restored_chapter["nodes"][NODE] = base_node
    check(restored_chapter == base_chapter, "No other Chapter 4 node, route, roll or flag changed")
    check("toilet is still inside the stall" not in (ROOT / CHAPTER).read_text().lower(),
          "Contradicting claim removed from canonical narrative")

    changed = set(git("diff", "--name-only", BASE, "--").decode().split()) | \
        set(git("ls-files", "--others", "--exclude-standard").decode().split())
    check(changed <= EXPECTED_CHANGES, "Only approval files differ from canonical base: " + ", ".join(sorted(changed)))
    for filename in ("story/artwork-preview.json", "story/chapter-04.wip-review-layout.json", "story/storyboard-layout.json",
                     "story/death-presentations.export.json", "story/game-integration.json",
                     "story/storyboard-manifest.json", "story/items.draft.json", "story/sync-contract.json",
                     "tools/storyboard/qa-smoke.mjs", "tools/storyboard/qa-browser.js"):
        check((ROOT / filename).read_bytes() == at(BASE, filename), "No gameplay, popup, layout or runtime change: " + filename)
    pr32 = git("ls-remote", "origin", "refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124").split()[0].decode()
    check(pr32 == PR32_HEAD, "Draft PR #32 head unchanged")

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE, "approvedReviewHead": REVIEW_HEAD,
        "sourceCommit": "be883d9", "approvedPreservedReferences": {
            name: {"file": DEST + name + ".png", "sha256": v[0], "size": list(v[1]), "parentRecord":
                   "scenes:grand_bellevue/restroom" + ("#portraitBackground" if v[2] == "portraitBackground" else "")}
            for name, v in APPROVED.items()},
        "unselectedAlternative": {UNSELECTED[0]: UNSELECTED[1]},
        "newCanonicalSelections": 0, "priorSelectedAssetsUnchanged": len(base_preview),
        "narrativeCorrection": {"node": NODE, "runs": [2, 6], "before": [OLD_DESC, OLD_LINE], "after": [NEW_DESC, NEW_LINE]},
        "newKeysFocusIdsFlagsOrBindings": False, "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(checks)} checks passed; 5 references preserved; braced UNSELECTED; "
          f"{len(base_preview)} selections unchanged; one authorized narrative correction")


if __name__ == "__main__":
    main()
