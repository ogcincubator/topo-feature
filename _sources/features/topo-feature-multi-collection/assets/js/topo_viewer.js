import { initScene } from './viewer_scene.js';
import { initControls } from './viewer_controls.js';
import { initViewerApp } from './viewer_app.js';

const params = new URLSearchParams(window.location.search);
const exampleName = params.get("example");

if (!exampleName) {
  throw new Error("Missing ?example=filename.json parameter");
}

const dataUrl = new URL(`../examples/${exampleName}`, window.location.href);

// // ─── Viewer dimensions ────────────────────────────────────────────────────────
//
// const VIEWER_WIDTH = 500;
// const VIEWER_HEIGHT = 500;

// ─── Initialisation ───────────────────────────────────────────────────────────

const sceneObjects = initScene(window.innerWidth, window.innerHeight, document.getElementById('sceneContainer'));
const viewerControls = initControls(sceneObjects);

initViewerApp({
    sceneObjects,
    viewerControls,
    initialModel: dataUrl.href,
});

window.addEventListener('resize', sceneObjects.handleResize);
