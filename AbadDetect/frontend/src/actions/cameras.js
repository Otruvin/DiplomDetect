import axios from 'axios';
import { createMessage, returnErrors } from './messages';
import { tokenConfig } from './auth';

import {
    GET_CAMERAS,
    ADD_CAMERA,
    DELETE_CAMERA,
    UPDATE_CAMERA
} from './types';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

//GET ALL CAMERAS
export const getCameras = () => (dispatch, getState) => {
    axios.get('lost/api/cameras', tokenConfig(getState))
        .then(res => {
            dispatch({
                type: GET_CAMERAS,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

//DELETE CAMERA
export const deleteCamera = id => (dispatch, getState) => {
    axios.delete(`/lost/api/cameras/${id}/`, tokenConfig(getState))
        .then(res => {
            dispatch(createMessage({ cameraDeleted: 'Camera deleted'}));
            dispatch({
                type: DELETE_CAMERA,
                payload: id
            });
        }).catch(err => console.log(err));
}

//ADD_CAMERA
export const addCamera = (camera) => (dispatch, getState) => {
    camera.user = getState().auth.user.id;
    axios.post('/lost/api/cameras/', camera, tokenConfig(getState))
        .then(res => {
            dispatch(createMessage({ cameraAdded: 'Camera added'}));
            dispatch({
                type: ADD_CAMERA, 
                payload: res.data
            });
        }).catch(err => console.log(err));
}

//UPDATE CAMERA
export const updateCamera = (camera) => (dispatch, getState) => {
    camera.user = getState().auth.user.id;
    axios.put(`/lost/api/cameras/${camera.id}/`, camera, tokenConfig(getState))
        .then(res => {
            dispatch(createMessage({ cameraUpdated: 'Camera updated' }));
            dispatch({
                type: UPDATE_CAMERA,
                payload: res.data
            });
        }).catch(err => console.log(err));
}