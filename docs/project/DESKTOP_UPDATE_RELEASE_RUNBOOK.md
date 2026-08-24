# Church Cap Desktop Update Release Runbook

Last updated: 2026-08-21

Church Cap uses Tauri's mandatory updater signature in addition to Apple Developer ID or Windows Authenticode. These trust systems are independent and both are required for a public desktop update.

## Channels and releases

- Mac: GitHub tag/release `macos-vX.Y.Z`; channel `updates/desktop/darwin-aarch64/latest.json`.
- Windows: GitHub tag/release `windows-vX.Y.Z`; channel `updates/desktop/windows-x86_64/latest.json`.
- Linux CLI: GitHub tag/release `linux-vX.Y.Z`; existing CLI updater, not Tauri.
- Appliance: reserve `appliance-vX.Y.Z` only if a separately installed image is published; otherwise document the appliance as a Linux deployment profile.

The version inside every build remains normal semantic version text such as `0.8.1`. Platform prefixes belong to Git tags, not the application version. Independent manifests prevent GitHub's one repository-wide “latest release” selection from coupling the Mac and Windows update cadence.

## Updater signing key

The committed public key is `packaging/updater/church-cap-updater-public.key` and is embedded in `desktop/src-tauri/tauri.conf.json`. The private key must never enter the repository, a release asset, normal logs, diagnostics, or a shared project folder.

On the current release Mac, the encrypted private key is stored outside this project and its password is protected by the macOS Keychain service `Church Cap Tauri Updater Signing Key`. Before the first public v0.8 release:

1. Back up the encrypted private key to an independently encrypted, access-controlled location.
2. Back up the password in the project owner's password manager, separately from the key backup.
3. Restore both into an isolated directory and perform a signing probe.
4. Record who controls recovery access. Losing either item prevents existing installations from trusting future updates.

CI should receive the private key and password only through protected release-environment secrets. Unsigned build/test jobs must not receive them.

## Mac release order

1. Build the frozen engine and release-profile app from locked inputs on Apple Silicon.
2. Set `CHURCH_CAP_CODESIGN_IDENTITY` to the exact Keychain identity, `CHURCH_CAP_CODESIGN_IDENTITY_SHA1` to its 40-character certificate fingerprint, and `CHURCH_CAP_NOTARY_PROFILE` to the validated `notarytool` profile. The fingerprint selector prevents duplicate certificates with the same Apple display name from making `codesign` ambiguous while authority verification still uses the human-readable Developer ID name.
3. Run `scripts/release/sign-macos-app.sh`. It signs nested code from the inside out, verifies Developer ID, Team ID, secure timestamp, Hardened Runtime, and production entitlements, then deliberately defers Gatekeeper until notarization.
4. Run `scripts/release/notarize-macos-app.sh`. It submits a metadata-preserving ZIP, retains Apple's submission/log evidence, staples the accepted ticket to the app, and requires Gatekeeper acceptance.
5. Run `scripts/release/build-macos-updater-artifact.sh` against that exact stapled app. It rejects ad-hoc/no-Team-ID apps, creates `Church-Cap-vX.Y.Z-macOS-Apple-Silicon.app.tar.gz`, and invokes `sign-updater-artifact.sh` for its `.sig`.
6. Run `scripts/release/build-macos-dmg.sh` to create the human-facing DMG from the same stapled app. The production builder rejects internal naming, version drift, ad-hoc/no-Team-ID input, or an unstapled app.
7. Run `scripts/release/notarize-macos-dmg.sh` to sign the DMG, submit it, retain Apple's evidence, staple it, and require the final Gatekeeper assessment.
8. Upload the DMG, updater archive, `.sig`, checksums, notices, SBOM, provenance, and release notes to the draft `macos-vX.Y.Z` release.
9. Run clean-machine/quarantine tests, publish the release, and confirm the updater archive URL is anonymously downloadable.
10. Generate `updates/desktop/darwin-aarch64/latest.json` with `generate-desktop-update-manifest.py`, review its URL/version/signature, then publish that manifest.

The v0.8.0 release Mac has a user-verified `Developer ID Application` identity for Team ID `VCFSA9YLF5`, certificate fingerprint `27744BF4CE7F2729EE04284CEB4579E6244ED9C3`, and a validated `Church Cap Notary` Keychain profile. Certificate names and fingerprints are public release metadata; no private key, certificate export, Apple password, or app-specific password belongs in this project or its logs.

## Windows release order

Use the matching order on a clean Windows x64 builder: frozen-engine verification, NSIS build, Authenticode signing and verification when required, Tauri `.sig`, clean-machine tests, publish `windows-vX.Y.Z`, confirm the asset URL, then publish `updates/desktop/windows-x86_64/latest.json`. The shared-core and wrapper source-of-truth rules are in `CROSS_PLATFORM_ARCHITECTURE.md`; current release status is recorded in `V0.8.0_IMPLEMENTATION.md`.

## Required update acceptance

A release is not complete until the previous installed version:

- reports the correct new version and release notes;
- rejects missing, altered, and wrong-key signatures;
- refuses installation while captions are live, including when captions start during download;
- preserves passwords, settings, models, logs, and privacy choices;
- stops its owned engine cleanly only after verification;
- installs, relaunches, passes compatible `/health`, and reports the new running version;
- recovers honestly from network loss, full disk, locked files, installer failure, and failed post-update health.

v0.8.0 currently has no published manifest by design. Its real GitHub check displays “Update channel not published yet” and keeps running normally until a newer signed desktop release is available.
