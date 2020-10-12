import React, {Component} from 'react'
import {Link} from 'react-router-dom'
import axios from 'axios'
import api from '../../api'
import '../../App.css'
import './Main.css'

import ChannelList from './ChannelList'
import UserSection from './UserSection'
import SearchBar from './SearchBar'
import Post from './Post'
import NavItem from './NavItem'
import Loading from '../Helpers/Loading'
import Settings from '../Settings/Settings'

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showCommunity: true,
            posts: [],
            loadingPosts: false,
        };
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('token');
    }

    componentDidMount() {
        this.getAllUsersGroups()
    }

    toggleCommunity = () => {
        this.setState({showCommunity: !this.state.showCommunity})
    }

    createPost() {
        const message = document.getElementById('NewPostMessage').value
        if (message) {
            api({
                method: 'POST',
                url: '/groups/5f83e890d1bf28e13820a756/contents/create',
                data: {
                    "name": "New Post",
                    "dis": message
                },
            })
            .then(function (response) {
                console.log(response)
            })
            .catch(function (error) {
                console.log(error)
            })
        } else if (!message) {
            console.log('Please enter a message.')
        }
    }

    postOnEnter(event) {
        if (event.which === 13 && !event.shiftKey) {
            this.createPost()
            event.preventDefault()
        }
    }

    getAllUsersGroups = () => {
        // This will get all the groups of the current user so they can be displayed as NavItems
        api({
            method: 'GET',
            url: '/groups/yourgroups'
        })
        .then(function (response) {
            console.log(response.data)
        })
        .catch(function (error) {
            console.log(error)
        })
    }

    getPosts = (channel_id) => {
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels/' + channel_id
        })
        .then((response) => {
            let posts = []
            posts.push(response.data)
            this.setState({posts, loadingPosts: false})
        })
        .catch((error) => {
            console.log(error)
        })
    }

    loadPosts = (channel_id) => {
        // This will get all the posts for the selected channel_id
        this.setState({loadingPosts: true}, () => {
            this.getPosts(channel_id)
        })
    }

    render () {
        return (
            <div className='Main'>
                <div className='Nav'>
                    <NavItem />
                    <NavItem />
                    <Link to="/discover" className="AddClass">
                        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" className="feather feather-plus">
                            <line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                    </Link>
                    <Settings />
                </div>
                <div className={this.state.showCommunity ? 'Channels' : 'Channels Channels-lg'}>
                    <h1>Class Name</h1>
                    <hr className='m-t-30' />
                    <ChannelList
                        loadPosts={this.loadPosts}
                    />
                </div>
                <div className={this.state.showCommunity ? 'Feed' : 'Feed Feed-lg'}>
                    <div className='HeaderToolbar'>
                        <SearchBar
                            placeHolder='Search class_name'
                        />
                        {!this.state.showCommunity ?
                            <a onClick={this.toggleCommunity} className='float-right m-t-30 m-b-n5'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-plus-circle">
                                    <circle cx="12" cy="12" r="10" />
                                    <line x1="12" y1="8" x2="12" y2="16" />
                                    <line x1="8" y1="12" x2="16" y2="12" />
                                </svg>
                            </a>
                        : null }
                    </div>
                    <div className='Posts'>
                        {this.state.loadingPosts ?
                            <Loading />
                            :
                            this.state.posts.map((post) => {
                                return(
                                    <Post

                                    />
                                )
                            })
                        }
                    </div>
                    <div className='CreatePost m-0'>
                        <svg onClick={this.createPost} className="sendIcon" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" class="feather feather-send"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                        <textarea className="NewPostMessage" id="NewPostMessage" placeholder='Message class_name' rows="3" onKeyPress={this.postOnEnter.bind(this)} />
                    </div>
                </div>
                { this.state.showCommunity ?
                    <div className='Users'>
                        <div className='UsersTitle'>
                            <h1 className='m-r-20'>Community</h1>
                            <a onClick={this.toggleCommunity} className='float-right m-t-30 m-b-n5'>
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-minus-circle">
                                    <circle cx="12" cy="12" r="10" />
                                    <line x1="8" y1="12" x2="16" y2="12" />
                                </svg>
                            </a>
                        </div>
                        <hr className='m-t-30' />
                        <UserSection
                            groupTitle="Instructors"
                            userItems={[
                                {
                                    "name": "Starlight Romero",
                                    "status": "4hr ago"
                                },
                                {
                                    "name": "Starlight Romero",
                                    "status": "4hr ago"
                                }
                            ]}
                        />
                    </div>
                : null }
            </div>
        )
    }
}

export default Main
