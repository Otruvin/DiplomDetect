import axios from 'axios';
import { createMessage, returnErrors } from './messages';
import { tokenConfig } from './auth';

import { GET_BAGS, DELETE_BAG } from './types';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// GET ALL BAGS
export const getBags = () => (dispatch, getState) => {
    axios.get('/lost/api/detected/', tokenConfig(getState))
        .then(res => {
            dispatch({
                type: GET_BAGS,
                payload: res.data
            });
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}

// DELETE BAG
export const deleteBag = id => (dispatch, getState) => {
    axios.delete(`/lost/api/detected/${id}/`, tokenConfig(getState))
        .then(res => {
            dispatch(createMessage({ objectDeleted: 'Object Deleted' }));
            dispatch({
                type: DELETE_BAG,
                payload: id
            });
        }).catch(err => console.log(err));
}