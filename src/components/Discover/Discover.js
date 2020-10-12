import React, {Component} from 'react'

import api from '../../api'

import '../../App.css'
import './Discover.css'
import ellipse from '../../assets/ellipse.svg'
import school from '../../assets/school.svg'

import Group from './Group'

class Discover extends Component {
    constructor(props) {
        super(props);
        this.state = {
            groups: [],
            displayGroups: [],
            loading: true,
        }
    }

    componentDidMount() {
        this.getGroups.apply(this)
    }

    getGroups = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups',
        })
        .then(function (response) {
            for (const group of response.data) {
                _this.setState({groups: [..._this.state.groups, group], loading: false})
            }
        })
        .catch(function (error) {
            console.log(error)
        })
    }

    searchGroups = (event) => {
        this.setState({displayGroups: []})
        const search = document.getElementById('discoverClasses').value
        if (search.length > 0) {
            this.state.groups.forEach(group => {
                if (group.name.includes(search) || group.keywords.includes(search) || group.dis.includes(search)) {
                    this.setState({displayGroups: [...this.state.displayGroups, group]})
                }
            })
        }
    }

    preventSubmit(event) {
        if (event.which === 13) {
            event.preventDefault()
        }
    }

    render () {
        return (

            <div className='Discover'>
                <img src={ellipse} alt='ellipse' className='ellipse' />
                <form>
                    <label htmlFor='discoverClasses'><h4 className='m-0'>Discover Classes</h4></label>
                    <input type='text' name='discoverClasses' id='discoverClasses' placeholder='Search from a list of thousands of classes' onKeyUp={this.searchGroups.bind(this)} onKeyPress={this.preventSubmit} />
                </form>
                <div className='searchResults row'>
                    {this.state.displayGroups.map(group => {
                        return(
                            <Group
                                groupName={group.name}
                                groupPrice="68"
                            />
                        )
                    })}
                </div>
                <img src={school} alt='school' className='school' />
            </div>
        )
    }
}

export default Discover
