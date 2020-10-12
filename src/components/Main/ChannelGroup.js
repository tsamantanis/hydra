import React, {Component} from 'react'
import './ChannelGroup.css'

import AddChannel from '../AddChannel/AddChannel'
import AddAssignment from '../AddAssignment/AddAssignment'
class ChannelGroup extends Component {
    render() {
        return (
            <div className='ChannelGroup m-t-15 m-b-15'>
                <div className='ChannelTitle'>
                    <h5 className="m-b-15">{this.props.channelLabel}</h5>
                    {this.props.channelLabel !== "Assignments" ? <AddChannel channelLabel={this.props.channelLabel} /> : <AddAssignment />}
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
