import { GET_BAGS, DELETE_BAG } from '../actions/types.js';

const initialState = {
    bags: []
}

export default function(state = initialState, action) {
    switch(action.type){
        case GET_BAGS:
            return {
                ...state,
                bags: action.payload
            };
        case DELETE_BAG:
            return {
                ...state,
                bags: state.bags.filter(bag => bag.id !== action.payload)
            }
        default:
            return state;
    }
}