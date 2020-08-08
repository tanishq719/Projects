import axios from 'axios'

import { GET_TODOS, ADD_TODOS, DELETE_TODOS } from './types'

const config = {
    headers: {
        'Content-Type': 'application/json'
    }
}

// GET TODOS
export const getTodos = () => (dispatch, getState) => {

    const token = getState().auth.token;

    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }
    axios.post("http://127.0.0.1:8000/api/todo/getTodos/", {}, config)
        .then(res => {
            dispatch({
                type: GET_TODOS,
                payload: res.data
            })
        })
        .catch(err => console.log(err))

}

export const addTodoList = (listI) => (dispatch, getState) => {

    const token = getState().auth.token;

    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }
    axios.post("http://127.0.0.1:8000/api/todo/addTodoList/", listI, config)
        .then(res => {
            dispatch({
                type: ADD_TODOS,
                payload: res.data.todos
            })
        })
        .catch(err => console.log(err))

}

export const deleteTodo = (ids) => (dispatch, getState) => {

    const token = getState().auth.token;

    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }
    axios.post("http://127.0.0.1:8000/api/todo/deleteTodo/", ids, config)
        .then(res => {
            dispatch({
                type: DELETE_TODOS,
                payload: res.data.todos
            })
        })
        .catch(err => console.log(err))

}
