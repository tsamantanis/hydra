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

    render () {
        return (
            <div className='AddChannel'>
                <Button color='primary' onClick={this.toggle}>Add Channel</Button>
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
                        <Button onClick={this.toggle}>Add</Button>
                    </ModalFooter>
                </Modal>
            </div>
        )
    }
}

export default AddChannel
