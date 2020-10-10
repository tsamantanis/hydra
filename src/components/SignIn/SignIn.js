import React, {Component} from 'react'
import '../../App.css'
import './SignIn.css'
import happiness from '../../assets/happiness.svg'

class SignIn extends Component {
  render () {
    return (
      <div className='SignIn'>
        <div className='left'>
          <form>
            <legend>
              <h1>Sign In</h1>
              <h6>Access your messages, tutorials, and more</h6>
            </legend>
            <fieldset>
              <label for='email'>Email Address</label>
              <input type='email' name='email' placeholder='name@address.com' />
              <label for='password'>Password</label>
              <input type='password' name='password' placeholder='Enter your password' />
            </fieldset>
            <button type='submit'>Sign In</button>
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
