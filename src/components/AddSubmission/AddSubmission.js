import React, {Component} from 'react'
import {Modal} from 'reactstrap';
import {ModalHeader} from 'reactstrap';
import {ModalBody} from 'reactstrap';

import api from '../../api'

import '../../App.css'
import './AddSubmission.css'

class AddSubmission extends Component {
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

    createSubmission = () => {
        const _this = this
        const url = document.querySelector('input[name=projectUrl]').value
        if (url) {
            api({
                method: 'POST',
                url: '/groups/5f848e95c86be6cef283dfee/assignments/5f84e4a8b1b1e1bc745474c7/submissions/create',
                data: {
                    "tempFieldId": url,
                    "userId": 100,
                    "scoredGrade": 100
                },
            })
            .then(function (response) {
                _this.toggle()
            })
            .catch(function (error) {
                console.log(error)
            })
        } else if (!url) {
            console.log('Please enter a url.')
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
                <Modal isOpen={this.state.modal} toggle={this.toggle} contentClassName='AddSubmissionModal'>
                    <ModalHeader toggle={this.toggle}>
                    </ModalHeader>
                    <ModalBody>
                        <h2>Add Submission</h2>
                        <p className='big'>Copy and paste below the link to your coding project to submit you assignment.</p>
                        <div className='userInput'>
                            <label htmlFor='projectUrl'>Project URL</label>
                            <input type='url' id='projectUrl' name='projectUrl' placeholder='https://www.github.com/tsamantanis/hydra' required />
                        </div>
                        <div className='buttonGradientContainerAlt m-b-40'>
                            <button onClick={this.createSubmission}>Add</button>
                        </div>
                    </ModalBody>
                </Modal>
        )
    }
}

export default AddSubmission
