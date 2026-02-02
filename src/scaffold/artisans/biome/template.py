import json
from typing import Dict, Any


def forge_biome_html(gnosis: Dict[str, Any]) -> str:
    """
    Forges the HTML5/WebGL container for the Codebase Biome.
    Injects the Gnostic Data directly into the JavaScript scope.
    """

    json_payload = json.dumps(gnosis)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Scaffold Biome: {gnosis['project']}</title>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #050505; font-family: 'Segoe UI', sans-serif; }}
        #ui {
    position: absolute; top: 10px; left: 10px; color: #00ffcc; 
            background: rgba(0, 10, 20, 0.85); padding: 15px; border: 1px solid #00ffcc;
            border-radius: 4px; pointer-events: none; min-width: 250px;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
            backdrop-filter: blur(5px);
        }
        h1 {margin: 0 0 10px 0; font-size: 18px; text-transform: uppercase; letter-spacing: 2px; }
        .stat {font - size: 12px; color: #aaa; margin-bottom: 4px; }
        .value {color: #fff; font-weight: bold; }
        .hot {color: #ff3366; } .cold {color: #00ccff; }
        #tooltip {
    position: absolute; display: none; background: rgba(0, 0, 0, 0.9);
            border: 1px solid #fff; padding: 10px; color: #fff; font-size: 12px;
            pointer-events: none; z-index: 100; white-space: pre;
        }
        #controls {
    position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 20px;
        }
        .btn {
    background: rgba(0,0,0,0.5); border: 1px solid #555; color: #eee;
            padding: 8px 16px; cursor: pointer; text-transform: uppercase;
            font-size: 10px; letter-spacing: 1px; transition: all 0.3s;
        }
        .btn:hover {background: #00ffcc; color: #000; border-color: #00ffcc; }
    </style>
    <!-- Celestial Libraries -->
    <script type="importmap">
      {{
        "imports": {{
          "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        }}
      }}
    </script>
</head>
<body>
    <div id="ui">
        <h1>Gnostic Biome</h1>
        <div class="stat">Project: <span class="value">{gnosis['project']}</span></div>
        <div class="stat">Scriptures: <span class="value">{gnosis['stats']['total_files']}</span></div>
        <div class="stat">Max Complexity (Height): <span class="value">{gnosis['stats']['max_complexity']}</span></div>
        <div class="stat">Max Churn (Heat): <span class="value hot">{gnosis['stats']['max_churn']}</span></div>
        <hr style="border-color: #333; margin: 10px 0;">
        <div id="hover-info">Hover over a structure...</div>
    </div>

    <div id="tooltip"></div>

    <div id="controls">
        <button class="btn" id="btn-orbit">Orbit</button>
        <button class="btn" id="btn-reset">Reset View</button>
    </div>

    <script type="module">
        import * as THREE from 'three';
        import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
        import {{ UnrealBloomPass }} from 'three/addons/postprocessing/UnrealBloomPass.js';
        import {{ EffectComposer }} from 'three/addons/postprocessing/EffectComposer.js';
        import {{ RenderPass }} from 'three/addons/postprocessing/RenderPass.js';

        // --- 1. THE GNOSTIC INJECTION ---
        const DATA = {json_payload};

        // --- 2. THE SCENE SETUP ---
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x050505, 0.002);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
        camera.position.set(100, 100, 100);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.toneMapping = THREE.ReinhardToneMapping;
        document.body.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // --- 3. THE LUMINOUS RENDERER (BLOOM) ---
        const renderScene = new RenderPass(scene, camera);
        const bloomPass = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85);
        bloomPass.threshold = 0.2;
        bloomPass.strength = 1.2; // Glowing Intensity
        bloomPass.radius = 0.5;

        const composer = new EffectComposer(renderer);
        composer.addPass(renderScene);
        composer.addPass(bloomPass);

        // --- 4. THE CITY FORGE (LAYOUT ENGINE) ---
        // Simple Grid Layout for V1.
        // Files are blocks. Directories are districts.

        const materials = {{
            base: new THREE.MeshStandardMaterial({{ color: 0x444444, roughness: 0.2, metalness: 0.8 }}),
            wire: new THREE.LineBasicMaterial({{ color: 0x00ffff, transparent: true, opacity: 0.1 }})
        }};

        // Group by folder
        const districts = {{}};
        DATA.cells.forEach(cell => {{
            if (!districts[cell.folder]) districts[cell.folder] = [];
            districts[cell.folder].push(cell);
        }});

        const group = new THREE.Group();
        let districtX = 0;
        let districtZ = 0;
        const spacing = 5;
        const districtGap = 20;

        // Heat Gradient (Blue -> Red)
        function getHeatColor(churn, maxChurn) {{
            const t = Math.min(1.0, churn / (maxChurn || 1));
            // Lerp from Blue (0x00ccff) to Red (0xff0055)
            const r = Math.floor(0 + t * 255);
            const g = Math.floor(204 - t * 204);
            const b = Math.floor(255 - t * 170);
            return new THREE.Color(`rgb(${{r}},${{g}},${{b}})`);
        }}

        Object.keys(districts).forEach((folderName, dIdx) => {{
            const files = districts[folderName];

            // Layout files in a grid within the district
            const side = Math.ceil(Math.sqrt(files.length));

            files.forEach((file, fIdx) => {{
                const lx = fIdx % side;
                const lz = Math.floor(fIdx / side);

                // Height = Complexity
                // Normalize complexity (1 to 50)
                const height = Math.max(1, Math.min(50, file.metrics.complexity * 2));

                const geometry = new THREE.BoxGeometry(3, height, 3);
                geometry.translate(0, height / 2, 0); // Pivot at bottom

                const color = getHeatColor(file.metrics.churn, DATA.stats.max_churn);
                const material = new THREE.MeshStandardMaterial({{
                    color: color,
                    emissive: color,
                    emissiveIntensity: file.metrics.churn > 0 ? 0.4 : 0.05, // Hot files glow
                    roughness: 0.1,
                    metalness: 0.5
                }});

                const mesh = new THREE.Mesh(geometry, material);

                // Position
                mesh.position.set(
                    districtX + (lx * spacing),
                    0,
                    districtZ + (lz * spacing)
                );

                // Attach Gnosis to Mesh for Raycaster
                mesh.userData = {{ ...file }};

                group.add(mesh);
            }});

            // Move to next district position (Spiral or simple line for V1)
            districtX += (side * spacing) + districtGap;
            if (districtX > 150) {{
                districtX = 0;
                districtZ += 60;
            }}
        }});

        // Center the city
        new THREE.Box3().setFromObject(group).getCenter(group.position).multiplyScalar(-1);
        scene.add(group);

        // --- 5. THE LIGHT OF TRUTH ---
        const ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(-1, 1.75, 1);
        scene.add(dirLight);

        // Grid Floor
        const gridHelper = new THREE.GridHelper(500, 50, 0x00ffcc, 0x222222);
        scene.add(gridHelper);

        // --- 6. THE RAYCASTER (INTERACTION) ---
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        const infoPanel = document.getElementById('hover-info');

        function onMouseMove(event) {{
            mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

            tooltip.style.left = event.clientX + 10 + 'px';
            tooltip.style.top = event.clientY + 10 + 'px';
        }}
        window.addEventListener('mousemove', onMouseMove, false);

        let hoveredObj = null;

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();

            // Raycasting logic
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(group.children);

            if (intersects.length > 0) {{
                const obj = intersects[0].object;
                if (hoveredObj !== obj) {{
                    // Reset previous
                    if (hoveredObj) hoveredObj.material.emissiveIntensity = hoveredObj.userData.baseEmissive || 0.1;

                    hoveredObj = obj;
                    hoveredObj.userData.baseEmissive = hoveredObj.material.emissiveIntensity;
                    hoveredObj.material.emissiveIntensity = 1.0; // Flash on hover

                    const meta = obj.userData;
                    const info = `
                        <strong style="color:#fff; font-size:14px">${{meta.name}}</strong><br>
                        <span style="color:#00ffcc">${{meta.path}}</span><br>
                        <hr style="border-color:#555">
                        Complexity: <span style="color:${{meta.metrics.complexity > 10 ? '#ff3366' : '#fff'}}">${{meta.metrics.complexity}}</span><br>
                        Churn (Heat): <span style="color:${{meta.metrics.churn > 10 ? '#ff3366' : '#fff'}}">${{meta.metrics.churn}}</span><br>
                        Last Author: ${{meta.metrics.last_author}}<br>
                        Size: ${{meta.metrics.size}} B
                    `;
                    tooltip.innerHTML = info;
                    tooltip.style.display = 'block';

                    infoPanel.innerHTML = `GAZE: ${{meta.path}} | HEAT: ${{meta.metrics.churn}} | ELEVATION: ${{meta.metrics.complexity}}`;
                }}
            }} else {{
                if (hoveredObj) {{
                    hoveredObj.material.emissiveIntensity = hoveredObj.userData.baseEmissive || 0.1;
                    hoveredObj = null;
                    tooltip.style.display = 'none';
                    infoPanel.innerHTML = "Hover over a structure...";
                }}
            }}

            composer.render();
        }}

        // --- 7. AUTO-ORBIT (CINEMATIC) ---
        let autoOrbit = true;
        controls.autoRotate = true;
        controls.autoRotateSpeed = 1.0;

        document.getElementById('btn-orbit').addEventListener('click', () => {{
            autoOrbit = !autoOrbit;
            controls.autoRotate = autoOrbit;
        }});

        document.getElementById('btn-reset').addEventListener('click', () => {{
            controls.reset();
        }});

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            composer.setSize(window.innerWidth, window.innerHeight);
        }});

        animate();
    </script>
</body>
</html>
    """