import React, {Component} from 'react'
import './ChannelSection.css'

import AddChannel from '../AddChannel/AddChannel'
import AddTopic from '../AddTopic/AddTopic'
import AddAssignment from '../AddAssignment/AddAssignment'
class ChannelSection extends Component {

    displayChannel(channelName) {
        const allChannels = document.querySelectorAll('.ChannelItem')
        for (const channel of allChannels) {
            channel.classList.remove('activeChannel')
        }
        const currentChannel = document.getElementById(channelName)
        currentChannel.classList.add('activeChannel')

    }

    render() {
        return (
            <div className='ChannelSection m-t-15 m-b-15'>
                <div className='ChannelTitle'>
                    <h5 className="m-b-15">{this.props.channelLabel}</h5>
                    {this.props.channelLabel !== "Assignments" ? <AddTopic channelLabel={this.props.channelLabel} getChannels={this.props.getChannels} /> : <AddAssignment />}
                </div>
                { this.props.channels && this.props.channels.map((channel) => {
                    return(
                        <div className='ChannelItem m-b-10' id={channel._id} key={channel.name}>
                            <h6 className="m-auto" onClick={() => {this.displayChannel.bind(this, channel.name); this.props.loadPosts(channel._id)}}>{'#  ' + channel.name}</h6>
                        </div>
                )})}
            </div>
        )
    }
}

export default ChannelSection
