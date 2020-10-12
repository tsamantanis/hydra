import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './Group.css'
import group from '../../assets/group.svg'

class Group extends Component {

    groupPreview() {
        window.location.href = '/discover/preview'
    }

    render () {
        return (
            <div className='Group m-l-20 m-r-20 m-t-40'>
                <img src={group} alt='class image' className='group' onClick={this.groupPreview} />
                <div className='groupInfo m-b-20'>
                    <h5 onClick={this.groupPreview}>{this.props.groupTitle}</h5>
                    <h6 className='m-t-30'>From ${this.props.groupPrice}</h6>
                </div>
            </div>
        )
    }
}

export default Group
