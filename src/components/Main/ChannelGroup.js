import React, {Component} from 'react'

class ChannelGroup extends Component {
    render() {
        return (
            <div className='ChannelGroup m-t-15 m-b-15 m-l-30'>
                <h5 className="m-b-20">{this.props.channelLabel}</h5>
                { this.props.channelNames.map((channelName) => {
                    return(
                        <div className='ChannelItem m-b-20'>
                            <h6>{'#  ' + channelName}</h6>
                        </div>
                )})}
            </div>
        )
    }
}

export default ChannelGroup
