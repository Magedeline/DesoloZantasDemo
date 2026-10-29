# Desolo Zantas: Demo (Prologue to Chapter 4)

A separate copy of the mod for the 4-chapter demo. Everest name `DesoloZantasDemo`, assembly `DesoloZantasDemo.dll`. The full mod (`Mods/CEL`, `Celestellaris`) is unchanged and separate.

- **Do not enable it together with the full mod.** Both define the same map SIDs (`CEL/Area/...`), entity IDs, sprite IDs, dialog keys and audio event paths. Disable one in Olympus.
- **Maps:** Prologue and Chapters 1 to 4, A-Side only.
- **Dialog (trimmed):** every key for Chapter 5 onward (`CEL_CH5_` and up, the chapter-named keys like `CEL_0_15_Castle`, souls, poems, postcards) is removed from all seven files. Keys without a chapter number (NPC or boss names, shared UI) are still there.
- **Code (trimmed):** 217 files for later chapters were removed (cutscenes, NPCs, `Ch*` entity folders, most bosses). The rest stays because the shared core references it: `CELModule`, `EventTrigger`, `VignetteHooks` and the boss base classes still name later-chapter types, so some later-chapter code is still compiled in. Fully removing it means editing those hubs.
- **Not trimmed yet:** `Graphics/`, `Audio/` banks, `Loenn/`.
- Build: `dotnet build Source/DesoloZantasDemo.csproj -c Debug`. It builds. It has not been loaded in the game.

## Install

Drop `DesoloZantasDemo.zip` into `Celeste/Mods` (do not unzip) with the full mod disabled or removed. Everest installs the helper mods listed in `everest.yaml` on first launch.

## Zip contents

Since 0.1.6 the demo ships as **two zips**, both under GameBanana's 210 MB upload cap, built by
`tools/build_release.py` from the `Mods/DesoloZantasDemo` folder:

```
python -I tools/build_release.py <path to Mods/DesoloZantasDemo> <output folder> <version>
```

- `DesoloZantasDemo.zip` (about 150 MB): `everest.yaml`, `bin/`, `Dialog/`, `Graphics/`, `Maps/`, `Tutorials/`, `Loenn/`, `Credits.txt`.
  Its `everest.yaml` depends on `DesoloZantasDemoAudio` at the same version. Only chapter 0 to 4 assets are included: the
  script drops the `Mountain/` models and `Graphics/Atlases/Mountain/CEL` textures (chapters 0 to 9 use the vanilla mountain),
  the Checkpoints images of other chapters and sides, the complete-screen atlases of chapters 5+, `FinalCutscenes`, `Memo`,
  the late-chapter boss sprite folders (with their `Sprites.xml` entries), `.ase` sources, `GUIDs.txt` and `Loenn/pcg`.
  `dropped_from_main.txt` next to the zips lists every file left out.
- `DesoloZantasDemoAudio.zip` (about 181 MB): the five demo FMOD banks and a minimal `everest.yaml`
  (`Name: DesoloZantasDemoAudio`). Upload it to GameBanana first so the main zip's dependency resolves.

The source code is not in either zip. The old single-zip packages (0.1.4, 0.1.5) are 568 MB and can only be hosted on GitHub.

`DesoloZantasDemo_0.1.2_broken_tar_not_zip.tar` in this folder is the 2026-10-14 upload: a tar archive that was named `.zip`. Everest cannot load it. Never upload it again.
