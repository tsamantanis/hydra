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
            modal: true
        };

        this.toggle = this.toggle.bind(this);
    }

    toggle() {
        this.setState({
            modal: !this.state.modal
        });
        // document.getElementById('generalTab').click()
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

    render () {
        return (
            <div className='Settings'>
                <Button color='primary' onClick={this.toggle}>Settings</Button>
                <Modal isOpen={this.state.modal} toggle={this.toggle} contentClassName='SettingsModal'>
                    <ModalHeader toggle={this.toggle}>
                    </ModalHeader>
                    <ModalBody>
                        <p className='big'>Overview</p>
                        <h2>Account</h2>
                        <div className='tab m-t-30'>
                            <a className='tablinks .big m-r-10' id='generalTab' onLoad onClick={this.openSettings.bind(null, 'General')}>General</a>
                            <a className='tablinks .big m-r-10' id='notificationsTab' onClick={this.openSettings.bind(null, 'Notifications')}>Notifications</a>
                            <a className='tablinks .big m-r-10' id='billingTab' onClick={this.openSettings.bind(null, 'Billing')}>Billing</a>
                        </div>
                        <hr className='m-t-10'/>

                        <section id='General' className='tabcontent general'>
                            <div className='Avatar'>
                                <div className='UserIcon'/>
                                <div className='avatarText'>
                                    <p className='big'>Your avatar</p>
                                    <small>PNG or JPG no bigger than 1000px wide and tall.</small>
                                </div>
                                <button type='button'>Upload</button>
                            </div>
                        </section>

                        <section id='Notifications' className='tabcontent notifications'>
                            <h2>Notifications</h2>
                        </section>

                        <section id='Billing' className='tabcontent billing'>
                            <h2>Billing</h2>
                        </section>

                    </ModalBody>
                    <ModalFooter>
                        <div className='deleteAccount'>
                            <h6>Delete your account</h6>
                            <small>Please note, deleting your account is a permanent action and will not be recoverable once completed.</small>
                        </div>
                        <Button color='danger' onClick={this.toggle}>Delete Account</Button>
                    </ModalFooter>
                </Modal>
            </div>
        )
    }
}

export default Settings
