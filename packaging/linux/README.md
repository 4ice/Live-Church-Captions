# Church Cap Linux CLI package

Church Cap v0.8.0 for Linux is a curated, architecture-neutral source archive. It contains the shared browser application and the package-manager-aware Linux setup, start, update, CUDA, translation, spoken-language, and password-recovery helpers. It intentionally contains no Tauri wrapper, macOS/Windows artifacts or named updater scripts, Finder `.DS_Store` metadata, repository history, tests, build caches, or developer toolchains.

Build on any platform:

```text
python scripts/release/build-linux-cli-release.py
python scripts/release/check-linux-cli-release.py dist/releases/Church-Cap-Linux-CLI.tar.gz
```

The archive must still pass clean installation and upgrade acceptance on representative Debian/Ubuntu and RHEL/AlmaLinux-family x86_64 systems before publication.

Current rebuilt candidate: 190 files, 948,856 bytes, SHA-256 `a1453e41cdde9a8217fb6184e44e31a778a541eb04fe9ae52ab307db9c0c2672`. The build is deterministic and the validator rejects `update-macos.sh`, `.DS_Store`, links, unsafe paths, desktop/build trees, or missing shared engine/update/project-local Python helpers. The pinned x86_64 glibc `uv` bootstrap was independently downloaded and matched its embedded SHA-256; Ubuntu 26.04 setup now passes, while startup of this engine-inclusive rebuild and RHEL-family installation acceptance remain required.
