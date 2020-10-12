import React, {Component} from 'react'
import {Button} from 'reactstrap';
import {Modal} from 'reactstrap';
import {ModalHeader} from 'reactstrap';
import {ModalBody} from 'reactstrap';
import {ModalFooter} from 'reactstrap';

import api from '../../api'

import '../../App.css'
import './Settings.css'

class Settings extends Component {
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

    openSettings(setting, e) {
        const tabcontent = document.getElementsByClassName('tabcontent')
        for (const content of tabcontent) {
            content.style.display = 'none'
        }

        const tablinks = document.getElementsByClassName('tablinks')
        for (const link of tablinks) {
            link.className = link.className.replace(' active', '')
        }

        document.getElementById(setting).style.display = 'block'
        e.currentTarget.className += ' active'
    }

    async setActiveTab() {
        await document.getElementById('generalTab')
        document.getElementById('generalTab').click()
    }

    updateAccount () {
        const firstName = document.querySelector('input[name=firstName]').value
        const lastName = document.querySelector('input[name=lastName]').value
        const email = document.querySelector('input[name=email]').value
        const password = document.querySelector('input[name=password]').value
        if (firstName && lastName && email && password) {
            api({
                method: 'POST',
                url: '/users/user_id',
                data: {
                    "firstName": firstName,
                    "lastName": lastName,
                    "email": email,
                    "password": password
                },
            })
            .then(function (response) {
                console.log(response)
            })
            .catch(function (error) {
                console.log(error)
            })
        } else if (!firstName) {
            console.log('Please enter a first name.')
        } else if (!lastName) {
            console.log('Please enter a last name.')
        } else if (!email) {
            console.log('Please enter an email.')
        } else if (!password) {
            console.log('Please enter a password.')
        }
    }

    deleteAccount() {
        const firstName = document.querySelector('input[name=firstName]').value
        const lastName = document.querySelector('input[name=lastName]').value
        const email = document.querySelector('input[name=email]').value
        const password = document.querySelector('input[name=password]').value
        api({
            method: 'DELETE',
            url: '/users/user_id',
            data: {
                "firstName": firstName,
                "lastName": lastName,
                "email": email,
                "password": password
            },
        })
        .then(function (response) {
            console.log(response)
        })
        .catch(function (error) {
            console.log(error)
        })
    }

    render () {
        return (
            !this.state.modal ?
                <div className='Settings' onClick={() => { this.toggle(); this.setActiveTab()}}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-settings">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                    </svg>
                </div>
            :
                <Modal isOpen={this.state.modal} toggle={this.toggle} contentClassName='SettingsModal'>
                    <ModalHeader toggle={this.toggle}>
                    </ModalHeader>
                    <ModalBody>
                        <p className='big'>Overview</p>
                        <h2>Account</h2>
                        <div className='tab m-t-30'>
                            <a className='tablinks .big m-r-10' id='generalTab' onClick={this.openSettings.bind(null, 'General')}>General</a>
                            <a className='tablinks .big m-r-10' id='notificationsTab' onClick={this.openSettings.bind(null, 'Notifications')}>Notifications</a>
                            <a className='tablinks .big m-r-10' id='billingTab' onClick={this.openSettings.bind(null, 'Billing')}>Billing</a>
                        </div>
                        <hr className='m-t-10 m-b-30'/>

                        <section id='General' className='tabcontent general'>
                            <div className='Avatar'>
                                <div className='left'>
                                    <div className='UserIcon'/>
                                    <div className='avatarText m-l-10'>
                                        <p className='big m-b-5'>Your avatar</p>
                                        <small>PNG or JPG no bigger than 1000px wide and tall.</small>
                                    </div>
                                </div>
                                <div className='right'>
                                    <button type='button'>Upload</button>
                                </div>
                            </div>
                            <hr className='m-t-30 m-b-20'/>
                            <div className='UserInfo'>
                                <div className='left m-r-10'>
                                    <div className='userInput'>
                                        <label htmlFor='firstName'>First Name</label>
                                        <input type='text' name='firstName' id='firstName' value='Jimi' required />
                                    </div>
                                    <div className='userInput'>
                                        <label htmlFor='email'>Email Address</label>
                                        <input type='email' name='email' id='email' value='name@address.com' pattern='/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/' required />
                                    </div>
                                </div>
                                <div className='right m-l-10'>
                                    <div className='userInput'>
                                        <label htmlFor='lastName'>Last Name</label>
                                        <input type='text' name='lastName' id='lastName' value='Hendrix' required />
                                    </div>
                                    <div className='userInput'>
                                        <label htmlFor='password'>Password</label>
                                        <input type='text' name='password' id='password' value='&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;'/>
                                    </div>
                                    <button type='button' className='m-t-20' onClick={this.updateAccount}>Save</button>
                                </div>
                            </div>
                        </section>

                        <section id='Notifications' className='tabcontent notifications'>
                            <h2>Notifications</h2>
                        </section>

                        <section id='Billing' className='tabcontent billing'>
                            <h2>Billing</h2>
                        </section>

                    </ModalBody>
                    <ModalFooter className='m-b-40'>
                        <hr/>
                        <div className='deleteAccount'>
                            <div className='deleteAccountText'>
                                <h6>Delete your account</h6>
                                <small>Please note, deleting your account is a permanent action and will not be recoverable once completed.</small>
                            </div>
                            <Button color='danger' onClick={this.deleteAccount}>Delete</Button>
                        </div>
                    </ModalFooter>
                </Modal>

        )
    }
}

export default Settings
