import React, {Component} from 'react'
import {Link} from 'react-router-dom'
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
        let filteredGroups = this.state.searchTerm.length > 0 && this.state.groups.filter((group) => {
            let searchable = group.name + group.keywords.toString().replace(',', '') + group.dis;
            let searchTerms = this.state.searchTerm.toLowerCase().trim().split(' ');
            return searchTerms.every((term) => {
                return searchable.toLowerCase().includes(term);
            })
        })

        return (
            <div className="container discover" style={{backgroundImage: 'url('+ellipse+')', backgroundSize: "cover"}}>
                <Link to="/" className="backButton alt">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-home">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                </Link>
                <div className="row">
                    <form className='search col-12'>
                        <label htmlFor='discoverClasses'><h4 className='m-0'>Discover Classes</h4></label>
                        <input type='text' className='discoverClasses' name='discoverClasses' id='discoverClasses' placeholder='Search from a list of thousands of classes' value={this.state.searchTerm} onChange={this.updateSearch} />
                    </form>
                </div>
                {filteredGroups ?
                    <div className="row m-b-30">
                        <div className="col-9">
                            <div className="row">
                                {filteredGroups && filteredGroups.map(group => {
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
                        </div>
                    </div>
                    :
                    null
                }
                <img src={school} alt='school' className={filteredGroups ? 'school hidden m-t-auto' : 'school m-t-auto animate fadeIn one'} />
            </div>
        )
    }
}

export default Discover
