import React, { Component } from 'react'
import {connect} from 'react-redux'
import PropTypes from 'prop-types'
import {addUser} from './actions/auth'

export class AddUser extends Component {
    state = {
        email: '',
        password: '',
        toggleForm: false
    }

    static propTypes = {
        addUser : PropTypes.func.isRequired,
    }

    onChange = e => this.setState({[e.target.name]: e.target.value});

    onSubmit = e => {
        e.preventDefault();
        const {email,password} = this.state;
        const listI = {email,password}
        this.props.addUser(listI)
        this.setState({toggleForm:!this.state.toggleForm})
        // this.props.toggleForm = !this.props.toggleForm
    }

    componentDidMount(){
        this.setState({toggleForm :this.props.toggleForm})
        // this.setState({listId:this.props.listId})
    }

    render() {
        const {email,password} = this.state
        return (
            <div>
            {this.state.toggleForm?
            (<div className="container col-md-4 mx-auto">
                <h1 style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif', textAlign: 'center' }}>
                Customer Registeration</h1>
            <form id="loginForm" onSubmit={this.onSubmit} >
            <div className="form-row">
                <div className="form-group col-md-12 mx-auto">
                    <label htmlFor="inputEmail4">Email</label>
                    <input onChange={this.onChange} type="email" className="form-control" id="inputEmail4" placeholder="Email" name="email" value={email}/>
                </div>
                <div className="form-group col-md-12 mx-auto">
                    <label htmlFor="inputPassword4">Password</label>
                    <input onChange={this.onChange} type="password" className="form-control" id="inputPassword4" placeholder="Password" name="password" value={password}/>
                </div>
            </div>
            <div style={{ textAlign: 'center' }}>
                <button type="submit" className="btn btn-primary" id="loginbutton">Register</button>
            </div>
        </form></div>):<span></span>}</div>
        )
    }
}

export default connect(null,{addUser})(AddUser)