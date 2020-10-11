import React, {Component} from 'react'
import api from '../../api'
import '../../App.css'
import './Main.css'

import ChannelGroup from './ChannelGroup'
import UserGroup from './UserGroup'
import SearchBar from './SearchBar'
import Post from './Post'

import Settings from '../Settings/Settings';

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
            showCommunity: true
        };
    }

    toggleCommunity = () => {
        this.setState({showCommunity: !this.state.showCommunity})
    }

    createPost() {
        const message = document.getElementById('NewPostMessage').value
        if (message) {
            api({
                method: 'POST',
                url: '/groups/1/channels/1',
                data: {
                    "user_id": 1,
                    "message": message
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

    submitOnEnter(event) {
        if (event.which === 13 && !event.shiftKey) {
            event.target.form.dispatchEvent(new Event("submit", {cancelable: true}))
            event.preventDefault()
        } else if (event.which === 13) {
            this.createPost()
        }
    }

    render () {
        let posts = ["Post", "Post", "Post"]
        return (
            <div className='Main'>
                <div className='Nav'>
                    <div className='NavItem m-b-20' />
                    <div className='NavItem m-b-20' />
                    <div className="AddClass">
                        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>                    </div>
                    <Settings />
                </div>
                <div className={this.state.showCommunity ? 'Channels' : 'Channels Channels-lg'}>
                    <h1>Class Name</h1>
                    <hr className='m-t-30' />
                    <ChannelGroup
                        channelLabel='Lectures'
                        channelNames={['Channel Name', 'Channel Name']}
                    />
                    <ChannelGroup
                        channelLabel='Assignments'
                        channelNames={['Channel Name', 'Channel Name']}
                    />
                    <ChannelGroup
                        channelLabel='Groups'
                        channelNames={['Channel Name', 'Channel Name']}
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
                        {posts.map((post) => {
                            return(
                                <Post

                                />
                            )
                        })}
                    </div>
                    <div className='CreatePost m-0'>
                        <textarea className="NewPostMessage" id="NewPostMessage" placeholder='Message class_name' rows="3" onKeyPress={this.submitOnEnter} />
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
                        <UserGroup
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
