import React, {Component} from 'react'
import './ChannelGroup.css'

class ChannelGroup extends Component {
    render() {
        return (
            <div className='ChannelGroup m-t-15 m-b-15 m-l-20'>
                <h5 className="m-b-15">{this.props.channelLabel}</h5>
                { this.props.channelNames.map((channelName) => {
                    return(
                        <div className='ChannelItem m-b-10'>
                            <h6 className="m-auto">{'#  ' + channelName}</h6>
                        </div>
                )})}
            </div>
        )
    }
}

export default ChannelGroup
