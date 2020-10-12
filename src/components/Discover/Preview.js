import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './Preview.css'
import preview from '../../assets/preview.svg'
import backArrow from '../../assets/backArrow.svg'


class Preview extends Component {

    goToPayment() {
        window.location.href = '/'
    }

    goToDiscover() {
        window.location.href = '/discover'
    }

    render () {
        return (
            <div className='Preview'>
                <img src={backArrow} alt='go back to Discover page' className='backButton alt' onClick={this.goToDiscover} />
                <img src={preview} alt='preview image' className='previewImage' />
                <div className='previewText'>
                    <h1>Build apps with Python, Flask, and Angular</h1>
                    <p className='big'>Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur imperdiet sapien id lorem iaculis sollicitudin. Morbi sit amet interdum leo, in blandit sapien. Vivamus a scelerisque ligula. Sed tellus nibh, eleifend eu ex non, consequat pretium est. Nulla venenatis ex vel nisl tempor volutpat.</p>
                    <ul className='m-0'>
                        <li><h6>13 Live Lectures</h6></li>
                        <li><h6>9 Assignments</h6></li>
                        <li><h6>5 Groups</h6></li>
                    </ul>
                    <div className='previewDatePrice'>
                        <p className='big'>Start Date: <span className='date'>10/13/2020</span></p>
                        <h4>$68/month</h4>
                    </div>
                    <div className='buttonGradientContainerAlt'>
                        <button type='button' className='alt' onClick={this.goToPayment}>Start Learning</button>
                    </div>
                </div>
            </div>
        )
    }
}

export default Preview
