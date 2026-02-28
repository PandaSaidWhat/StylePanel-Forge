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
    data = _get_full_data(arch, category)
    return [NONE] + [k for k in data.keys() if k]

def get_value(data, key):
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
                    reload_btn = gr.Button("🔄 Reload JSON Files", variant="secondary")
                
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
                    nt = gr.Checkbox(label="Enable Negative Tags", value=False)

                pp = gr.Textbox(label="Positive Preview", lines=2, elem_id="ucp_positive_preview")
                np = gr.Textbox(label="Negative Preview", lines=2, visible=False, elem_id="ucp_negative_preview")

                warning_box = gr.HTML("", elem_id="ucp_warning_box")
                action_btn = gr.Button("Inject Tags", variant="primary", elem_id="ucp_action_btn")

        input_list = [arch, it, f, cp, a, ex, l, s, nt]
        output_list = [it, f, cp, a, ex, l, s, nt, pp, np, action_btn, warning_box]
        
        for comp in input_list:
            comp.change(fn=self.update_ui_state, inputs=input_list, outputs=output_list)
        
        reload_btn.click(fn=self.update_ui_state, inputs=input_list, outputs=output_list)

        action_btn.click(None, None, None, _js=r"""
        () => {
            const posContent = document.querySelector('#ucp_positive_preview textarea').value;
            const negContent = document.querySelector('#ucp_negative_preview textarea').value;
            const mainPos = document.querySelector('#txt2img_prompt textarea');
            const mainNeg = document.querySelector('#txt2img_neg_prompt textarea');
            
            if (mainPos && posContent) {
                mainPos.value = (mainPos.value.trim() ? mainPos.value.trim() + ", " : "") + posContent;
                mainPos.dispatchEvent(new Event('input', {bubbles:true}));
            }
            if (mainNeg && negContent) {
                mainNeg.value = (mainNeg.value.trim() ? mainNeg.value.trim() + ", " : "") + negContent;
                mainNeg.dispatchEvent(new Event('input', {bubbles:true}));
            }

            const btn = document.getElementById('ucp_action_btn');
            if (btn && btn.innerText.includes("GENERATE")) {
                setTimeout(() => {
                    const genBtn = document.getElementById('txt2img_generate');
                    if (genBtn) genBtn.click();
                }, 100);
            }
        }""")

        return [arch, it, f, cp, a, ex, l, s, nt, pp, np]

    def update_ui_state(self, arch, cur_it, cur_f, cur_cp, cur_a, cur_ex, cur_l, cur_s, use_neg):
        data_it = _get_full_data(arch, "ImageType")
        data_f = _get_full_data(arch, "Framing")
        data_cp = _get_full_data(arch, "CameraPosition")
        data_a = _get_full_data(arch, "Atmosphere")
        data_ex = _get_full_data(arch, "Expression")
        data_l = _get_full_data(arch, "Lighting")
        data_s = _get_full_data(arch, "Stability")

        it_v = cur_it if cur_it in data_it else NONE
        f_v = cur_f if cur_f in data_f else NONE
        cp_v = cur_cp if cur_cp in data_cp else NONE
        a_v = cur_a if cur_a in data_a else NONE
        ex_v = cur_ex if cur_ex in data_ex else NONE
        l_v = cur_l if cur_l in data_l else NONE
        s_v = [x for x in cur_s if x in data_s]

                # --- Global conflict check (all categories vs all categories) ---
        selected = {
            "ImageType": it_v,
            "Framing": f_v,
            "CameraPosition": cp_v,
            "Atmosphere": a_v,
            "Expression": ex_v,
            "Lighting": l_v,
        }

        selected_stability = list(s_v)

        # All selected keys (fast membership checks)
        selected_keys = set(v for v in selected.values() if v and v != NONE)
        selected_keys.update(x for x in selected_stability if x and x != NONE)

        data_map = {
            "ImageType": data_it,
            "Framing": data_f,
            "CameraPosition": data_cp,
            "Atmosphere": data_a,
            "Expression": data_ex,
            "Lighting": data_l,
            "Stability": data_s,
        }

        found_conflicts = []

        def check_item_conflicts(cat_name: str, key_name: str):
            if not key_name or key_name == NONE:
                return
            item = data_map.get(cat_name, {}).get(key_name, {})
            if not isinstance(item, dict) or "conflicts" not in item:
                return

            conflicts = item.get("conflicts", [])
            if isinstance(conflicts, str):
                conflicts = [conflicts]
            elif not isinstance(conflicts, list):
                conflicts = []

            for c in conflicts:
                if c in selected_keys:
                    found_conflicts.append(
                        f"<b>{cat_name}: {key_name}</b> conflicts with <b>{c}</b>"
                    )

        for cat, key in selected.items():
            check_item_conflicts(cat, key)

        for st_key in selected_stability:
            check_item_conflicts("Stability", st_key)

        warning_html = ""
        if found_conflicts:
            warning_html = f'<div style="color: #d97706; background: rgba(245, 158, 11, 0.1); padding: 12px; border-radius: 8px; border: 1px solid #f59e0b;"><b>Logic Warning:</b><br>{"<br>".join(found_conflicts)}</div>'

        pos_parts = [get_value(data_it, it_v), get_value(data_f, f_v), get_value(data_cp, cp_v), get_value(data_a, a_v), get_value(data_ex, ex_v), get_value(data_l, l_v)]
        for key in s_v: pos_parts.append(get_value(data_s, key))
        pos = ", ".join(filter(None, pos_parts))
        
        neg = ""
        if use_neg and arch != "Flux":
            neg_parts = []
            for cat, cur_val in [("ImageType", it_v), ("Framing", f_v), ("CameraPosition", cp_v)]:
                neg_data = _get_full_data(arch, cat, is_neg=True)
                neg_parts.append(get_value(neg_data, cur_val))
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
            gr.update(value=neg, visible=use_neg),
            gr.update(value=btn_label),
            gr.update(value=warning_html)
        )

    def process(self, p, arch, it, f, cp, a, ex, l, s, nt, pp, np):
        mode = shared.opts.data.get("ucp_operation_mode", "Manual")
        if mode in ["Semi-Automatic", "Automatic"]:
            # HER ER LOGGINGEN TIL CMD-VINDUET:
            if pp.strip():
                print(f"[UCP] Active Prompt: {pp.strip()}")
                p.prompt = f"{p.prompt}, {pp.strip()}" if p.prompt.strip() else pp.strip()
            
            if nt and arch != "Flux" and np.strip():
                p.negative_prompt = f"{p.negative_prompt}, {np.strip()}" if p.negative_prompt.strip() else np.strip()


script_callbacks.on_ui_settings(on_ui_settings)
