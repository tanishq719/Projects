import { LOGIN} from '../actions/types'

const initialState = {
    token: localStorage.getItem('token'),
    loggedin: false
}

export default function (state = initialState, action) {
    switch (action.type) {
        case LOGIN:
            {
                console.log(action.state)
                localStorage.setItem('token', action.token)
                return {
                    ...state,
                    token: action.token,
                    loggedin: action.loggedin
                }
            }
        default: return state;
    }
}

