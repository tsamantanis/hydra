import React, {Component} from 'react'
import '../../App.css'
import './Main.css'

class SignIn extends Component {
  render () {
    return (
      <div className='Main'>
        <div className='Nav'>
          <div className='NavItem' />
          <div className='NavItem' />
        </div>
        <div className='Channels'>
          <h1>Channels</h1>
        </div>
        <div className='Feed'>
          <h1>Posts</h1>
        </div>
        <div className='Users'>
          <h1>Users</h1>
        </div>
      </div>
    )
  }
}

export default SignIn
