import { combineReducers } from 'redux';
import bags from './bags';
import auth from './auth';
import errors from './errors';
import messages from './messages';
import cameras from './cameras'

export default combineReducers({
    bags,
    errors,
    auth,
    messages,
    cameras
});