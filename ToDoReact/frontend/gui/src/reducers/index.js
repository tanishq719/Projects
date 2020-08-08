import { combineReducers } from 'redux'
import todos from './todos'
import token from './auth'

export default combineReducers({
    todos,
    auth : token
});