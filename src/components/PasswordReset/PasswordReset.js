import React, {Component} from 'react'
import '../../App.css'
import coworking from '../../assets/coworking.svg'

class SignIn extends Component {
  render () {
    return (
      <div className='PasswordReset splitView'>
        <div className='left'>
          <form method='POST'>
            <legend>
              <h1>Password Reset</h1>
              <h6>Enter your email to get a password reset link</h6>
            </legend>
            <fieldset>
              <label htmlFor='email'>Email Address</label>
              <input type='email' name='email' placeholder='name@address.com' />
            </fieldset>
            <button type='submit'>Reset Password</button>
          </form>
          <small>Remember your password? <a href='/users/signin'>Sign In</a></small>
        </div>
        <div className='right'>
          <img src={coworking} alt='coworking' />
        </div>
      </div>
    )
  }
}

export default SignIn
