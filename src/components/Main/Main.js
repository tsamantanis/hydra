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
                    <div className='NavItem m-b-20' />
                    <div className='NavItem m-b-20' />
                </div>
                <div className='Channels'>
                    <h1>Class Name</h1>
                    <hr className='m-t-40' />
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
                    <div class='SearchBar'>
                        <form>
                            <input type='text' placeholder='Search class_name' />
                        </form>
                    </div>
                    <div className='CreatePost'>
                        <form>
                        </form>
                    </div>
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
