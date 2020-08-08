import React, { Component } from 'react'
import ToDoForm from './ToDoForm'
import AddUser from './AddUser'
import {connect} from 'react-redux'
import PropTypes from 'prop-types'
import {getTodos,deleteTodo} from './actions/todos'

export class ToDo extends Component {
    state = {
        isListFormClicked : false,
        isItemFormClicked : false,
        listId:-1,
        itemId:-1,
        isAdmin:false,
        isAddUser: false
    }
    static propTypes = {
        todos: PropTypes.array.isRequired,
        getTodos: PropTypes.func.isRequired,
        deleteTodo: PropTypes.func.isRequired
    }

    toggleForm = () =>{
        this.setState({[this.state.isItemFormClicked]:![this.state.isItemFormClicked]})
    }

    componentDidMount(){
        this.props.getTodos();
    }

    render() {
        let flag = this.state.isListFormClicked || this.state.isItemFormClicked
        // let addUser = () => this.state.isAddUser
        let isAdmin = () => this.state.isAdmin
        console.log(this.props.todos)
        return (
            <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                {/* <AddUser toggleForm={true} /> */}
                {this.state.isAddUser === true?<AddUser toggleForm={true} />:''}
                {flag?<ToDoForm todoItem={this.state.isItemFormClicked} toggleForm={true} listId={this.state.listId}/>:''}
                <table className='table table-stripped' style={{ width:'75%', margin:'auto', marginBottom:'10px' }}>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Todo</th>
                            {isAdmin?<th>User</th>:<p>Hello</p>}
                            <th>Title</th>
                            <th>Priority</th>
                            <th>Completed</th>
                        </tr>
                    </thead>
                    <tbody>
                        { this.props.todos instanceof Array? (this.props.todos.map(todolist => (
                            <tr key={todolist.id}>
                                {console.log("inside")}
                                
                                {// eslint-disable-next-line
                                todolist.user?this.state.isAdmin=true:this.state.isAdmin=false}
                        <td>{todolist.id}</td>
                        <td>
                            <button type="button" className="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            </button>
                            <div className="dropdown-menu dropdown-menu-lg-left" style={{left:'-500'}}>
                                {todolist.items.map(todoitem => (
                                    <tr className="dropdown-item" key={todoitem.id}>
                                    <td>{todoitem.id}</td>
                                    <td>{todoitem.title}</td>
                                    <td>{todoitem.description}</td>
                                    <td>{todoitem.due_date}</td>
                                    <td>{todoitem.isCompleted?"COMPLETED":"DUE"}</td>
                                    <td><button className="btn btn-danger btn-sm" onClick={()=>{this.props.deleteTodo({'listId':null,'itemId':todoitem.id});this.props.getTodos()}}>Delete</button></td>
                                    <td><button className="btn btn-success btn-sm" onClick={()=>this.setState({isItemFormClicked:!this.state.isItemFormClicked,listId:todolist.id})}>Add Item</button></td>
                                    </tr>
                                ))}
                            </div>
                        </td>
                        {isAdmin?<td>{todolist.user}</td>:<p></p>}
                        <td>{todolist.title}</td>
                        <td>{todolist.priority?"HIGH":"LOW"}</td>
                        <td>{todolist.isCompleted?"COMPLETED":"DUE"}</td>
                        <td><button className="btn btn-danger btn-sm" onClick={()=>{this.props.deleteTodo({'listId':todolist.id,'itemId': null});this.props.getTodos()}}>Delete</button></td>
                        </tr>
                        ))):<h1>Waterloo</h1>}
                    </tbody>
                </table>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <button type="button" className="btn btn-info" style={{margin:'5px'}} onClick={()=>this.setState({isListFormClicked:!this.state.isListFormClicked})}>Add ToDo List</button>
                
                    {isAdmin?
                    (<button type="button" className="btn btn-warning" style={{margin:'5px'}} onClick={()=>this.setState({isAddUser:!this.state.isAddUser})}>Register Customer</button>)
                    :<span></span>}
                </div>
                </div>
        )
    }
}

const mapStateTOProps = state => ({
    
    todos: state.todos.todos //state.todos of reducers/index file and another todos for todos return by getTodos
})

export default connect(mapStateTOProps, {getTodos,deleteTodo})(ToDo)