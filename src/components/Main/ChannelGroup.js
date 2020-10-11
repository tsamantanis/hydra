import React, {Component} from 'react'
import './ChannelGroup.css'

class ChannelGroup extends Component {
    render() {
        return (
            <div className='ChannelGroup m-t-15 m-b-15'>
                <div className='ChannelTitle'>
                    <h5 className="m-b-15">{this.props.channelLabel}</h5>
                    <a className="float-right">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" className="feather feather-plus-circle">
                            <circle cx="12" cy="12" r="10" />
                            <line x1="12" y1="8" x2="12" y2="16" />
                            <line x1="8" y1="12" x2="16" y2="12" />
                        </svg>
                    </a>
                </div>
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
