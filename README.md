# StylePanel  
### Structured Prompt Architecture for Forge  
**SD 1.x • SDXL • Flux**

StylePanel is a workflow-oriented extension for Forge (Neo) that introduces structured, repeatable prompt composition through a controlled injection system.

It is not a tag list.

It is a prompt control layer.

---

# Philosophy

Prompting often becomes inconsistent over time.

StylePanel enforces structure without removing creative flexibility.

It separates:

- Style components
- User intent
- Injection behavior
- Generation execution

You decide how structured your workflow should be.

---

# Core Architecture

StylePanel operates around a Unified Control Panel (UCP) system.

The UCP governs how style data moves from dropdown selections into Forge’s generation pipeline.

It introduces three operational modes designed for different workflow philosophies.

---

# UCP Modes

## 1. Manual Mode — Inject Only

Full user control.

- Style selections populate locked preview fields.
- Press **Inject** to transfer tags into the positive/negative prompt boxes.
- No automatic generation.
- Nothing is sent to Forge without explicit action.

Best suited for:
- Precision workflows
- Prompt purists
- Controlled iterative editing

---

## 2. Semi-Auto Mode — Assisted Composition

Structured prompting with manual refinement.

- Style selections populate preview fields.
- Preview becomes editable.
- **Inject** transforms into **Generate (UCP Mode)**.
- When pressed:
  - Prompt field content
  - Preview content
  - Manual edits
  are merged and sent to Forge's generate function.

Best suited for:
- Power users
- Hybrid control workflows
- Live stream environments

---

## 3. Auto Mode — Locked Pipeline

Fully structured generation.

- Style selections inject automatically.
- Preview fields remain locked.
- Content is sent directly to **Generate (raw)**.
- No manual interference.

Best suited for:
- Preset pipelines
- Stream automation
- Consistent visual identity workflows
- Environments where prompt drift must be avoided

---

# Feature Set

- Structured style categories  
  (Image Type, Framing, Camera, Atmosphere, Expression, Lighting, Stability)

- JSON-driven configuration  
  All styles are defined externally. No code modification required.

- Cross-model compatibility  
  Designed to function across:
  - Stable Diffusion 1.x
  - SDXL
  - Flux

- Optional negative tag handling  
  When supported by the active model.

- Live preview system  
  Clear visibility of injected prompt components.

- Stability tagging control  
  Prevents accidental prompt degradation in automated modes.

---

# Configuration

All styles are defined in JSON files.

You can:

- Add new categories
- Remove existing ones
- Modify tag behavior
- Create model-specific presets
- Build structured style ecosystems

The UI dynamically reflects the JSON structure.

No recompilation or core modification required.

---

# Design Intent

StylePanel does not replace prompting.

It:

- Reduces repetition
- Enforces structural clarity
- Prevents prompt drift
- Enables reproducible visual identity
- Supports both manual and automated workflows

Manual users retain precision.  
Auto users gain consistency.  
Stream users gain control.

---

# Installation

1. Clone or download this repository.
2. Place the `StylePanel` directory inside your Forge extensions folder.
3. Restart Forge.
4. Reload the UI.

If dropdowns appear empty:
- Verify JSON placement
- Confirm correct directory structure
- Restart Forge

---

# Compatibility

Tested with:

- Forge Neo
- Stable Diffusion 1.x
- SDXL
- Flux

Expected to function with most SD-based setups running under Forge.

---

# Project Status

This is a hobby project.

It is stable for personal and workflow use.

No guaranteed support is provided.

Issues and forks are welcome.

---

# License

MIT License.

Use freely. Modify freely. Attribute appropriately.