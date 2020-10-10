import React, {Component} from 'react'
import '../../App.css'
import happiness from '../../assets/happiness.svg'

class SignIn extends Component {
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
            <button type='submit'>Sign Up</button>
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
