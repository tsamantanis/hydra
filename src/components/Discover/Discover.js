import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './Discover.css'
import ellipse from '../../assets/ellipse.svg'
import school from '../../assets/school.svg'

import Group from './Group'

class Discover extends Component {

    getGroups() {
        api({
            method: 'GET',
            url: '/groups',
        })
    }

    searchGroups() {
        console.log('searching')
        const search = document.getElementById('discoverClasses').value
        if (value.length < 0) {
            const groups this.getGroups()
            const displayGroups = groups.filter(group => {
                return group.name.includes(search) || group.keywords.includes(search) || group.dis.includes(search)
            })
            console.log(displayGroups)
        }
    }

    render () {
        return (
            <div className='Discover'>
                <img src={ellipse} alt='ellipse' className='ellipse' />
                <form>
                    <label htmlFor='discoverClasses'><h4 className='m-0'>Discover Classes</h4></label>
                    <input type='text' name='discoverClasses' id='discoverClasses' placeholder='Search from a list of thousands of classes' onKeyPress={this.searchGroups} />
                </form>
                <div className='searchResults'>
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    {/* <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        />
                    <Group
                        groupTitle="Build apps with Python, Flask, and Angular"
                        groupPrice="68"
                        /> */}
                </div>
                <img src={school} alt='school' className='school' />
            </div>
        )
    }
}

export default Discover
