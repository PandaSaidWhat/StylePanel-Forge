import gradio as gr
import json
import os
from modules import script_callbacks, shared, scripts

# Paths to your style folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
STYLES_ROOT = os.path.join(BASE_DIR, "styles")

NONE = "— (none)"

def on_ui_settings():
    section = ("ucp", "Universe Control Panel")
    shared.opts.add_option("ucp_operation_mode", shared.OptionInfo(
        "Manual", 
        "UCP Mode: Manual (inject only), Semi-Auto (editable), Auto (locked)", 
        gr.Radio, 
        {"choices": ["Manual", "Semi-Automatic", "Automatic"]}, 
        section=section
    ))

def _get_full_data(arch: str, category: str, is_neg: bool = False):
    """Retrieves style data from JSON files based on architecture and category."""
    cat_map = {
        "ImageType": "imagetype", "Framing": "framing", "CameraPosition": "camera_position", 
        "Atmosphere": "mood", "Expression": "expression", "Lighting": "lighting", "Stability": "stability"
    }
    filename = cat_map.get(category, category.lower())
    if is_neg:
        filename += "_neg"
        
    file_path = os.path.join(STYLES_ROOT, arch, f"{filename}.json")
    if not os.path.exists(file_path): return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

def get_choices(arch: str, category: str):
    """Returns a list of available keys for a given category."""
    data = _get_full_data(arch, category)
    return [NONE] + [k for k in data.keys() if k]

def get_value(data, key):
    """Extracts the prompt string from the style data."""
    if not key or key == NONE or key.startswith("---"): return ""
    val = data.get(key, "")
    if isinstance(val, dict): return val.get("prompt", "").strip()
    return val.strip() if isinstance(val, str) else ""

