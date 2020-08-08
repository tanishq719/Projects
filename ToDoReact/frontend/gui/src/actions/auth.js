import axios from 'axios'

import {LOGIN,ADD_USER} from './types'

const config = {
    headers: {
        'Content-Type': 'application/json'
    }
}

//LOGIN
export const loginUser = (user) => dispatch =>{
    axios.post('http://127.0.0.1:8000/api/auth/login/',user)
    .then(res=>{
        console.log(res.data.token)
        // console.log(res.data)
        dispatch({
            type: LOGIN,
            token: String(res.data.token),
            loggedin: res.data.loggedin?true:false
        })
    })
    .catch(err=>console.log(err));
}

export const addUser = (cred) => (dispatch, getState) => {

    const token = getState().auth.token;

    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }
    axios.post("http://127.0.0.1:8000/api/auth/addUser/", cred, config)
        .then(res => {
            dispatch({
                type: ADD_USER,
                payload: res.data
            })
        })
        .catch(err => console.log(err))

}