import React, {Component} from 'react'
import axios from 'axios'
import '../../App.css'
import happiness from '../../assets/happiness.svg'

class SignIn extends Component {
  signUp () {
    const firstName = document.querySelector('input[name=firstName]').value
    const lastName = document.querySelector('input[name=lastName]').value
    const email = document.querySelector('input[name=email]').value
    const password = document.querySelector('input[name=password]').value
    const confirmPassword = document.querySelector('input[name=confirmPassword]').value
    console.log(firstName, lastName, email, password, confirmPassword)
    if (firstName && lastName && email && password && password === confirmPassword) {
      axios.post('/users/signup/', {
        firstName: firstName,
        lastName: lastName,
        email: email,
        password: password
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
              <h6>Get access to course material and real instructors</h6>
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

export default SignIn
