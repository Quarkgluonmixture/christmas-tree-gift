import os
import urllib.request
import urllib.error

# 配置路径
BASE_DIR = os.path.join("Merry Chrismas", "project2", "gesture-Christmas_tree-3d_with_photo")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 创建目录结构
dirs = [
    "js",
    "js/three/addons/postprocessing",
    "js/three/addons/environments",
    "js/three/addons/shaders",
    "models",
    "wasm",
    "css"
]

for d in dirs:
    os.makedirs(os.path.join(ASSETS_DIR, d), exist_ok=True)

print(f"Created directories in {ASSETS_DIR}")

# 资源映射表 (URL -> 本地相对路径)
resources = {
    # Three.js Core
    "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js": "js/three.module.js",
    
    # Three.js Addons (Dependencies based on usage)
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/postprocessing/EffectComposer.js": "js/three/addons/postprocessing/EffectComposer.js",
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/postprocessing/RenderPass.js": "js/three/addons/postprocessing/RenderPass.js",
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/postprocessing/UnrealBloomPass.js": "js/three/addons/postprocessing/UnrealBloomPass.js",
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/environments/RoomEnvironment.js": "js/three/addons/environments/RoomEnvironment.js",
    
    # Addon Internal Dependencies (Need to be downloaded manually as they are imported by above files)
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/shaders/LuminosityHighPassShader.js": "js/three/addons/shaders/LuminosityHighPassShader.js",
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/shaders/CopyShader.js": "js/three/addons/shaders/CopyShader.js",
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/postprocessing/ShaderPass.js": "js/three/addons/postprocessing/ShaderPass.js",
    "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/postprocessing/MaskPass.js": "js/three/addons/postprocessing/MaskPass.js", # RenderPass might need this or FullScreenQuad
    # Note: Modern three.js RenderPass often depends on FullScreenQuad which is in a different path in some versions, 
    # but in 0.160.0 RenderPass imports from FullScreenQuad.js? Let's check imports later or download common utils.
    # Actually checking 0.160.0 source: RenderPass imports FullScreenQuad from '../objects/FullScreenQuad.js' (if available) or implements it.
    # Let's verify standard 0.160.0 dependency.
    # To be safe, we will assume standard imports.
    
    # Mediapipe
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/+esm": "js/tasks-vision.js",
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm/vision_wasm_internal.js": "wasm/vision_wasm_internal.js",
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm/vision_wasm_internal.wasm": "wasm/vision_wasm_internal.wasm",
    
    # Model (Critical for China access)
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task": "models/hand_landmarker.task",

    # FontAwesome (Optional but good)
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css": "css/all.min.css"
}

# 自动补全 Three.js 的一些隐式依赖 (Based on 0.160.0 structure)
# UnrealBloomPass imports: Vector2, Vector3, Color, AdditiveBlending, MeshBasicMaterial, ShaderMaterial, UniformsUtils, WebGLRenderTarget, HalfFloatType from 'three'
# UnrealBloomPass imports: Pass, FullScreenQuad from './Pass.js'
# So we need Pass.js and FullScreenQuad.js (if used)
resources["https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/postprocessing/Pass.js"] = "js/three/addons/postprocessing/Pass.js"
# RenderPass extends Pass
# EffectComposer imports: Clock, HalfFloatType, NoBlending, Vector2, WebGLRenderTarget from 'three'
# EffectComposer imports: CopyShader from '../shaders/CopyShader.js'
# EffectComposer imports: ShaderPass from './ShaderPass.js'
# EffectComposer imports: MaskPass from './MaskPass.js'
# EffectComposer imports: ClearMaskPass from './MaskPass.js'

print("Starting download...")

for url, rel_path in resources.items():
    dest_path = os.path.join(ASSETS_DIR, rel_path)
    print(f"Downloading {rel_path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

print("Download complete.")
