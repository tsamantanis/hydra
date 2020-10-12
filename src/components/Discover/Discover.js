import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './Discover.css'
import ellipse from '../../assets/ellipse.svg'
import school from '../../assets/school.svg'

class Discover extends Component {
    render () {
        return (
            <div className='Discover'>
                <img src={ellipse} alt='ellipse' className='ellipse' />
                <img src={school} alt='school' className='school' />
                <form>
                    <label htmlFor='discoverClasses'><h4 className='m-0'>Discover Classes</h4></label>
                    <input type='text' name='discoverClasses' id='discoverClasses' placeholder='Search from a list of thousands of classes' />
                </form>
            </div>
        )
    }
}

export default Discover
