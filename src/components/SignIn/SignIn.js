import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './SignIn.css'
import happiness from '../../assets/happiness.svg'

class SignIn extends Component {
    signIn () {
        const email = document.querySelector('input[name=email]').value
        const password = document.querySelector('input[name=password]').value
        if (email && password) {
            api({
                method: 'POST',
                url: '/users/signin',
                data: {
                    "email": email,
                    "password": password
                },
            })
            .then(function (response) {
                console.log(response.data.authToken)
                window.location.href='/'
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
                            <input type='email' name='email' placeholder='name@address.com' pattern="/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/" required />
                            <label htmlFor='password'>Password</label>
                            <input type='password' name='password' placeholder='Enter your password' required />
                        </fieldset>
                        <div className="buttonGradientContainer m-b-10 m-t-30">
                            <button className="m-l-0" type='button' onClick={this.signIn}>Sign In</button>
                        </div>
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
