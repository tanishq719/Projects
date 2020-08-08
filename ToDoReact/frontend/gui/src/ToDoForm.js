import React, { Component } from 'react'
import {connect} from 'react-redux'
import PropTypes from 'prop-types'
import {addTodoList,getTodos} from './actions/todos'

export class ToDoForm extends Component {
    state = {
        listTitle: -1,
        priority: false,
        itemTitle: undefined,
        duedate: undefined,
        description: '',
        toggleForm:false,
        listId:-1
    }

    static propTypes = {
        addTodoList : PropTypes.func.isRequired,
        getTodos: PropTypes.func.isRequired
    }

    onChange = e => this.setState({[e.target.name]: e.target.value});

    onSubmit = e => {
        e.preventDefault();
        const {listTitle,priority,itemTitle,duedate,description,toggleForm,listId} = this.state;
        const listI = {listTitle,priority,itemTitle,duedate,description,toggleForm,listId}
        this.props.addTodoList(listI)
        this.props.getTodos()
        this.setState({toggleForm:!toggleForm})
        this.props.todoItem = !this.props.todoItem
    }

    componentDidMount(){
        // this.setState({toggleForm :this.props.toggleForm})
        this.setState({listId:this.props.listId})
    }

    render() {
        const {listTitle,priority,itemTitle,duedate,description} = this.state
        return (
            <div>
            {!this.state.toggleForm?
            (<div style={{width:'75%',margin:'auto'}}>
            <form onSubmit={this.onSubmit}>
                {this.props.todoItem?<span></span>:
                <div className="row">
                <div className="col">
                    <label>List Title</label>
                    <input onChange={this.onChange} className="form-control" type='text' name="listTitle" value={listTitle}/>
                </div>
                <div className="col" style={{margin:"auto", marginLeft:'25%'}}>
                    <input onChange={this.onChange} type="checkbox" className="form-check-input" name="priority" checked={priority}/>
                    <label className='form-check-label'>Set on Priority</label>
                </div>
            </div>}
                
                <div className="row">
                    <div className="col">
                        <label>ToDo Item Title</label>
                        <input onChange={this.onChange} className="form-control" type='text' name="itemTitle" value={itemTitle}/>
                        <label>Due Date</label>
                        <input onChange={this.onChange} className="form-control" type='text' name="duedate" value={duedate}/>
                    </div>
                    <div className="col">
                        <label>Description</label>
                        <textarea onChange={this.onChange} className="form-control" type='text' name="description" value={description}/>
                        {console.log(this.state.listId)}
                    </div>
                </div>
                <div style={{display:'flex',justifyContent:'center',margin:'10px'}}><button type="submit" className="btn btn-primary">Submit</button></div>
            </form>
            </div>):<span></span>}</div>
        )
    }
}

export default connect(null,{addTodoList,getTodos})(ToDoForm)