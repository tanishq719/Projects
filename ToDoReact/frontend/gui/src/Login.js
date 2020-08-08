import React, { Component } from 'react'
import {connect} from 'react-redux'
import PropTypes from 'prop-types'
import {loginUser} from './actions/auth'

export class Login extends Component {
    state = {
        username: '',
        password: ''
    };

    static propTypes = {
        loginUser: PropTypes.func.isRequired
    };

    onChange = e => this.setState({[e.target.name]: e.target.value});

    onSubmit = e => {
        e.preventDefault();
        const {username, password} = this.state;
        const user = {username,password};
        this.props.loginUser(user);
    }
    render() {
        const {username,password} = this.state;
        return (
            <div className="container col-md-4 mx-auto" style={{ marginTop: '5%' }}>
                <div className="jumbotron" style={{ opacity: '0.95', backgroundColor:'#e3e5e6'}}>
                    <div className="jumbotron-content">
                        <h1 style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif', textAlign: 'center' }}>
                            Login here</h1>
                        <form id="loginForm" onSubmit={this.onSubmit} >
                            <div className="form-row">
                                <div className="form-group col-md-12 mx-auto">
                                    <label htmlFor="inputEmail4">Email</label>
                                    <input onChange={this.onChange} type="email" className="form-control" id="inputEmail4" placeholder="Email" name="username" value={username}/>
                                </div>
                                <div className="form-group col-md-12 mx-auto">
                                    <label htmlFor="inputPassword4">Password</label>
                                    <input onChange={this.onChange} type="password" className="form-control" id="inputPassword4" placeholder="Password" name="password" value={password}/>
                                </div>
                            </div>
                            <div style={{ textAlign: 'center' }}>
                                <button type="submit" className="btn btn-primary" id="loginbutton">Sign in</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}

export default connect(null,{loginUser})(Login)
