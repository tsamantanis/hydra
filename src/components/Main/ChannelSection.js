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

    displayChannelSections() {
        if (this.props.channelLabel === "Topics") {
            return <AddTopic channelLabel={this.props.channelLabel} getChannels={this.props.getChannels} />
        } else if (this.props.channelLabel === "Assignments") {
            return <AddAssignment channelLabel={this.props.channelLabel} getChannels={this.props.getChannels} />
        } else if (this.props.channelLabel === "Discussions") {
            return <AddChannel channelLabel={this.props.channelLabel} getChannels={this.props.getChannels} />
        }
    }

    render() {
        return (
            <div className='ChannelSection m-t-15 m-b-15'>
                <div className='ChannelTitle'>
                    <h5 className="m-b-15">{this.props.channelLabel}</h5>
                    {this.displayChannelSections()}
                </div>
                { this.props.channels && this.props.channels.map((channel) => {
                    return(
                        <div className='ChannelItem m-b-10' id={channel._id} key={channel.name}>
                            <h6 className="m-auto" onClick={() => {this.displayChannel.bind(this, channel.name); this.props.loadPosts(channel._id.$oid)}}>{'#  ' + channel.name}</h6>
                        </div>
                )})}
            </div>
        )
    }
}

export default ChannelSection
