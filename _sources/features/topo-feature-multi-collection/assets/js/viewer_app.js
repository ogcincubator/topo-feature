import {
    buildMaps, buildSolidGeometry, buildSolidEdgeLines,
    createSolidMesh, createVertexMarkers,
    getFeatures, getTopologyFeatureCounts,
} from './topo_geometry.js';

// ─── UI messages ──────────────────────────────────────────────────────────────

const LOADING_MESSAGE = 'Loading model...<br>Use the mouse to rotate and zoom';
const NO_SOLIDS_MESSAGE = '<span style="color: #ff6666;">No solids found in this file.</span>';
const LOAD_ERROR_MESSAGE = '<span style="color: #ff6666;">Error loading model:</span><br>';

// ─── Viewer app factory ───────────────────────────────────────────────────────

/**
 * Initialises the viewer application: builds the UI, wires control events,
 * loads the initial model, and starts the animation loop.
 *
 * @param {Object} sceneObjects - The result of initScene() containing a scene, gridHelper, and animate.
 * @param {Object} viewerControls - The result of initControls() containing solid state and camera helpers.
 * @param {string} [initialModel] - Path to the model JSON to load on startup (used when modelSelectId is absent).
 * @param {string} [modelSelectId] - ID of the <select> element for model switching. When provided, the
 *                                   select's current value is used as the initial model and change events
 *                                   trigger reloads.
 */
