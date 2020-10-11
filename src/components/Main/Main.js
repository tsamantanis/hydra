import React, {Component} from 'react'
import '../../App.css'
import './Main.css'
import ChannelGroup from './ChannelGroup'
import UserGroup from './UserGroup'
import SearchBar from './SearchBar'
import Post from './Post'
class Main extends Component {
    render () {
        let posts = ["Post", "Post", "Post"]
        return (
            <div className='Main'>
                <div className='Nav'>
                    <div className='NavItem m-b-20' />
                    <div className='NavItem m-b-20' />
                </div>
                <div className='Channels'>
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
                <div className='Feed'>
                    <SearchBar
                        placeHolder='Search class_name'
                    />
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
                <div className='Users'>
                    <h1>Community</h1>
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
            </div>
        )
    }
}

export default Main
