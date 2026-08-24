# Roadmap To v1.0.0

Church Cap v0.8.0 development continues the move from a single preview app toward one maintained codebase with two supported experiences:

- the open-source desktop app for macOS, Windows, and Linux
- the Church Cap Appliance profile for locked-down AlmaLinux boxes

The aim is not to fork the app. Shared captioning, audio, translation, security, update, and UI code should stay in one project. Appliance-specific behaviour should be selected by explicit deployment identity, not by guessing from hardware.

## v0.5.x Stabilisation

- Keep the explicit deployment profile system: `desktop`, `appliance_cpu`, and `appliance_gpu`.
- Keep appliance setup on the secure local operator port `9090`.
- Finish server-side capability guards so appliance limits cannot be bypassed by stale runtime settings or manual API calls.
- Add regression tests for deployment profiles, CPU appliance translation caps, warning flows, and appliance identity files.
- Continue polishing the appliance shell on 7-inch touch displays.

## v0.6.x Translation Performance And Efficient Runtimes

- Move heavier translation paths toward CTranslate2/INT8 where practical, starting behind feature/provider checks rather than replacing Argos abruptly.
- Keep Argos as the lightweight Base path for language packs that perform well enough.
- Keep SMaLL-100 available as Core while measuring whether converted CTranslate2 models can give better throughput and lower memory use.
- Investigate AMD ROCm as an experimental Linux path only after CUDA and CPU/int8 paths are stable.
- Benchmark CPU-only systems with 1-2 active translated languages and GPU systems with higher active-language limits.
- Add clearer operator recommendations based on measured latency, CPU load, GPU readiness, and active viewer-language demand.

## v0.7.x Translation Readability And Context

- Preserve the low-latency English route while giving translated viewers a rolling reader option.
- **Presentation polish complete in v0.7.4:** Room Display and OBS share the same confirmed-prefix, two-line presentation policy so unstable English tail words are not exposed on projected or streamed output.
- **Optional translated-audio pilot in v0.7.5:** installed, licence-reviewed Sherpa-ONNX voices can read finalized translated cues on demand without delaying captions. Voice coverage, native-listener quality and target-hardware capacity still require explicit acceptance testing before this can become a default feature.
- **Service Context hybrid in development for v0.7.6:** operators can prepare deterministic temporary corrections from pasted notes or UTF-8 text scripts without changing Whisper in the safe default mode. Direct recognition assistance is experimental, off by default and capped at two selected terms. Deterministic Bible-reference formatting runs after recognition for all English captions, with or without notes. Optional local-model assistance and wider acceptance evidence remain future work. See [V0.7.6_SERVICE_CONTEXT_PLAN.md](V0.7.6_SERVICE_CONTEXT_PLAN.md).
- **Alpha 1 complete:** replace the single translation slot with timestamp-aligned cue revisions and bounded per-language queues that coalesce stale revisions, preserve unrelated sealed cues, rotate fairly, and expose privacy-safe cue/queue-health measurements.
- **Alpha 2 superseded after Linux evidence:** retire the two-thought Contextual and four-thought Extended waits. Responsive Context now retranslates the current stable English cue and finalises it in place; legacy settings migrate automatically. Separate `zh-Hans`/`zh-Hant` choices retain deterministic OpenCC conversion.
- Compare Responsive Context against Live and More Stable using first translated cue time, revision counts, queue pressure, and native-reader scores. Tune its debounce only from repeated reference-appliance evidence.
- Keep runtime storage bounded: on-demand Diagnostics storage accounting, rotated Church Cap logs, capped benchmark samples, clear download-size guidance, and explicit allow-listed cleanup.
- Evaluate Apache-2.0 OPUS-MT English→Chinese as an optional Chinese quality package; do not add it unless it beats SMaLL-100 + OpenCC on the reference hardware.
- Improve Farsi mixed-direction presentation and add passage-level Farsi and Traditional Chinese review gates.

Responsive Context and Chinese-script controls are implemented for controlled testing. Responsive Context is recommended for new configurations, while Live remains the lowest-delay control. Chinese naturalness and Farsi presentation still require native review.

## v0.8.x Desktop Packaging, Appliance Recovery, And Signed Releases

- Treat v0.7.4 as the completed application-security and hardening baseline and v0.7.6 as the current product/packaging baseline. v0.8 preserves the former while explicitly packaging, deferring, or disabling every accepted/development feature in the latter.
- Track the Windows x64 and Apple Silicon desktop supervisor, installer, recovery, update, signing, QA, and GitHub release work through [V0.8.0_IMPLEMENTATION.md](V0.8.0_IMPLEMENTATION.md), [CROSS_PLATFORM_ARCHITECTURE.md](CROSS_PLATFORM_ARCHITECTURE.md), and [DESKTOP_UPDATE_RELEASE_RUNBOOK.md](DESKTOP_UPDATE_RELEASE_RUNBOOK.md).
- Keep one modular monorepo: shared FastAPI/browser code, typed platform-service contracts, a source-install adapter, a packaged-supervisor adapter, and a thin Tauri host. Do not fork Windows and macOS application code.
- Develop both desktop targets against the same contracts, then build, sign, and test each on its native platform. Publish Windows, macOS, and Linux together only after all release gates pass.
- Freeze executable runtimes into the signed product (or separately signed versioned components) while keeping model weights, settings, credentials, logs, and exports in per-user storage.
- Keep the existing checksum-verified Church Cap updater and provide a matching appliance-shell path.
- Document rollback, recovery, and factory-reset procedures while keeping identity and secrets outside release folders.
- Run a repeatable test matrix across macOS, Windows CPU, Windows NVIDIA, Linux CPU, Linux NVIDIA, AlmaLinux CPU appliance, and AlmaLinux GPU appliance.
- Add diagnostics that clearly report deployment profile, CUDA readiness, audio device formats, and translation capacity.
- Review accessibility, keyboard/touch use, and small-display layouts.

## v0.9.x Public Candidate

- Freeze the operator workflow and appliance setup flow except for bug fixes.
- Complete privacy, safeguarding, translation, and accessibility documentation.
- Produce a clean migration guide from preview releases.
- Verify that desktop installs never enter appliance mode unless explicitly configured.

## v1.0.0 Criteria

- A non-technical church can install, start, recover, and update the standard app from the docs.
- A Church Cap Appliance can boot into the kiosk shell, join Wi-Fi, use the correct profile, and recover from common faults without terminal access.
- English captions are stable on recommended CPU hardware.
- Multilingual captions have clear supported-hardware guidance and fail safely when hardware is not suitable.
- The project has tests and documentation covering the supported desktop and appliance paths.
