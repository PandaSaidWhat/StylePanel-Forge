# StylePanel  
### Structured prompt control layer for Forge — *powered by UCP*

StylePanel is a workflow-centric extension for **Forge (Neo)**  
that introduces structured, repeatable prompt composition using a controlled injection system called **UCP (Universe Control Panel)**.

This extension is designed for:

- **Stable Diffusion 1.x**
- **SDXL**
- **Flux**

StylePanel is not just a tag list — it’s a prompt orchestration layer built for clarity, consistency, and modular control.

---

## 🚀 Why StylePanel Exists

Prompting without structure can easily become inconsistent and messy.  
StylePanel’s goal is to:

- Enforce structured visual elements
- Reduce repeated typing
- Prevent prompt drift
- Improve prompt reproducibility

UCP (Universe Control Panel) is the core — the mechanism that controls how style components are *injected* into the generation pipeline.

---

## 🧠 UCP Modes (How it Works)

StylePanel introduces three operational modes that govern how style data moves from dropdowns into Forge’s prompt pipeline.

### **1. Manual Mode — Inject Only**
- Styles populate locked preview fields.
- You must click **Inject** to transfer tags into the prompt.
- No automatic generation.
- Best for prompt purists and controlled editing.

---

### **2. Semi-Auto Mode — Assisted Composition**
- Styles populate preview, and preview becomes editable.
- The **Inject** button becomes **Generate (UCP Mode)**.
- When pressed, all prompt + preview + edits merge and generate.
- Great for hybrid workflows and live tweaking.

---

### **3. Auto Mode — Locked Pipeline**
- Styles inject automatically.
- Preview is locked.
- Everything goes straight to **Generate (raw)**.
- Useful for automated pipelines and consistent, no-drift workflows (e.g., streaming).

---

## 🔧 Features

- Structured style categories:  
  - Image Type  
  - Framing  
  - Camera  
  - Atmosphere  
  - Expression  
  - Lighting  
  - Stability

- JSON-driven configuration  
  (No core code changes required)

- Cross-model compatibility  
  Works with:
  - Stable Diffusion 1.x
  - SDXL
  - Flux

- Optional negative tag handling  
  (Where supported by the model)

- Live preview system  
  (See injected prompt components before generate)

---

## ⚠️ Flux Note

Negative tag injection is intentionally disabled in Flux mode  
because Forge does not utilize negative prompts with Flux-based models.

---

## 📁 Installation

1. Clone or download this repository.
2. Place the `StylePanel` directory inside your Forge extensions folder.
3. Restart Forge.
4. Reload the UI.

If dropdowns appear empty:
- Verify JSON placement
- Confirm correct directory structure
- Restart Forge

---

## 🧾 Compatibility

Tested with:

- Forge Neo
- SD 1.x
- SDXL
- Flux

Expected to work with most SD-based Forge setups.

---

## ❗ Notes

- Hobby project
- No guaranteed support
- Contributions, forks, and improvements are welcome

---

## 📜 License

MIT License

Use freely. Modify freely. Attribute appropriately.
