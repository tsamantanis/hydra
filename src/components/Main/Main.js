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
          <h1>Class Name</h1>
          <hr />
          <div className='ChannelGroup'>
            <h5>Lectures</h5>
            <div className='ChannelItem'>
              <h6># Channel Name</h6>
            </div>
            <div className='ChannelItem'>
              <h6># Channel Name</h6>
            </div>
          </div>
          <div className='ChannelGroup'>
            <h5>Assignments</h5>
            <div className='ChannelItem'>
              <h6># Channel Name</h6>
            </div>
          </div>
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
