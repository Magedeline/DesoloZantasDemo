"""Build the GameBanana-sized demo packages from the Mods/DesoloZantasDemo folder.

  python -I build_split.py <mod folder> <out dir> <version>

Writes <out>/DesoloZantasDemo.zip (code, maps, dialog, trimmed graphics) and
<out>/DesoloZantasDemoAudio.zip (the FMOD banks), each under GameBanana's upload cap.
"""
import os, re, sys, time, zipfile

src, out, ver = sys.argv[1], sys.argv[2], sys.argv[3]
MAIN = os.path.join(out, "DesoloZantasDemo.zip")
AUDIO = os.path.join(out, "DesoloZantasDemoAudio.zip")

# Folders that ship in the main zip, relative to the mod folder.
SHIP_DIRS = ["bin", "Dialog", "Graphics", "Maps", "Tutorials", "Loenn"]
SHIP_FILES = ["Credits.txt"]

# Everything matching one of these (path relative to the mod folder, forward slashes) stays out.
DROP_PREFIX = [
    "Loenn/pcg/", "Loenn/scripts/pcg_",
    "Graphics/Atlases/Mountain/CEL/",             # Desolo Zantas overworld textures: chapters 10+ only
    "Graphics/Atlases/FinalCutscenes/",           # chapter 21 ending
    "Graphics/Atlases/Memo/",                     # chapter 5 cutscene
    # complete screens of chapters 5+ (CompleteScreens.xml keeps the entries; they load lazily)
    "Graphics/Atlases/Fractured/", "Graphics/Atlases/Stronghold/", "Graphics/Atlases/Truth/",
    "Graphics/Atlases/VortexIntro/", "Graphics/Atlases/VortexEnd/", "Graphics/Atlases/Core/",
    "Graphics/Atlases/Inferno/", "Graphics/Atlases/Finale/", "Graphics/Atlases/Ruins/",
    "Graphics/Atlases/SnowdinCity/", "Graphics/Atlases/WaterEdge/", "Graphics/Atlases/HotCliff/",
    "Graphics/Atlases/CyberNexus/", "Graphics/Atlases/Citadel/", "Graphics/Atlases/MyWorld/",
]
# Late-chapter boss sprite folders (their Sprites.xml entries are cut below).
DROP_CHARS = ["els_true_final_boss", "morpho_knight_delta", "asrielgodboss", "darkmatter_boss",
              "roaring_spawn_titan", "asrielangelofdeathboss", "madelinegod", "vessel_boss",
              "darkerdark_swordsman"]
DROP_PREFIX += [f"Graphics/Atlases/Gameplay/characters/CEL/{c}/" for c in DROP_CHARS]
DROP_SPRITES = ["madelinegod", "asriel_angelofdeath", "chara_final_beam", "els_true_final_boss",
                "asrielgodboss", "darkerdark_swordsman", "galacta_knight_clone", "morpho_knight_clone",
                "morpho_knight_delta", "mkd_fx"]
KEEP_CHECKPOINTS = re.compile(r"^Graphics/Atlases/Checkpoints/CEL/Area/0[0-4]_[^/]+/A/")


def dropped(rel):
    low = rel.lower()
    if low.endswith((".ase", ".gitkeep", ".bak")) or re.search(r"\.bak\d+$", low):
        return True
    if any(rel.startswith(p) for p in DROP_PREFIX):
        return True
    if rel.startswith("Graphics/Atlases/Checkpoints/") and not KEEP_CHECKPOINTS.match(rel):
        return True
    return False


def trim_sprites_xml(text):
    for name in DROP_SPRITES:
        pat = re.compile(rf"^[ \t]*<{name} +path=\"[^\"]*\".*?^[ \t]*</{name}>[ \t]*\r?\n", re.S | re.M)
        text, n = pat.subn("", text)
        assert n == 1, (name, n)
    return text


def main_yaml(text):
    text, n = re.subn(r"^(  Version: )\S+", rf"\g<1>{ver}", text, count=1, flags=re.M)
    assert n == 1
    dep = f"    - Name: DesoloZantasDemoAudio\n      Version: {ver}\n"
    text, n = re.subn(r"^(  Dependencies:\r?\n)", r"\g<1>" + dep, text, count=1, flags=re.M)
    assert n == 1
    return text


AUDIO_YAML = f"""- Name: DesoloZantasDemoAudio
  Version: {ver}
  Dependencies:
    - Name: Everest
      Version: 1.6458.0
"""


def add(zo, rel, data, mtime):
    info = zipfile.ZipInfo(rel, date_time=time.localtime(mtime)[:6])
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zo.writestr(info, data)


def walk(dirname):
    for root, dirs, files in os.walk(os.path.join(src, dirname)):
        dirs.sort()
        for f in sorted(files):
            full = os.path.join(root, f)
            yield os.path.relpath(full, src).replace("\\", "/"), full


dropped_list, kept = [], 0
with zipfile.ZipFile(MAIN, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zo:
    ymlp = os.path.join(src, "everest.yaml")
    add(zo, "everest.yaml", main_yaml(open(ymlp, encoding="utf-8").read()).encode("utf-8"), os.path.getmtime(ymlp))
    for f in SHIP_FILES:
        p = os.path.join(src, f); add(zo, f, open(p, "rb").read(), os.path.getmtime(p)); kept += 1
    for d in SHIP_DIRS:
        for rel, full in walk(d):
            if dropped(rel):
                dropped_list.append(rel); continue
            data = open(full, "rb").read()
            if rel == "Graphics/Sprites.xml":
                data = trim_sprites_xml(data.decode("utf-8")).encode("utf-8")
            add(zo, rel, data, os.path.getmtime(full)); kept += 1

with zipfile.ZipFile(AUDIO, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zo:
    add(zo, "everest.yaml", AUDIO_YAML.encode("utf-8"), time.time())
    # Only the demo banks. The folder also holds the full mod's MUS_A / DLC_MUS banks (650 MB).
    AUDIO_KEEP = {"Celestellaris_MUS_DEMO.bank", "Celestellaris_SFX_DEMO.bank", "Celestellaris_UI_DEMO.bank",
                  "Master Bank.bank", "Master Bank.strings.bank"}
    for rel, full in walk("Audio"):
        if os.path.basename(rel) in AUDIO_KEEP:
            add(zo, rel, open(full, "rb").read(), os.path.getmtime(full))

open(os.path.join(out, "dropped_from_main.txt"), "w", encoding="utf-8").write("\n".join(dropped_list) + "\n")
print(f"main: kept {kept} files, dropped {len(dropped_list)}; {os.path.getsize(MAIN)/1e6:.1f} MB")
print(f"audio: {os.path.getsize(AUDIO)/1e6:.1f} MB")
