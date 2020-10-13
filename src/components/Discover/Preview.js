import React, {Component} from 'react'
import {Link} from 'react-router-dom';

import api from '../../api'
import Loading from '../Helpers/Loading'
import '../../App.css'
import './Preview.css'
import preview from '../../assets/preview.svg'
import backArrow from '../../assets/backArrow.svg'


class Preview extends Component {
    constructor (props) {
        super(props);
        this.state = {
            group: null
        }
    }

    componentDidMount() {
        this.loadGroup();
    }

    loadGroup = () => {
        api({
            method: 'GET',
            url: '/groups/' + this.props.match.params.id,
        })
        .then((response) => {
            this.setState({group: response.data})
        })
        .catch((error) => {
            console.log(error)
        })
    }

    enrollUserInGroup = () => {
        api({
            method: 'POST',
            url: '/groups/' + this.props.match.params.id + '/join',
            data: {
                "paymentMethodId": true,
            }
        })
        .then((response) => {
            console.log(response)
        })
        .catch((error) => {
            console.log(error)
        })
    }

    goToPayment = () => {
        this.enrollUserInGroup()
        window.location.href = '/'
    }

    render () {
        return (
            <div className='Preview'>
                <Link to="/discover" className="backButton alt">
                    <img src={backArrow} alt='go back to Discover page' />
                </Link>
                { this.state.group !== null ?
                    <>
                        <img src={preview} alt='preview' className='previewImage' />
                        <div className='previewText'>
                            <h1>{this.state.group.name}</h1>
                            <p className='big'>{this.state.group.dis}</p>
                            <ul className='m-0'>
                                <li><h6>13 Live Lectures</h6></li>
                                <li><h6>9 Assignments</h6></li>
                                <li><h6>5 Groups</h6></li>
                            </ul>
                            <div className='previewDatePrice'>
                                <p className='big'>Start Date: <span className='date'>10/13/2020</span></p>
                                <h4>{'$' + this.state.group.price + '/month'}</h4>
                            </div>
                            <div className='buttonGradientContainerAlt'>
                                <button type='button' className='alt' onClick={this.goToPayment}>Start Learning</button>
                            </div>
                        </div>
                    </>
                    :
                    <Loading />
                }
            </div>
        )
    }
}

export default Preview
