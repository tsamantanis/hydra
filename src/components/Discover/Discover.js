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
            searchTerm: '',
        }
    }

    componentDidMount() {
        this.getGroups();
    }

    getGroups = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups',
        })
        .then(function (response) {
            for (const group of response.data) {
                _this.setState({groups: [..._this.state.groups, group]})
            }
        })
        .catch(function (error) {
            console.log(error)
        })
    }

    updateSearch = (event) => {
        this.setState({
            searchTerm: event.target.value
        });
    };

    preventSubmit(event) {
        if (event.which === 13) {
            event.preventDefault()
        }
    }

    render () {
        let filteredGroups = this.state.groups.filter((group) => {
            let searchable = group.name + group.keywords.toString().replace(',', '') + group.dis;
            let searchTerms = this.state.searchTerm.toLowerCase().trim().split(' ');
            return searchTerms.every((term) => {
                return searchable.toLowerCase().includes(term);
            })
        })

        return (
            <div className='Discover'>
                <img src={ellipse} alt='ellipse' className='ellipse' />
                <form>
                    <label htmlFor='discoverClasses'><h4 className='m-0'>Discover Classes</h4></label>
                    <input type='text' name='discoverClasses' id='discoverClasses' placeholder='Search from a list of thousands of classes' value={this.state.searchTerm} onChange={this.updateSearch} />
                </form>
                <div className='searchResults row'>
                    {filteredGroups.map(group => {
                        return(
                            <Group
                                groupId={group._id}
                                groupName={group.name}
                                groupPrice={group.price}
                                groupDis={group.dis}
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
