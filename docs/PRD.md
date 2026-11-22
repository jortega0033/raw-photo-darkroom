# RAW Photo Darkroom

## Product requirements

A photographer working offline can open a small supported digital-negative file, compare an original rendering with a developed view, adjust exposure and color, save those adjustments, and export the result. The original is held as immutable bytes. Reversing an edit or restarting the workspace restores the same look from the same recipe. The first useful demo uses an original synthetic image with inspectable pixel values.

**User flow.** Start the local darkroom, load the bundled fixture or pick a supported local file, and inspect the image dimensions and active profile. Compare neutral and edited views. Set exposure, white balance gains, and a monotone tone curve. Save or undo the edit, close and reopen the project, then export a selected recipe revision as PNG. A later batch action exports a small group to a single download with a manifest.

**Success criteria.** The bounded DNG fixture decodes and displays on a CPU with external browser requests blocked. Neutral and +1 EV renderings match the specified test pixels. The preview and PNG use the same renderer. Import, edit, reopen, and export leave the source SHA-256 unchanged. Unsupported input receives a specific error before a project or partial preview appears in the library. The exported image carries only metadata intentionally added by the tool.

**Scope.** This project implements a declared DNG profile, a basic demosaic and color pipeline, versioned recipes, and local PNG export. Broad camera support, compressed RAW, lens correction, noise reduction, custom ICC profiles, photographic color-accuracy claims, and GPU acceleration belong to later work. Synthetic scenes are enough to pass the epic. Neither a license-restricted decoder nor an online service is a required runtime dependency.

## Technical design

### Runtime and ownership

Use Python 3.12 and its standard library for import, render, storage, and PNG output. Serve static HTML, CSS, and JavaScript over 127.0.0.1. The browser displays the renderer's output and sends settings. The Python engine owns the pixel algorithm so preview and export share it. Keep engine, file parser, storage, and HTTP modules separate. Verify the desktop's actual Python and browser before the first build.

The service uses an explicit application-owned data root. Store only selected image imports, never crawl a directory. Stream each import to a capped temporary file, compute SHA-256, validate and decode, then publish to an immutable object path derived from its digest. Create a SQLite project only after the required object is available. Interrupted orphan objects can be listed and removed separately after a reachability check. Use generated project IDs and allowlisted output names. Keep the selected local source untouched, and avoid displaying original absolute paths. Render before and after at the same output size. Apply a neutral recipe for the before view and the selected revision for the after view. Both use the same algorithm.

### Supported DNG profile and error boundaries

Version the allowlisted importer profile. Start with little-endian classic TIFF, one full-resolution Bayer CFA IFD, RGGB order, contiguous uncompressed 16-bit unsigned samples, one strip, and top-left orientation. Accept even width and height of at least 2 and at most 1024 pixels each. Set an 8 MiB input cap, at most 128 entries, and a single IFD traversal. Require the DNG version declaration, dimensions and layout tags, supported CFA plane mapping, a scalar black level, and an integer white level above it. Require RowsPerStrip to cover the image and cross-check strip size against width × height × 2. For generated fixtures include the required DNG color and camera declarations and validate against the relevant Adobe specification sections. Use an original fixture generator and record the generator revision and fixture hashes.

Check offset, count, type, length, address arithmetic, and strip boundaries before allocating a pixel buffer. Decode inline and addressed TIFF values according to their type and count. Reject overlapping structural ranges or a strip whose declared size does not match the expected sample count. Return distinct invalid-format, unsupported-profile, and resource-limit errors. Reject compressed, tiled, multi-image, BigTIFF, rotated, and unsupported CFA profiles. Reject unsupported pixel or calibration operations such as a nonidentity linearization table or nonempty opcode lists at this milestone. Round-trip preservation of arbitrary TIFF or DNG tags is outside the profile. Skip EXIF, GPS, MakerNote, embedded thumbnails and camera-identity metadata rather than traversing or exporting them. Never print or expose those values in logs, errors, or reports. The DNG tag and layout definitions come from Adobe rather than any decoder's defaults. [Adobe DNG Specification 1.7.1.0](https://helpx.adobe.com/content/dam/help/en/camera-raw/digital-negative/jcr_content/root/content/flex/items/position/position-par/download_section_733958301/download-1/DNG_Spec_1_7_1_0.pdf)

### Rendering contract

