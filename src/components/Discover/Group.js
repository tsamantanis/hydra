import React, {Component} from 'react'
import {Link} from 'react-router-dom';

import api from '../../api'

import '../../App.css'
import './Group.css'
import pythonImage from '../../assets/python-flask-angular.jpg'

class Group extends Component {
    render () {
        return (
            <Link to="/discover/preview" className="text-decoration-none col-3">
                <div className='Group m-t-40'>
                    <img src={pythonImage} alt='class image' />
                    <svg className="m-t-n25" width="330" height="28" viewBox="0 0 290 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M0 0C0 0 88.374 20 145 20C201.626 20 290 0 290 0V20H0V0Z" fill="#F7F7FF"/>
                    </svg>
                    <div className='groupInfo m-b-20'>
                        <h5>{this.props.groupName}</h5>
                        <h6 className='m-t-30'>From ${this.props.groupPrice}</h6>
                    </div>
                </div>
            </Link>
        )
    }
}

export default Group
