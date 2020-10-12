import React, {Component} from 'react'
import './NavItem.css'

class NavItem extends Component {

    displayChannel(channelName) {
        alert(channelName)
    }

    render() {
        return (
            <div className='NavItem m-b-20'>
            </div>
        )
    }
}

export default NavItem
