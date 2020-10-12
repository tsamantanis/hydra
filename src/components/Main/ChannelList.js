import React, {Component} from 'react'
import api from '../../api'

import ChannelGroup from './ChannelGroup'

class ChannelList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            channels: []
        }
    }

    componentDidMount() {
        this.getChannels();
    }

    getChannels = () => {
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then(function (response) {
            for (const channel of response.data) {
                console.log(channel.name)
                // THIS IS READING ALL THE CHANNEL NAMES. THE SETSTATE BELOW THROWS A TYPE ERROR
                // this.setState({channels: [...this.state.channels, channel.name]})
            }
        })
        .catch(function (error) {
            console.log(error)
        })
    }



    render() {
        return (
            <>
                <ChannelGroup
                    channelLabel='Lectures'
                    channelNames={this.state.channels.map((channel) => {
                        return (
                            <h6>{channel}</h6>
                        )
                    })}
                />
                <ChannelGroup
                    channelLabel='Assignments'
                    channelNames={this.state.channels.map((channel) => {
                        return (
                            <h6>{channel}</h6>
                        )
                    })}
                />
            </>
        )
    }
}

export default ChannelList
