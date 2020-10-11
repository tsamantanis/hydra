import React, {Component} from 'react'
import '../../App.css'
import './Main.css'
import ChannelGroup from './ChannelGroup'
import UserGroup from './UserGroup'
import SearchBar from './SearchBar'
import Post from './Post'
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

    render () {
        let posts = ["Post", "Post", "Post"]
        return (
            <div className='Main'>
                <div className='Nav'>
                    <div className='NavItem m-b-20' />
                    <div className='NavItem m-b-20' />
                    <div className='Settings'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-settings">
                            <circle cx="12" cy="12" r="3"></circle>
                            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                        </svg>
                    </div>
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
                        <textarea className="NewPostMessage" placeholder='Message class_name' rows="3" />
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
