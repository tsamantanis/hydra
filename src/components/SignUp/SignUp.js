import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import happiness from '../../assets/happiness.svg'

class SignUp extends Component {
    signUp () {
        const firstName = document.querySelector('input[name=firstName]').value
        const lastName = document.querySelector('input[name=lastName]').value
        const email = document.querySelector('input[name=email]').value
        const password = document.querySelector('input[name=password]').value
        const confirmPassword = document.querySelector('input[name=confirmPassword]').value
        if (firstName && lastName && email && password && password === confirmPassword) {
            api(
                method: 'post',
                url: '/users/signup',
                data: {
                    firstName: firstName,
                    lastName: lastName,
                    email: email,
                    password: password
                },
                headers: {
                    'content-type': 'multipart/form-data'
                },
            )
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
        } else if (password !== confirmPassword) {
            console.log('Please ensure passwords match.')
        }
    }

    render () {
        return (
            <div className='SignUp splitView'>
                <div className='left'>
                    <form method='POST'>
                        <legend>
                            <h1>Sign Up</h1>
                            <h6>Access course material and live instructors</h6>
                        </legend>
                        <fieldset>
                            <label htmlFor='firstName'>First Name</label>
                            <input type='text' name='firstName' placeholder='First' />
                            <label htmlFor='lastName'>Last Name</label>
                            <input type='text' name='lastName' placeholder='Last' />
                            <label htmlFor='email'>Email Address</label>
                            <input type='email' name='email' placeholder='name@address.com' />
                            <label htmlFor='password'>Password</label>
                            <input type='password' name='password' placeholder='Enter a password' />
                            <label htmlFor='password'>Confirm Password</label>
                            <input type='password' name='confirmPassword' placeholder='Confirm the password' />
                        </fieldset>
                        <button type='button' onClick={this.signUp}>Sign Up</button>
                    </form>
                    <small>Already have an account? <a href='/users/signin'>Sign In</a></small>
                </div>
                <div className='right'>
                    <img src={happiness} alt='happiness' />
                </div>
            </div>
        )
    }
}

export default SignUp
