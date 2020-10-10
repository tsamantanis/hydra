import React, {Component} from 'react'
import '../../App.css'
import './Main.css'
import ChannelGroup from './ChannelGroup'
import UserGroup from './UserGroup'
class Main extends Component {
    render () {
        return (
            <div className='Main'>
                <div className='Nav'>
                    <div className='NavItem' />
                    <div className='NavItem' />
                </div>
                <div className='Channels'>
                    <h1>Class Name</h1>
                    <hr />
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
                    <h1>Posts</h1>
                </div>
                <div className='Users'>
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
