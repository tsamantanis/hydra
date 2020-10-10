import React, {Component} from 'react'
import axios from 'axios'

import api from '../../api'

import '../../App.css'
import happiness from '../../assets/happiness.svg'

class SignIn extends Component {
    signIn () {
        const email = document.querySelector('input[name=email]').value
        const password = document.querySelector('input[name=password]').value
        if (email && password) {
            api.post('/users/signIn/', {
                email: email,
                password: password
            })
            .then(function (response) {
                console.log(response)
            })
            .catch(function (error) {
                console.log(error)
            })
        } else if (!email) {
            console.log('Please enter an email.')
        } else if (!password) {
            console.log('Please enter a password.')
        }
    }

    render () {
        return (
            <div className='SignIn splitView'>
                <div className='left'>
                    <form>
                        <legend>
                            <h1>Sign In</h1>
                            <h6>Access your messages, tutorials, and more</h6>
                        </legend>
                        <fieldset>
                            <label htmlFor='email'>Email Address</label>
                            <input type='email' name='email' placeholder='name@address.com' />
                            <label htmlFor='password'>Password</label>
                            <input type='password' name='password' placeholder='Enter your password' />
                        </fieldset>
                        <button type='button' onClick={this.signIn}>Sign In</button>
                    </form>
                    <small>Need an account? <a href='/users/signUp'>Sign Up</a></small>
                </div>
                <div className='right'>
                    <img src={happiness} alt='happiness' />
                </div>
            </div>
        )
    }
}

export default SignIn
