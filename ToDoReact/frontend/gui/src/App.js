import React, {Component} from 'react'; 
import Login from './Login'
import ToDo from './ToDo'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import './App.css';

export class App extends Component {
  static propTypes = {
    auth:PropTypes.string.isRequired,
    loggedin:PropTypes.bool.isRequired
  };

  onClick = (e) =>{
    localStorage.setItem('token','0')
    window.location.reload()
  }

  render(){
    return (
      <div className="App">
        <nav className="navbar navbar-light bg-light" style={{justifyContent:"center"}}>
          <a className="navbar-brand my-auto" href="/">My ToDo List</a>
          {this.props.token!=='0' ?<button onClick={this.onClick} className="btn btn-outline-info my-2 my-sm-0" style={{right:'5%',position:'absolute'}}>Logout</button>:<span></span>}
          </nav>
        {this.props.auth === '0'?<Login />:<ToDo/>}
      </div>
    );
    }
}

const mapStateToProps = state => ({
  auth: state.auth.token || '0',
  loggedin: state.auth.loggedin
})
export default connect(mapStateToProps)(App);