class UCP_Engine(scripts.Script):
    def title(self):
        return "Universe Control Panel Engine"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion("🚀 UNIVERSE CONTROL PANEL", open=True):
            with gr.Column():
                with gr.Row():
                    arch = gr.Radio(choices=["SD", "SDXL", "Flux"], value="Flux", label="Architecture Mode") 
                    reload_btn = gr.Button("🔄 Reload JSON files", variant="secondary")
                
                with gr.Row():
                    it = gr.Dropdown(label="Image Type", choices=get_choices("Flux", "ImageType"), value=NONE)
                    f = gr.Dropdown(label="Framing", choices=get_choices("Flux", "Framing"), value=NONE)
                    cp = gr.Dropdown(label="Camera Position", choices=get_choices("Flux", "CameraPosition"), value=NONE)
                
                with gr.Row():
                    a = gr.Dropdown(label="Atmosphere", choices=get_choices("Flux", "Atmosphere"), value=NONE)
                    ex = gr.Dropdown(label="Expression", choices=get_choices("Flux", "Expression"), value=NONE)
                    l = gr.Dropdown(label="Lighting", choices=get_choices("Flux", "Lighting"), value=NONE)
                                
                with gr.Row():
                    s = gr.Dropdown(label="Stability", choices=get_choices("Flux", "Stability"), value=[], multiselect=True)
                    

                pp = gr.Textbox(label="Positive Preview", lines=2, elem_id="ucp_positive_preview")
                nt = gr.Checkbox(label="Enable Negative Tags", value=False)
                np = gr.Textbox(label="Negative Preview", lines=2, visible=False, elem_id="ucp_negative_preview")

                warning_box = gr.HTML("", elem_id="ucp_warning_box")
                action_btn = gr.Button("Inject Tags", variant="primary", elem_id="ucp_action_btn")

        input_list = [arch, it, f, cp, a, ex, l, s, nt]
        output_list = [it, f, cp, a, ex, l, s, nt, pp, np, action_btn, warning_box]
        
        for comp in input_list:
            comp.change(fn=self.update_ui_state, inputs=input_list, outputs=output_list)
        
        reload_btn.click(fn=self.update_ui_state, inputs=input_list, outputs=output_list)

        # Handle tag injection (Manual mode) and trigger generate
        action_btn.click(None, None, None, _js=r"""
        () => {
            const btn = document.getElementById('ucp_action_btn');
            const isManual = btn && btn.innerText.includes("Manual");
            
            if (isManual) {
                const posContent = document.querySelector('#ucp_positive_preview textarea').value;
                const negContent = document.querySelector('#ucp_negative_preview textarea').value;
                const mainPos = document.querySelector('#txt2img_prompt textarea');
                const mainNeg = document.querySelector('#txt2img_neg_prompt textarea');
                
                if (mainPos && posContent) {
                    mainPos.value = (mainPos.value.trim() ? mainPos.value.trim() + ", " : "") + posContent;
                    mainPos.dispatchEvent(new Event('input', {bubbles:true}));
                }
                if (mainNeg && negContent && mainNeg.offsetParent !== null) {
                    mainNeg.value = (mainNeg.value.trim() ? mainNeg.value.trim() + ", " : "") + negContent;
                    mainNeg.dispatchEvent(new Event('input', {bubbles:true}));
                }
            }

            const genBtn = document.getElementById('txt2img_generate');
            if (genBtn) genBtn.click();
        }""")

        return [arch, it, f, cp, a, ex, l, s, nt, pp, np]

    def update_ui_state(self, arch, cur_it, cur_f, cur_cp, cur_a, cur_ex, cur_l, cur_s, use_neg):
        """Updates the UI components based on the selected architecture and values."""
        # Load data for all categories
        data_it = _get_full_data(arch, "ImageType")
        data_f = _get_full_data(arch, "Framing")
        data_cp = _get_full_data(arch, "CameraPosition")
        data_a = _get_full_data(arch, "Atmosphere")
        data_ex = _get_full_data(arch, "Expression")
        data_l = _get_full_data(arch, "Lighting")
        data_s = _get_full_data(arch, "Stability")

        # Validate current selections against loaded data
        it_v = cur_it if cur_it in data_it else NONE
        f_v = cur_f if cur_f in data_f else NONE
        cp_v = cur_cp if cur_cp in data_cp else NONE
        a_v = cur_a if cur_a in data_a else NONE
        ex_v = cur_ex if cur_ex in data_ex else NONE
        l_v = cur_l if cur_l in data_l else NONE
        s_v = [x for x in cur_s if x in data_s]

        # 1. Collect all active selections for cross-referencing conflicts
        current_selections = [
            ("Image Type", it_v, data_it),
            ("Framing", f_v, data_f),
            ("Camera Position", cp_v, data_cp),
            ("Atmosphere", a_v, data_a),
            ("Expression", ex_v, data_ex),
            ("Lighting", l_v, data_l)
        ]
        
        # Add Stability selections individually (handling multi-select)
        for val in s_v:
            current_selections.append(("Stability", val, data_s))

        # 2. Comprehensive conflict detection loop
        found_conflicts = []
        for label, val, data in current_selections:
            if val == NONE or not val: 
                continue
            
            item_data = data.get(val, {})
            if isinstance(item_data, dict) and "conflicts" in item_data:
                conflict_list = item_data["conflicts"]
                
                for other_label, other_val, _ in current_selections:
                    if other_val != NONE and other_val != "" and other_val != val:
                        if other_val in conflict_list:
                            # Color logic:
                            # Choice = Orange (#ff9a33)
                            # Label = White/Silver (#e0e0e0)
                            # "conflicts with" = Yellow (#ffdb58)
                            msg = (f"<span style='color: #ff9a33;'><b>{val}</b></span> "
                                   f"<span style='color: #e0e0e0;'>({label})</span> "
                                   f"<span style='color: #ffdb58;'>conflicts with</span> "
                                   f"<span style='color: #ff9a33;'><b>{other_val}</b></span> "
                                   f"<span style='color: #e0e0e0;'>({other_label})</span>")
                            
                            if msg not in found_conflicts:
                                found_conflicts.append(msg)

        # Generate warning HTML with a slightly darker border for better contrast
        warning_html = ""
        if found_conflicts:
            warning_html = (
                f'<div style="color: #e0e0e0; background: rgba(245, 158, 11, 0.1); '
                f'padding: 12px; border-radius: 8px; border: 1px solid #d97706; line-height: 1.6;">'
                f'<b style="color: #ffdb58; font-size: 1.1em;">⚠️ Logic Warning:</b><br>'
                f'{"<br>".join(found_conflicts)}</div>'
            )

        # Build positive prompt preview
        pos_parts = [get_value(data_it, it_v), get_value(data_f, f_v), get_value(data_cp, cp_v), 
                     get_value(data_a, a_v), get_value(data_ex, ex_v), get_value(data_l, l_v)]
        for key in s_v: 
            pos_parts.append(get_value(data_s, key))
        pos = ", ".join(filter(None, pos_parts))
        
        # Build negative prompt preview (disabled for Flux)
        neg = ""
        if use_neg and arch != "Flux":
            neg_parts = []
            # Single-select categories
            for cat, cur_val in [("ImageType", it_v), ("Framing", f_v), ("CameraPosition", cp_v),
                                ("Atmosphere", a_v), ("Expression", ex_v), ("Lighting", l_v)]:
                neg_data = _get_full_data(arch, cat, is_neg=True)
                neg_parts.append(get_value(neg_data, cur_val))

            # Multi-select category: Stability
            neg_data_s = _get_full_data(arch, "Stability", is_neg=True)
            for key in s_v:
                neg_parts.append(get_value(neg_data_s, key))

            neg = ", ".join(filter(None, neg_parts))

        mode = shared.opts.data.get("ucp_operation_mode", "Manual")
        btn_label = "🚀 GENERATE (UCP Mode)" if mode != "Manual" else "Inject Tags (Manual)"

        return (
            gr.update(choices=[NONE] + list(data_it.keys()), value=it_v),
            gr.update(choices=[NONE] + list(data_f.keys()), value=f_v),
            gr.update(choices=[NONE] + list(data_cp.keys()), value=cp_v),
            gr.update(choices=[NONE] + list(data_a.keys()), value=a_v),
            gr.update(choices=[NONE] + list(data_ex.keys()), value=ex_v),
            gr.update(choices=[NONE] + list(data_l.keys()), value=l_v),
            gr.update(choices=[NONE] + list(data_s.keys()), value=s_v),
            gr.update(interactive=(arch != "Flux"), value=use_neg if arch != "Flux" else False),
            gr.update(value=pos, interactive=(mode == "Semi-Automatic")),
            gr.update(value=neg, visible=(use_neg and arch != "Flux")),
            gr.update(value=btn_label),
            gr.update(value=warning_html)
        )

    def process(self, p, arch, it, f, cp, a, ex, l, s, nt, pp, np):
        """Main processing function to inject tags into the prompt list."""
        mode = shared.opts.data.get("ucp_operation_mode", "Manual")
        
        if mode in ["Semi-Automatic", "Automatic"]:
            active_tags = pp.strip()
            if active_tags:
                print(f"\n--- [UCP ACTIVE] ---")
                print(f"Injecting into {arch}: {active_tags}")
                
                # Update main prompt (for metadata)
                p.prompt = f"{p.prompt}, {active_tags}" if p.prompt.strip() else active_tags
                
                # Update batch prompts for Forge Neo
                if hasattr(p, 'all_prompts'):
                    p.all_prompts = [f"{prompt}, {active_tags}" if prompt.strip() else active_tags for prompt in p.all_prompts]
                print(f"--- [UCP INJECTED] ---\n")

            # Handle negative tag injection for non-Flux architectures
            if nt and arch != "Flux" and np.strip():
                active_neg = np.strip()
                p.negative_prompt = f"{p.negative_prompt}, {active_neg}" if p.negative_prompt.strip() else active_neg
                if hasattr(p, 'all_neg_prompts'):
                    p.all_neg_prompts = [f"{neg}, {active_neg}" if neg.strip() else active_neg for neg in p.all_neg_prompts]

script_callbacks.on_ui_settings(on_ui_settings)