import React, {Component} from 'react'
import {Button} from 'reactstrap';
import {Modal} from 'reactstrap';
import {ModalHeader} from 'reactstrap';
import {ModalBody} from 'reactstrap';
import {ModalFooter} from 'reactstrap';

import api from '../../api'

import '../../App.css'
import './AddChannel.css'

class AddChannel extends Component {
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

    createChannel() {
        const name = document.querySelector('input[name=channelName]').value
        const dis = document.querySelector('input[name=description]').value
        if (name && dis) {
            api({
                method: 'POST',
                url: '/groups/1/channels/create',
                data: {
                    "name": name,
                    "dis": dis
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
                <Modal isOpen={this.state.modal} toggle={this.toggle} contentClassName='AddChannelModal'>
                    <ModalHeader toggle={this.toggle}>
                    </ModalHeader>
                    <ModalBody>
                        <h2>Add Channel</h2>
                        <p className='big'>Channels are where your team communicates. They’re best when organized around a lecture or topic.</p>
                        <div className='userInput'>
                            <label htmlFor='channelName'>Channel Name</label>
                            <input type='text' id='channelName' name='channelName' placeholder='# CS1.1 Object Oriented Programming'/>
                        </div>
                        <div className='userInput'>
                            <label htmlFor='description'>Description</label>
                            <input type='text' id='description' name='description' placeholder='What is this channel about?' />
                        </div>
                    </ModalBody>
                    <ModalFooter className='m-b-40'>
                        <Button onClick={this.createChannel}>Add</Button>
                    </ModalFooter>
                </Modal>
        )
    }
}

export default AddChannel