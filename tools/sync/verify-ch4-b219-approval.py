"""Verify Nate's Chapter 4 B2-19 approval: three lobby / Lot 61 conditional state references.

Three v01 references are APPROVED / PRESERVED byte-for-byte in the approved conditional-reference folder,
with no artwork key, Focus ID, flag or runtime binding. The selected CH4-01 lobby master stays selected and
unchanged; its record gains only an appended, dated note with the conditional timing. The restroom
conversation background (CH4-B2-03) gains a dated note recording the B2-18 post-lift decision: reuse it
unchanged for hotel_stall_porter_protest. The fatal FOLDED FOR CONVENIENCE illustration is unchanged.
No narrative, gameplay, engine or selection change.
"""

from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BASE = "3785e87506c4218a360cf7a309b2fbe690cc4546"
REVIEW_HEAD = "7c85a4150655d1988866dafd7278d2a4a0aba0f3"
REVIEW_HISTORY = ("801dbd91c89742b9272d451188297ddac9b0b9f3", "6305bd70c566e7dd254b40d9cce17d6c02f356c0", REVIEW_HEAD)
PKG_ROOT = "tools/prologue-art-lab/assets/review/chapter-04-b219-lobby-states-2026-11-26/"
PKG = PKG_ROOT + "v01/"
DEST = "tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-19/"
APPROVED_ROOT = "tools/prologue-art-lab/assets/approved/"
PR32_HEAD = "f320e63934c13e27fd13b9482d0cfba58911362d"

