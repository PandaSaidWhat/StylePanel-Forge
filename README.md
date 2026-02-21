# StylePanel
### Structured Prompt Architecture for Forge  
#### Powered by UCP (Universe Control Panel)

StylePanel is a workflow-centric extension for **Forge (Neo)** that introduces structured, repeatable prompt composition through a controlled injection architecture called **UCP**.

Designed for:

- Stable Diffusion 1.x  
- SDXL  
- Flux  

StylePanel is not a tag list.

It is a prompt control layer.

---

## Why StylePanel Exists

Prompting without structure eventually becomes inconsistent.

StylePanel enforces clarity without limiting creativity.

It provides:

- Structured visual components  
- Reduced repetition  
- Controlled injection behavior  
- Reproducible generation workflows  

UCP (Universe Control Panel) is the engine that governs how style components move into Forge’s generation pipeline.

---

## UCP Mode Configuration

UCP execution mode is configured globally in the Forge Settings panel.

Upon first installation, StylePanel defaults to:

Manual Mode (Inject Only)

Only the **Inject** button is available by default.

To enable other modes, navigate to:

Forge → Settings → StylePanel (UCP Mode)

Available options:

- Manual (Inject Only)
- Semi-Automatic (Editable)
- Automatic (Locked)

The selected mode persists across sessions.

---

## UCP Modes (Behavior)

Once configured, UCP controls how style components are injected into the generation pipeline.

### 1. Manual — Inject Only

- Styles populate locked preview fields  
- You must click **Inject** to transfer tags into the prompt  
- No automatic generation occurs  
- Safest and most controlled workflow  

---

### 2. Semi-Automatic — Editable Preview

- Preview fields become editable  
- **Inject** becomes **Generate (UCP Mode)**  
- Preview + prompt merge before generation  
- Ideal for hybrid workflows and live tweaking  

---

### 3. Automatic — Locked Pipeline

- Injection happens automatically  
- Preview fields are locked  
- Generation executes immediately  
- Designed for automation and consistent output workflows  

---

## Feature Set

- Structured style categories  
  - Image Type  
  - Framing  
  - Camera  
  - Atmosphere  
  - Expression  
  - Lighting  
  - Stability  

- JSON-driven configuration  
- Cross-model compatibility  
- Live preview injection system  
- Clean separation between style logic and generation execution  

---

## Flux Compatibility Note

Negative prompt injection is intentionally disabled in **Flux mode**, as Forge does not utilize negative prompts with Flux models.

---

## Installation

1. Clone or download this repository  
2. Place the `StylePanel` directory inside your Forge extensions folder  
3. Restart Forge  
4. Reload the UI  

If dropdowns appear empty:
- Verify JSON structure  
- Confirm correct folder placement  
- Restart Forge  

---

## Compatibility

Tested with:

- Forge Neo  
- Stable Diffusion 1.x  
- SDXL  
- Flux  

---

## Philosophy

Structure does not remove creativity.

It enables consistency.

---

## License

MIT
