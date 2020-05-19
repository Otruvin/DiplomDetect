import {
    GET_CAMERAS,
    DELETE_CAMERA,
    UPDATE_CAMERA,
    ADD_CAMERA
} from '../actions/types';

const initialState = {
    cameras: []
}

export default function(state = initialState, action) {
    switch(action.type) {
        case GET_CAMERAS:
            return {
                ...state,
                cameras: action.payload
            };
        case DELETE_CAMERA:
            return {
                ...state,
                cameras: state.cameras.filter(camera => camera.id !== action.payload)
            };
        case UPDATE_CAMERA:
            return {
                ...state,
                cameras: [...state.cameras.filter(camera => camera.id !== action.payload.id), action.payload]
            };
        case ADD_CAMERA:
            return {
                ...state,
                cameras: [...state.cameras, action.payload],
            };
        default:
            return state;
    }
}