import React, {Component} from 'react'
import axios from 'axios'
import '../../App.css'
import happiness from '../../assets/happiness.svg'

class SignIn extends Component {
  signIn () {
    const email = document.querySelector('input[type=email]')
    console.log(email.value)
    // axios.post('/users/signin/')
    // .then(function (response) {
    //   console.log(response)
    //   window.location.href = '/admin/employees'
    // })
    // .catch(function (error) {
    //   console.log(error)
    //   window.location.href = '/admin/employees'
    // })
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
            <button type='submit' onClick='signIn'>Sign In</button>
          </form>
          <small>Need an account? <a href='/users/signup'>Sign Up</a></small>
        </div>
        <div className='right'>
          <img src={happiness} alt='happiness' />
        </div>
      </div>
    )
  }
}

export default SignIn
