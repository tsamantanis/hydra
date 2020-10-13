import React, {Component} from 'react'
import {Modal} from 'reactstrap';
import {ModalHeader} from 'reactstrap';
import {ModalBody} from 'reactstrap';

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

    componentDidMount() {
        this.props.getChannels('discussions')
    }

    createChannel = () => {
        const _this = this
        const name = document.querySelector('input[name=channelName]').value
        const dis = document.querySelector('input[name=description]').value
        const category = document.querySelector('input[name=channelLabel]').value.toLowerCase()
        if (name && dis) {
            api({
                method: 'POST',
                url: '/groups/5f851b320305d23b48751521/channels/create',
                data: {
                    "name": name,
                    "dis": dis,
                    "category": category
                },
            })
            .then(function (response) {
                _this.toggle()
                _this.props.getChannels('discussions')
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
                            <input type='hidden' id='channelLabel' name='channelLabel' value={this.props.channelLabel} required />
                            <label htmlFor='channelName'>Channel Name</label>
                            <input type='text' id='channelName' name='channelName' placeholder='# CS1.1 Object Oriented Programming' required />
                        </div>
                        <div className='userInput'>
                            <label htmlFor='description'>Description</label>
                            <input type='text' id='description' name='description' placeholder='What is this channel about?' required />
                        </div>
                        <div className='buttonGradientContainerAlt m-b-40'>
                            <button onClick={this.createChannel}>Add</button>
                        </div>
                    </ModalBody>
                </Modal>
        )
    }
}

export default AddChannel
