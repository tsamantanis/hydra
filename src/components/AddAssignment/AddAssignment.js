import React, {Component} from 'react'
import {Modal} from 'reactstrap';
import {ModalHeader} from 'reactstrap';
import {ModalBody} from 'reactstrap';
import {ModalFooter} from 'reactstrap';

import api from '../../api'

import '../../App.css'
import './AddAssignment.css'

class AddAssignment extends Component {
    constructor(props) {
        super(props);
        this.state = {
            modal: false
        };

        this.toggle = this.toggle.bind(this);
    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
    }

    createAssignment = () => {
        const name = document.getElementById('name').value
        const dis = document.getElementById('description').value
        const maxGrade = document.getElementById('totalPoints').value
        const dueDate = document.getElementById('dueDate').value
        const startDate = document.getElementById('startDate').value
        if (name && dis && maxGrade && dueDate && startDate) {
            api({
                method: 'POST',
                url: '/groups/5f83e890d1bf28e13820a756/assignments/create',
                data: {
                    "name": name,
                    "dis": dis,
                    "maxGrade": maxGrade,
                    "dueDate": dueDate,
                    "startDate": startDate
                },
            })
            .then(function (response) {
                console.log(response)
            })
            .catch(function (error) {
                console.log(error)
            })
        } else if (!name) {
            console.log('Please enter a name.')
        } else if (!dis) {
            console.log('Please enter a description.')
        } else if (!maxGrade) {
            console.log('Please enter the total points.')
        } else if (!dueDate) {
            console.log('Please enter a due date.')
        } else if (!startDate) {
            console.log('Please enter a start date.')
        }
    }

    render () {
        return (
            !this.state.modal ?
                <a className="float-right" onClick={this.toggle}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-plus-circle">
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="8" x2="12" y2="16" />
                        <line x1="8" y1="12" x2="16" y2="12" />
                    </svg>
                </a>
                :
                <Modal isOpen={this.state.modal} toggle={this.toggle} contentClassName='AddAssignmentModal'>
                    <ModalHeader toggle={this.toggle}>
                    </ModalHeader>
                    <ModalBody>
                        <p className='big'>Overview</p>
                        <h2>Assignment</h2>
                        <hr className='m-t-30 m-b-30'/>
                        <div className='assignmentImage'>
                            <div className='left'>
                                <div className='assignmentIcon'/>
                                <div className='assignmentText m-l-10'>
                                    <p className='big m-b-5'>Assignment Image</p>
                                    <small>PNG or JPG no bigger than 1000px wide and tall.</small>
                                </div>
                            </div>
                            <div className='right'>
                                <button type='button'>Upload</button>
                            </div>
                        </div>
                        <hr className='m-t-30 m-b-30'/>
                        <div className='assignmentInfo'>
                            <div className='left m-r-10'>
                                <div className='userInput'>
                                    <label htmlFor='name'>Name</label>
                                    <input type='text' id='name' name='name' placeholder='Homework 1' required/>
                                </div>
                                <div className='userInput'>
                                    <label htmlFor='attachments'>Attachments</label>
                                    <input type='file' id='attachments' name='attachments' placeholder='Upload Files' required/>
                                </div>
                                <div className='userInput'>
                                    <label htmlFor='startDate'>Start Date</label>
                                    <input type='date' id='startDate' name='startDate' placeholder='10/11/2020' required/>
                                </div>
                                <div className='userInput'>
                                    <label htmlFor='totalPoints'>Total Points</label>
                                    <input type='number' id='totalPoints' name='totalPoints' placeholder='100' required/>
                                </div>
                            </div>
                            <div className='right m-l-10'>
                                <div className='userInput'>
                                    <label htmlFor='description'>Description</label>
                                    <input type='text' id='description' name='description' placeholder='How to create a Hello World! page with Flask' required/>
                                </div>
                                <div className='userInput'>
                                    <label htmlFor='assignmentType'>Assignment Type</label>
                                    <input type='text' id='assignmentType' name='assignmentType' placeholder='Required' required/>
                                </div>
                                <div className='userInput'>
                                    <label htmlFor='dueDate'>Due Date</label>
                                    <input type='date' id='dueDate' name='dueDate' placeholder='10/13/2020' required/>
                                </div>
                                <button className='m-t-40' onClick={this.createAssignment}>Save</button>
                            </div>
                        </div>
                    </ModalBody>
                </Modal>
        )
    }
}

export default AddAssignment
