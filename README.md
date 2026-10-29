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

`everest.yaml`, `bin/`, `Audio/`, `Dialog/`, `Graphics/`, `Maps/`, `Loenn/`, `Mountain/`, `Tutorials/`, `Credits.txt`. The source code is not in the zip. Since 0.1.5 the package also leaves out dev-only files: `.ase` sources, `GUIDs.txt`, `Loenn/pcg/` and the `pcg_*.lua` scripts (see `ZippedFilesExclude` in the csproj).

`DesoloZantasDemo_0.1.2_broken_tar_not_zip.tar` in this folder is the 2026-10-14 upload: a tar archive that was named `.zip`. Everest cannot load it. Never upload it again.