APPROVED = {  # name: (published sha256, nodes the timing note must name)
    "lobby-doors-removed": ("e2aa3835dca0edf1e76b93df2a3cf628db8dc5ff8f56c1f5df8e6188ea7d218e", ("hotel_auctioneer_arrival",)),
    "lot61-open": ("3913c8ad89c0245c31827f1933926ff0d1a00ec9da71f34dfa9818ff222c42b5", ("hotel_lot61_pod_auction", "hotel_lot61_pod_declined")),
    "lot61-packed": ("f3c27be75a18007850f8eb9bff7ae71f031063aa44735f9bfbd24bf5d876b558", ("hotel_lot61_pod_escaped",)),
}
PRESERVED_SELECTIONS = {
    "scenes:grand_bellevue/lobby": "582bcd51de937e5fe124160a8beb74b4ee469f52eeb6d9d0d38b918cfb0d6be0",
    "scenes:grand_bellevue/restroom#portraitBackground": "77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377",
    "deathScreens:grand_bellevue/folded_for_convenience": "30490a4259b363879dc126e273dcc07bb979d96ad4f6534dd75cb7e3901ddc07",
}
EXPECTED_CHANGES = {
    "story/artwork.draft.json", "tools/sync/verify-ch4-b219-approval.py",
    "docs/151_CH4_B219_APPROVAL_COMPLETION_20261126.md", "docs/151_CH4_B219_VERIFICATION_20261126.json",
} | {DEST + name + ".png" for name in APPROVED}
REPORT = ROOT / "docs/151_CH4_B219_VERIFICATION_20261126.json"


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
    publication = at(REVIEW_HEAD, PKG_ROOT + "PUBLICATION.md").decode()
    public_receipt = at(REVIEW_HEAD, PKG_ROOT + "PUBLIC-BYTE-VERIFICATION.json").decode()
    art, base_art = json.loads((ROOT / "story/artwork.draft.json").read_text()), json.loads(at(BASE, "story/artwork.draft.json"))
    preview = json.loads((ROOT / "story/artwork-preview.json").read_text())["images"]
    base_preview = json.loads(at(BASE, "story/artwork-preview.json"))["images"]

    for older, newer in zip(REVIEW_HISTORY, REVIEW_HISTORY[1:]):
        check(git("merge-base", "--is-ancestor", older, newer) == b"", f"Review history {older[:7]} precedes {newer[:7]}")
    check(set(candidates) == set(APPROVED), "Review manifest holds exactly the three approved B2-19 candidates")
    check(manifest["runtimeBindingsAdded"] is False and manifest["FocusIdsAdded"] is False
          and manifest["flagsOrModesAdded"] is False, "Review manifest adds no runtime binding, Focus ID, flag or mode")

    selected_hashes = {e["sha256"] for e in preview.values()}
    for name, (sha, _) in APPROVED.items():
        raw = (ROOT / DEST / (name + ".png")).read_bytes()
        check(digest(raw) == sha, f"Exact approved PNG hash: {name}")
        check(sha in publication and sha in public_receipt, f"Hash matches PUBLICATION.md and the public byte receipt: {name}")
        with Image.open(BytesIO(raw)) as image:
            check(image.size == (314, 206) and image.mode == "RGB", f"Native 314x206 opaque RGB: {name}")
        c = candidates[name]
        check(c["sha256"] == sha and c["runtimeBinding"] is None and c["focusId"] is None,
              f"Matches review manifest; no runtime binding or Focus ID: {name}")
        for ref in REVIEW_HISTORY:
            check(at(ref, PKG + f"native/{name}.png") == raw, f"Byte-identical to review source at {ref[:7]}: {name}")
        check(sha not in selected_hashes, f"Reference only, not a selected canonical image: {name}")

    # Approved tree: exactly three files added; every earlier approved/conditional reference unchanged.
    base_tree = {line.split("\t")[1]: line.split()[2] for line in git("ls-tree", "-r", BASE, APPROVED_ROOT).decode().splitlines()}
    work_paths = sorted(p for p in git("ls-files", "--cached", "--others", "--exclude-standard", APPROVED_ROOT).decode().splitlines()
                        if (ROOT / p).exists())
    work_tree = dict(zip(work_paths, git("hash-object", "--", *work_paths).decode().split()))
    check(all(work_tree.get(p) == blob for p, blob in base_tree.items()) and
          sorted(set(work_tree) - set(base_tree)) == sorted(DEST + n + ".png" for n in APPROVED),
          "Approved reference tree gains exactly the three B2-19 files; every earlier reference (incl. B2-18) unchanged")
    check(git("ls-tree", "-r", "--name-only", "HEAD", PKG_ROOT) == b"",
          "Review package (originals, prompts, layers, masks, porter assessment) stays on the review branch")

    # Selections: none added; the lobby master, CH4-B2-03 and the fatal illustration stay selected unchanged.
    check(preview == base_preview, "artwork-preview.json unchanged: no new canonical selection or key")
    for key, entry in base_preview.items():
        check(digest((ROOT / entry["file"]).read_bytes()) == entry["sha256"], "Earlier selected art bytes unchanged: " + key)
    for key, sha in PRESERVED_SELECTIONS.items():
        check(preview[key]["sha256"] == sha, "Selected master preserved unchanged: " + key)

    # Registry: only two appended notes.
    lobby, base_lobby = art["scenes"]["grand_bellevue/lobby"], base_art["scenes"]["grand_bellevue/lobby"]
    check(lobby["notes"].startswith(base_lobby["notes"] + " | B2-19 ")
          and all(n in lobby["notes"] and v[0] in lobby["notes"] and all(node in lobby["notes"] for node in v[1])
                  for n, v in APPROVED.items()),
          "Lobby note keeps its text verbatim and appends all three references, hashes and nodes")
    check("after the authored folding finishes" in lobby["notes"] and "ch4_pod_survived_packing" in lobby["notes"]
          and "deathScreens:grand_bellevue/folded_for_convenience" in lobby["notes"] and "fatal_lot61_folded" in lobby["notes"],
          "Timing recorded: packed case only after folding on the escape route; fatal outcome keeps its illustration")
    pb = art["scenes"]["grand_bellevue/restroom"]["portraitBackground"]
    base_pb = base_art["scenes"]["grand_bellevue/restroom"]["portraitBackground"]
    check(pb["notes"].startswith(base_pb["notes"] + " | B2-18 POST-LIFT BACKGROUND DECISION")
          and "hotel_stall_porter_protest" in pb["notes"] and "unchanged" in pb["notes"],
          "B2-18 decision recorded: CH4-B2-03 reused unchanged for hotel_stall_porter_protest")
    restored = deepcopy(art)
    restored["scenes"]["grand_bellevue/lobby"]["notes"] = base_lobby["notes"]
    restored["scenes"]["grand_bellevue/restroom"]["portraitBackground"]["notes"] = base_pb["notes"]
    check(restored == base_art, "Registry otherwise untouched: no new key, status, hash, prompt or path")

    # Canon the timing relies on is unchanged and still as recorded.
    nodes = json.loads((ROOT / "story/chapters/chapter-04.wip.json").read_text())["nodes"]
    check(nodes["hotel_lot61_pod_escaped"]["effects"] == {"set": {"ch4_pod_survived_packing": True}},
          "Escape node still sets ch4_pod_survived_packing on entry (why the flag alone must not reveal the case)")
    check(nodes["fatal_lot61_folded"]["deathPopup"]["artRef"] == "grand_bellevue/folded_for_convenience"
          and nodes["fatal_lot61_folded"]["endingArt"] == "grand_bellevue/folded_for_convenience",
          "Unsuccessful folding keeps the approved FOLDED FOR CONVENIENCE illustration")
    check(nodes["hotel_stall_porter_protest"]["scene"] == "grand_bellevue/restroom",
          "Porter protest stays on the restroom scene whose closer background is reused")

    changed = set(git("diff", "--name-only", BASE, "--").decode().split()) | \
        set(git("ls-files", "--others", "--exclude-standard").decode().split())
    check(changed <= EXPECTED_CHANGES, "Only approval files differ from canonical base: " + ", ".join(sorted(changed)))
    story_files = [p for p in git("ls-tree", "-r", "--name-only", BASE, "story/").decode().split() if p != "story/artwork.draft.json"]
    for filename in story_files + ["tools/storyboard/qa-smoke.mjs", "tools/storyboard/qa-browser.js",
                                   "docs/150_CH4_B218_APPROVAL_COMPLETION_20261126.md"]:
        check((ROOT / filename).read_bytes() == at(BASE, filename), "Unchanged narrative / gameplay / tooling / history: " + filename)
    pr32 = git("ls-remote", "origin", "refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124").split()[0].decode()
    check(pr32 == PR32_HEAD, "Draft PR #32 head unchanged")

    report = {
        "passed": True, "checksPassed": len(checks), "canonicalBase": BASE, "approvedReviewHead": REVIEW_HEAD,
        "sourceCommit": REVIEW_HISTORY[0],
        "approvedPreservedReferences": {n: {"file": DEST + n + ".png", "sha256": v[0], "size": [314, 206], "nodes": list(v[1]),
                                            "parentRecord": "scenes:grand_bellevue/lobby"} for n, v in APPROVED.items()},
        "b218PostLiftDecision": {"node": "hotel_stall_porter_protest", "reuse": "scenes:grand_bellevue/restroom#portraitBackground",
                                 "sha256": PRESERVED_SELECTIONS["scenes:grand_bellevue/restroom#portraitBackground"]},
        "newCanonicalSelections": 0, "priorSelectedAssetsUnchanged": len(base_preview),
        "newKeysFocusIdsFlagsOrBindings": False, "narrativeChanged": False, "gameplayIntegrationPerformed": False,
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(checks)} checks passed; 3 references preserved; {len(base_preview)} selections unchanged; "
          "B2-18 post-lift reuse recorded; narrative and gameplay unchanged")


if __name__ == "__main__":
    main()