export function initViewerApp({ sceneObjects, viewerControls, initialModel, modelSelectId }) {
    const { scene, gridHelper, animate } = sceneObjects;
    const {
        solidMeshes, solidEdges, solidVertices,
        clearScene, fitCameraToModel, resetCamera,
    } = viewerControls;

    // ─── UI elements ──────────────────────────────────────────────────────────

    /**
     * A collection of UI elements used for interaction in the application.
     *
     * @property {HTMLElement} info - The HTML element providing information to the user.
     * @property {HTMLElement} modelLabel - The label element displaying the current model name.
     * @property {HTMLElement} solidsControls - The container element for solid object controls.
     * @property {HTMLElement} toggleVertices - The checkbox for toggling vertex visibility.
     * @property {HTMLElement} toggleWireframe - The checkbox for toggling wireframe mode.
     * @property {HTMLElement} toggleEdges - The checkbox for toggling edge visibility.
     * @property {HTMLElement} resetCamera - The button to reset the camera view.
     * @property {HTMLElement} toggleGrid - The button for toggling the grid.
     */
    const ui = {
        info: document.getElementById('info'),
        modelLabel: document.getElementById('modelLabel'),
        solidsControls: document.getElementById('solidsControls'),
        toggleVertices: document.getElementById('toggleVertices'),
        toggleWireframe: document.getElementById('toggleWireframe'),
        toggleEdges: document.getElementById('toggleEdges'),
        resetCamera: document.getElementById('resetCamera'),
        toggleGrid: document.getElementById('toggleGrid'),
        modelSelect: modelSelectId ? document.getElementById(modelSelectId) : null,
    };

    const model = { name: 'Loading...' };
    ui.modelLabel.textContent = `Model:${model.name}`;

    // ─── Model loading ─────────────────────────────────────────────────────────

    /**
     * Loads a 3D model from a specified file, parses its content, and processes the model data.
     *
     * @param {string} filename - The path to the file containing the 3D model data.
     * @return {Promise<void>} A promise that resolves once the model is successfully loaded and processed.
     */
    async function _loadModel(filename) {
        try {
            _showLoadingState();

            const response = await fetch(filename);
            const data = await response.json();

            _updateModelMetadata(data, filename);

            const topologyMaps = buildMaps(data);
            const solids = getFeatures(data.solids);

            if (solids.length === 0) {
                ui.info.innerHTML = NO_SOLIDS_MESSAGE;
                return;
            }

            const featureCounts = getTopologyFeatureCounts(data);

            solids.forEach((solid, index) => {
                _addSolidToScene(solid, index, topologyMaps);
            });

            const modelBounds = fitCameraToModel();

            ui.info.innerHTML = _buildModelInfoHtml(filename.split('/').pop(), featureCounts, solids.length, modelBounds.size);
        } catch (error) {
            console.error('Error loading model:', error);
            ui.info.innerHTML = LOAD_ERROR_MESSAGE + error.message;
        }
    }

    function _showLoadingState() {
        ui.info.innerHTML = LOADING_MESSAGE;
        clearScene();
        ui.solidsControls.innerHTML = '<strong>Solids:</strong>';
        ui.toggleVertices.checked = false;
    }

    function _updateModelMetadata(data, filename) {
        model.name = data.surveyTitle || data.name || filename.split('/').pop();
        ui.modelLabel.textContent = `Model:${model.name}`;
    }

    /**
     * Adds a solid object to the scene by generating its geometry, mesh, edges, and vertex markers,
     * and then integrating them into the scene.
     *
     * @param {Object} solid - The solid object to be added to the scene.
     * @param {number} index - The index of the solid, used for colour selection and labelling.
     * @param {Object} topologyMaps - The topological maps required for constructing the solid geometry.
     * @return {void}
     */
    function _addSolidToScene(solid, index, topologyMaps) {
        const {pointMap, edgeMap, ringMap, faceMap, shellMap} = topologyMaps;

        const {geometry, faceCount} = buildSolidGeometry(
            solid, shellMap, faceMap, ringMap, edgeMap, pointMap
        );

        const mesh = createSolidMesh(solid, index, geometry);
        const edges = buildSolidEdgeLines(solid, shellMap, faceMap, ringMap, edgeMap, pointMap);
        const verticesGroup = createVertexMarkers(geometry);
        const solidName = mesh.userData.solidName;

        scene.add(mesh);
        scene.add(edges);
        scene.add(verticesGroup);

        solidMeshes.push(mesh);
        solidEdges.push(edges);
        solidVertices.push(verticesGroup);

        mesh.material.wireframe = ui.toggleWireframe.checked;
        edges.visible = ui.toggleEdges.checked;
        verticesGroup.visible = false;

        _addSolidVisibilityControl(mesh, edges, solidName, faceCount);
    }

    /**
     * Creates and appends a per-solid visibility checkbox to the solids controls panel.
     *
     * @param {THREE.Mesh} mesh - The solid mesh.
     * @param {THREE.LineSegments} edges - The edge lines for the solid.
     * @param {string} solidName - Label text for the checkbox.
     * @param {number} faceCount - Face count shown in the label.
     * @return {void}
     */
    function _addSolidVisibilityControl(mesh, edges, solidName, faceCount) {
        const label = document.createElement('label');
        const checkbox = document.createElement('input');

        checkbox.type = 'checkbox';
        checkbox.checked = true;
        checkbox.addEventListener('change', event => {
            mesh.visible = event.target.checked;
            edges.visible = event.target.checked && ui.toggleEdges.checked;
        });

        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(` ${solidName} (${faceCount} faces)`));
        ui.solidsControls.appendChild(label);
    }

    /**
     * Generates an HTML string containing detailed information about a 3D model.
     *
     * @param {string} filename - The name of the file representing the 3D model.
     * @param {Object} featureCounts - Point, edge, face, and shell counts.
     * @param {number} solidCount - The total number of solids in the model.
     * @param {Object} boundsSize - Bounding box dimensions {x, y, z}.
     * @return {string} An HTML string describing the 3D model details.
     */
    function _buildModelInfoHtml(filename, featureCounts, solidCount, boundsSize) {
        return `<b>${filename}</b><br>` +
            `Points: ${featureCounts.points.toLocaleString()}<br>` +
            `Edges: ${featureCounts.edges.toLocaleString()}<br>` +
            `Faces: ${featureCounts.faces.toLocaleString()}<br>` +
            `Shells: ${featureCounts.shells.toLocaleString()}<br>` +
            `Solids: ${solidCount.toLocaleString()}<br>` +
            `Bounds: ${boundsSize.x.toFixed(3)} × ${boundsSize.y.toFixed(3)} × ${boundsSize.z.toFixed(3)}<br><br>` +
            `<small>Mouse: rotate/zoom<br>Axes: X(red) Y(green) Z(blue)</small>`;
    }

    // ─── Event wiring ──────────────────────────────────────────────────────────

    if (modelSelectId) {
        _loadModel(ui.modelSelect.value);
        ui.modelSelect.addEventListener('change', e => _loadModel(e.target.value));
    } else {
        _loadModel(initialModel);
    }

    ui.toggleWireframe.addEventListener('change', e => {
        solidMeshes.forEach(m => { m.material.wireframe = e.target.checked; });
    });
    ui.toggleEdges.addEventListener('change', e => {
        solidEdges.forEach(edges => { edges.visible = e.target.checked; });
    });
    ui.toggleVertices.addEventListener('change', e => {
        solidVertices.forEach(v => { v.visible = e.target.checked; });
    });
    ui.resetCamera.addEventListener('click', resetCamera);
    ui.toggleGrid.addEventListener('click', () => {
        gridHelper.visible = !gridHelper.visible;
    });

    animate();
}
