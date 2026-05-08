import * as THREE from 'three';

// ─── Camera fitting constants ─────────────────────────────────────────────────

const CAMERA_DISTANCE_SCALE = 2;
const CAMERA_OFFSET_SCALE = 0.7;
const CAMERA_NEAR_SCALE = 0.001;
const CAMERA_FAR_SCALE = 100;

// ─── Controls factory ─────────────────────────────────────────────────────────

/**
 * Initialises solid-state arrays and camera-control helpers bound to the given scene objects.
 * Call once per viewer after initScene().
 *
 * solidMeshes, solidEdges, and solidVertices are stable array references — they are cleared
 * in-place (array.length = 0) rather than reassigned, so destructured references remain valid.
 *
 * initialCameraPosition / initialCameraTarget are kept private; use resetCamera() instead.
 *
 * @param {{ scene: THREE.Scene, camera: THREE.PerspectiveCamera, controls: OrbitControls }} sceneObjects
 * @return {{ solidMeshes, solidEdges, solidVertices, clearScene, fitCameraToModel, resetCamera }}
 */
export function initControls({ scene, camera, controls }) {

    // ─── Solid state ──────────────────────────────────────────────────────────

    const solidMeshes = [];
    const solidEdges = [];
    const solidVertices = [];
    let initialCameraPosition = null;
    let initialCameraTarget = null;

    // ─── Scene management ─────────────────────────────────────────────────────

    /**
     * Clears all elements related to the 3D scene, including meshes, edges, and vertices.
     * Frees up memory by disposing of geometry and materials associated with the elements.
     *
     * @return {void} This method does not return a value.
     */
    function clearScene() {
        solidMeshes.forEach(m => { scene.remove(m); m.geometry.dispose(); m.material.dispose(); });
        solidEdges.forEach(e => { scene.remove(e); e.geometry.dispose(); });
        solidVertices.forEach(g => { scene.remove(g); });
        solidMeshes.length = 0;
        solidEdges.length = 0;
        solidVertices.length = 0;
    }

    // ─── Camera control ───────────────────────────────────────────────────────

    /**
     * Adjusts the camera's position, near and far planes, and controls' target to fit all given solid meshes within the view.
     * This method calculates the bounding box of all solid meshes, determines the center and size of the box, and updates the camera and controls accordingly.
     *
     * @return {{center: THREE.Vector3, size: THREE.Vector3}} An object containing the computed center and size of the bounding box that encompasses all solid meshes.
     */
    function fitCameraToModel() {
        const box = new THREE.Box3();

        solidMeshes.forEach(mesh => {
            box.expandByObject(mesh);
        });

        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDimension = Math.max(size.x, size.y, size.z);
        const distance = maxDimension * CAMERA_DISTANCE_SCALE;

        camera.position.set(
            center.x - distance * CAMERA_OFFSET_SCALE,
            center.y - distance * CAMERA_OFFSET_SCALE,
            center.z + distance * CAMERA_OFFSET_SCALE
        );

        camera.near = distance * CAMERA_NEAR_SCALE;
        camera.far = distance * CAMERA_FAR_SCALE;
        camera.updateProjectionMatrix();

        controls.target.copy(center);
        controls.update();

        initialCameraPosition = camera.position.clone();
        initialCameraTarget = controls.target.clone();

        return {center, size};
    }

    /**
     * Restores the camera to the position and target recorded by the last fitCameraToModel() call.
     *
     * @return {void}
     */
    function resetCamera() {
        if (initialCameraPosition) {
            camera.position.copy(initialCameraPosition);
            controls.target.copy(initialCameraTarget);
            controls.update();
        }
    }

    return {
        solidMeshes,
        solidEdges,
        solidVertices,
        clearScene,
        fitCameraToModel,
        resetCamera,
    };
}