1. Compute each normalized mosaic sample as (raw − black)/(white − black). Clamp black underflow and white overflow to the documented normalized sensor interval. Sensor saturation statistics come from this stage.
2. Convert the RGGB mosaic to three linear camera-space channels with bilinear interpolation. A sample's own channel stays intact. At red or blue sites average the available orthogonal green neighbors and available diagonal neighbors for the opposite chroma. At green sites average the matching neighbors on the axis where each missing color occurs. Use only in-bounds neighbors, with fixed ordering and normalization by their count. The even minimum 2 by 2 profile guarantees a sample for each required interpolation.
3. Apply finite per-channel white-balance gains and linear exposure multiplier 2^EV. Set bounds of 0.25–4 for gains and −3 to +3 EV in validated quarter-stop steps. The changes remain in linear light.
4. Use a named, versioned profile to map camera space to linear sRGB. For the original fixture use a declared synthetic profile with identity transform and unit starting gains. For one additional authored calibrated fixture, stage and document an explicit camera-to-linear-sRGB matrix and verify neutral and color swatches. Treat matrix selection or inversion as a separate documented calibration decision. Decline unknown calibrated sources instead of applying a convenient matrix to arbitrary camera encodings.
5. Apply the selected monotone piecewise-linear tone curve. Fix the extreme input and output endpoints at zero and one. Validate ordered finite control points with a small upper bound, apply the documented input clamp before lookup, then encode linear values using the standard sRGB transfer curve. Convert to bytes once using floor(255v + 0.5), with v clamped to [0, 1]. Use the same full-resolution source-space algorithm in preview and export. If preview is resized, make that resize explicit and compare test pixels at 1:1. [W3C sRGB transfer function](https://www.w3.org/TR/css-color-4/#predefined-sRGB)

Use fixed processing order and avoid rounding intermediate channels. Version the algorithm and color profile with the recipe. Compare output pixels across runs on a pinned runtime and separately report tolerance-based comparisons across environments. Browser users can use labeled controls, step through edits by keyboard, and compare clipping in text as well as in the image. Show rejected and pending states. Gate async preview updates by recipe revision so an old render does not replace a newer edit.

### Recipes, export, and recovery

A project holds the source digest, importer profile, recipe schema and algorithm versions, and an ordered immutable list of committed revisions. Store scalar adjustments and control-point data in SQLite. Commit a new revision against the expected current revision in one transaction. A stale edit yields an explicit conflict, preserves the user's draft, and can be reapplied to the latest revision after review. Undo and redo move a pointer between valid revisions. A new edit after undo discards the redo path from normal navigation while prior committed records can remain addressable for already-requested exports. Record original, committed, displayed, and exported revisions separately.

Export an RGB PNG without source metadata. Use explicit dimensions, standard sRGB signaling, a fixed encoder and compression setting on the pinned runtime. Record the source digest, recipe digest, algorithm version, image dimensions, and output SHA-256 in the batch manifest. Reuse the same renderer invocation at full resolution. Give outputs generated safe names. Bound batches to 10 revisions with one CPU job at a time, cap temporary output, and isolate work by job ID. Prepare outputs in a job-owned scratch area and expose a batch archive only once all requested items and its manifest are validated. Cancellation and failure clean job-owned partial files without affecting source, recipes, or completed exports. An available batch can be retried at the same frozen revision list.

## Deterministic fixtures and checks

| Fixture | Expected observation |
|---|---|
| Constant-color RGGB image | With black 64, white 1088, R samples 576, G samples 320 and B samples 192, normalized linear RGB is (0.5, 0.25, 0.125) everywhere after bilinear demosaic. At neutral exposure, synthetic identity profile and identity curve, the quantized RGB is (188, 137, 99). At +1 EV the output is (255, 188, 137). Verify corners and interior. |
| Nonuniform mosaic patch | Use a 6 by 6 fixture and center red at (2,2) with black-relative value 512, its four orthogonal green neighbors at 128, 256, 384 and 512, and four diagonal blue neighbors at 64, 128, 192 and 256. With the same white-minus-black range of 1024, center linear RGB is (0.5, 0.3125, 0.15625) and final RGB is (188, 152, 110). This catches wrong neighbor types and rounding before averaging. |
| Recipe history | Neutral → +1 EV → undo → restart returns the neutral pixel. Redo returns the +1 EV pixel. The imported object and user's original file retain the same digest. |
| Unsupported inputs | A declared compressed input, short sample strip, oversized dimensions, unknown pixel profile, and invalid white/black range all fail with specific messages. The app exposes no partial project from a rejected file. |
| Export fidelity and privacy | Decode the export with an independent PNG reader or browser at 1:1 and compare expected pixels. Check dimensions, expected PNG chunk types, immutable source digest, revision identity, and absence of copied EXIF and GPS fields. |

The pixel numbers above were calculated from the fixture contract and sRGB transfer function. A future implementation must make the generated DNG and verify its own output. If rawpy and its native dependencies can be staged from an approved source, pin the toolchain and record its exact decode settings. Compare raw sample layout first, then compare selected rendered observables with method-aware tolerances. A different demosaic, white-balance policy, camera matrix, or tone default can create legitimate pixel differences. The original fixture and independent arithmetic path are the mandatory offline oracle. Report timings from the actual host before claiming support for larger files or longer batches.

## Epic E31 · Develop and export a digital negative offline

Deliver a small but complete darkroom whose declared DNG subset can enter through a validated local import, render with a reproducible recipe, reopen after restart, and export inspectable PNGs. The epic passes when the included fixtures and pipeline checks succeed, unsupported inputs receive actionable feedback, and a clean offline demo shows source, preview, persisted settings, and export.

| Ticket | Dependencies | Remaining estimate |
|---|---|---:|
| E31-1 Generate fixtures and validate raw import | — | 2–3 h |
| E31-2 Demosaic and display a reproducible preview | E31-1 | 3–4 h |
| E31-3 Save and revisit edits | E31-2 API contract | 2–4 h |
| E31-4 Apply color controls and inspect clipping | E31-2, E31-3 | 3–5 h |
| E31-5 Verify full-resolution PNG and batch export | E31-3, E31-4 | 3–5 h |
| E31-6 Run clean offline acceptance and measure resource use | E31-1 through E31-5 | 2–3 h |

**Remaining effort.** 15–24 engineering hours including verification and integration. E31-1 and E31-2 together form the first thin workflow. After the E31-2 input, render, and result contracts freeze, E31-3 can develop against fixture previews while E31-2 finishes the engine. E31-4 integrations follow both. E31-5 owns export encoding and tests. E31-6 owns the cross-layer gate.

### E31-1 · Generate fixtures and validate raw import

Build the original fixture generator, immutable import path, and strict profile decoder. Provide both positive and negative fixtures with known versions and origin. Accept the declared constant fixture and recover every sample value exactly. Return distinct unsupported-profile and malformed-file errors. An interrupted or rejected import must have no library row. Verify with readback of the decoded samples, source digests, and import state.

### E31-2 · Demosaic and display a reproducible preview

Implement normalization, neighborhood interpolation, neutral synthetic conversion and sRGB quantization. Wire one imported project into a browser view with a visible profile and 1:1 inspection. Verify constant pixels at corners and interior, and the nonuniform patch at its center. Make startup and preview work from a clean checkout with external network requests blocked.

### E31-3 · Save and revisit edits

Implement recipe validation, immutable revisions, undo, redo, restart, and stale-write conflict handling. Bind labeled controls and make one exposure adjustment visible end to end. Verify neutral → +1 EV → undo → restart → redo with exact reference pixels. Check that two windows do not silently overwrite each other's committed revisions. Preserve stale edits as a draft before offering a resolution.

### E31-4 · Apply color controls and inspect clipping

Add white-balance gains, exposure, monotone curve, bounded calibrated-profile support for one authored fixture, and explicit clipping diagnostics. Verify neutral profile values, a synthetic neutral swatch with calibrated gains, and monotonic curve endpoints. Reject unknown profile IDs and invalid curves. Verify an older asynchronous preview response cannot replace the current selected revision. Record clipping counts separately from sensor saturation.

### E31-5 · Verify full-resolution PNG and batch export

Export a frozen recipe revision as a full-resolution PNG. Add a bounded batch, generated filenames, manifests, and cancellation cleanup. Verify expected colors with an independent decoder and inspect the emitted chunk allowlist. Repeat an export on the same runtime and compare image hashes. Check an injected writer failure leaves no downloadable partial archive and does not alter earlier completed outputs.

### E31-6 · Run clean offline acceptance and measure resource use

Validate the full import → compare → edit → restart → export sequence in the browser. Repeat with network requests blocked. Run fixture and metadata checks, invalid-profile cases, and import or export interruptions on a disposable application-owned data root. Measure import, render, and export time for pinned fixtures, peak RSS where available, input bytes, and output pixels on the actual host. Record the exact runtime and algorithm revisions. Treat optional external-reference comparisons as additional evidence after source and tool verification.

[Official project inspiration](https://docs.google.com/document/d/1R5MyfVvn033KoXZXgXP65qRAXnhcjtVvO_VF7IxUZaA/edit?tab=t.ef9a30wzb1z5)
