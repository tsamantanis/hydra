import React, {Component} from 'react'

class ChannelGroup extends Component {
    render() {
        return (
            <div className='ChannelGroup'>
                <h5>{this.props.channelLabel}</h5>
                { this.props.channelNames.map((channelName) => {
                    return(
                        <div className='ChannelItem'>
                            <h6>{'#  ' + channelName}</h6>
                        </div>
                )})}
            </div>
        )
    }
}

export default ChannelGroup
