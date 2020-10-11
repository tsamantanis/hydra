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

    render () {
        return (
            <div className='Settings'>
                <Button color='primary' onClick={() => { this.toggle(); this.setActiveTab()}}>Settings</Button>
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
                                        <input type='text' name='firstName' id='firstName' placeholder='Jimi'/>
                                    </div>
                                    <div className='userInput'>
                                        <label htmlFor='email'>Email Address</label>
                                        <input type='email' name='email' id='email' placeholder='name@address.com'/>
                                    </div>
                                </div>
                                <div className='right m-l-10'>
                                    <div className='userInput'>
                                        <label htmlFor='lastName'>Last Name</label>
                                        <input type='text' name='lastName' id='lastName' placeholder='Hendrix'/>
                                    </div>
                                    <div className='userInput'>
                                        <label htmlFor='password'>Password</label>
                                        <input type='text' name='password' id='password' placeholder='&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;'/>
                                    </div>
                                    <button type='button' className='m-t-20'>Save</button>
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
                            <Button color='danger' onClick={this.toggle}>Delete</Button>
                        </div>
                    </ModalFooter>
                </Modal>
            </div>
        )
    }
}

export default Settings
