import * as THREE from 'three';
import { OrbitControls } from 'three/addons/OrbitControls.js';

// ─── Scene constants ──────────────────────────────────────────────────────────

const SCENE_BACKGROUND_COLOR = 0xadb1b1;
const CAMERA_FOV = 75;
const CAMERA_INITIAL_NEAR = 0.1;
const CAMERA_INITIAL_FAR = 10000;
const CAMERA_INITIAL_X = -2;
const CAMERA_INITIAL_Y = -2;
const CAMERA_INITIAL_Z = 2;
const CONTROLS_DAMPING_FACTOR = 0.05;
const LIGHT_COLOR = 0xffffff;
const AMBIENT_LIGHT_INTENSITY = 0.5;
const KEY_LIGHT_INTENSITY = 0.8;
const FILL_LIGHT_INTENSITY = 0.3;
const LIGHT_DISTANCE = 100;
const GRID_SIZE = 100;
const GRID_DIVISIONS = 20;
const GRID_CENTER_COLOR = 0x444444;
const GRID_LINE_COLOR = 0x222222;
const AXES_SIZE = 1;
const GRID_ROTATION_X = Math.PI / 2;
const CAMERA_UP_X = 0;
const CAMERA_UP_Y = 0;
const CAMERA_UP_Z = 1;

// ─── Scene factory ────────────────────────────────────────────────────────────

/**
 * Initialises the Three.js scene, camera, renderer, controls, lights, grid, and axes helper.
 * Call once per viewer with the desired canvas dimensions.
 *
 * @param {number}      width     - Canvas width in pixels.
 * @param {number}      height    - Canvas height in pixels.
 * @param {HTMLElement} container - DOM element to which the renderer canvas is appended.
 * @return {{ scene, camera, renderer, controls, gridHelper, axesHelper, animate }}
 */
export function initScene(width, height, container) {

    // ─── Scene ────────────────────────────────────────────────────────────────

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(SCENE_BACKGROUND_COLOR);

    // ─── Camera ───────────────────────────────────────────────────────────────

    const camera = new THREE.PerspectiveCamera(CAMERA_FOV, width / height, CAMERA_INITIAL_NEAR, CAMERA_INITIAL_FAR);
    camera.up.set(CAMERA_UP_X, CAMERA_UP_Y, CAMERA_UP_Z); // Z-up coordinate system
    camera.position.set(CAMERA_INITIAL_X, CAMERA_INITIAL_Y, CAMERA_INITIAL_Z);

    // ─── Renderer ─────────────────────────────────────────────────────────────

    // WebGL renderer with antialiasing; canvas is appended to the container.
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // ─── Controls ─────────────────────────────────────────────────────────────

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = CONTROLS_DAMPING_FACTOR;

    // ─── Lights ───────────────────────────────────────────────────────────────

    const ambientLight = new THREE.AmbientLight(LIGHT_COLOR, AMBIENT_LIGHT_INTENSITY);
    scene.add(ambientLight);

    const directionalLight1 = new THREE.DirectionalLight(LIGHT_COLOR, KEY_LIGHT_INTENSITY);
    directionalLight1.position.set(LIGHT_DISTANCE, LIGHT_DISTANCE, LIGHT_DISTANCE);
    scene.add(directionalLight1);

    const directionalLight2 = new THREE.DirectionalLight(LIGHT_COLOR, FILL_LIGHT_INTENSITY);
    directionalLight2.position.set(-LIGHT_DISTANCE, -LIGHT_DISTANCE, -LIGHT_DISTANCE);
    scene.add(directionalLight2);

    const directionalLight3 = new THREE.DirectionalLight(LIGHT_COLOR, FILL_LIGHT_INTENSITY);
    directionalLight3.position.set(0, -LIGHT_DISTANCE, 0);
    scene.add(directionalLight3);

    // ─── Grid and axes ────────────────────────────────────────────────────────

    const gridHelper = new THREE.GridHelper(GRID_SIZE, GRID_DIVISIONS, GRID_CENTER_COLOR, GRID_LINE_COLOR);
    gridHelper.rotation.x = GRID_ROTATION_X; // rotate XZ plane to XY for Z-up coordinate system
    gridHelper.visible = false;
    scene.add(gridHelper);

    const axesHelper = new THREE.AxesHelper(AXES_SIZE);
    scene.add(axesHelper);

    // ─── Animation loop ───────────────────────────────────────────────────────

    /**
     * Animates the scene by updating controls and rendering the scene with the camera.
     * Uses requestAnimationFrame for a continuous render loop.
     *
     * @return {void}
     */
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }

        // ─── Resize handler ───────────────────────────────────────────────────────

    /**
     * Updates the camera aspect ratio and renderer size to match the current window dimensions.
     * Wire to window 'resize' events in responsive (full-window) entry points.
     *
     * @return {void}
     */
    function handleResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    return { scene, camera, renderer, controls, gridHelper, axesHelper, animate, handleResize };
}
