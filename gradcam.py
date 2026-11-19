import io
import base64
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


def generate_gradcam(model, input_tensor, original_pil, pred_idx, is_healthy=False):
    """
    Lightweight Grad-CAM + Automatic Severity % (No OpenCV/Matplotlib needed)
    """
    activations = []
    gradients = []

    target_layer = model.layer4[-1]

    def forward_hook(module, inp, out):
        activations.append(out.detach())

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0].detach())

    fh = target_layer.register_forward_hook(forward_hook)
    bh = target_layer.register_full_backward_hook(backward_hook)

    try:
        model.zero_grad()
        input_tensor = input_tensor.clone().detach().requires_grad_(True)
        output = model(input_tensor)
        score = output[0, pred_idx]
        score.backward()

        acts = activations[0][0]   # [C, H, W]
        grads = gradients[0][0]    # [C, H, W]

        weights = grads.mean(dim=(1, 2), keepdim=True)
        cam = (weights * acts).sum(dim=0)
        cam = F.relu(cam).cpu().numpy()

        # Normalize 0 to 1
        cam_min, cam_max = cam.min(), cam.max()
        if cam_max - cam_min > 1e-8:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = np.zeros_like(cam)

        # --- Automatic Severity % ---
        if is_healthy:
            severity_pct = 0.0
            severity_level = {"en": "Healthy", "hi": "स्वस्थ"}
        else:
            # Pixels with high disease activation (> 0.5 threshold)
            severity_pct = round(float((cam > 0.5).mean() * 100), 1)
            if severity_pct < 15:
                severity_level = {"en": "Mild", "hi": "हल्का संक्रमण"}
            elif severity_pct < 40:
                severity_level = {"en": "Moderate", "hi": "मध्यम संक्रमण"}
            else:
                severity_level = {"en": "Severe", "hi": "गंभीर संक्रमण"}

        # --- Pure NumPy + PIL Heatmap Overlay (224x224 for fast transfer) ---
        base_img = original_pil.convert("RGB").resize((224, 224))
        cam_img = Image.fromarray(np.uint8(cam * 255)).resize((224, 224), Image.BILINEAR)
        cam_arr = np.array(cam_img, dtype=np.float32) / 255.0

        # Simple Jet-like Red/Yellow/Blue colormap
        r = np.clip(1.5 - np.abs(4 * cam_arr - 3), 0, 1)
        g = np.clip(1.5 - np.abs(4 * cam_arr - 2), 0, 1)
        b = np.clip(1.5 - np.abs(4 * cam_arr - 1), 0, 1)
        heatmap = np.stack([r, g, b], axis=-1) * 255.0

        orig_arr = np.array(base_img, dtype=np.float32)
        blended = np.uint8(0.6 * orig_arr + 0.4 * heatmap)

        buf = io.BytesIO()
        Image.fromarray(blended).save(buf, format="JPEG", quality=85)
        b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")

        return {
            "gradcam_image": f"data:image/jpeg;base64,{b64_img}",
            "severity_pct": severity_pct,
            "severity_level": severity_level
        }
    finally:
        fh.remove()
        bh.remove()
        model.zero_grad()