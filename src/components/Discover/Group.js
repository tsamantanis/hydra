import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './Group.css'
import group from '../../assets/group.svg'

class Group extends Component {
    render () {
        return (
            <div className='Group'>
                <img src={group} alt='class image' className='group' />
                <div className='groupInfo m-b-20'>
                    <h5>Build apps with Python, Flask, and Angular</h5>
                    <h6 className='m-t-30'>From $68</h6>
                </div>
            </div>
        )
    }
}

export default Group
