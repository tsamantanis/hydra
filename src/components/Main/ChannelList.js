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
        this.getChannels()
    }

    getChannels = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then(function (response) {
            for (const channel of response.data) {
                _this.setState({channels: [..._this.state.channels, channel.name]})
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
                    channelNames={this.state.channels}
                />
                <ChannelGroup
                    channelLabel='Assignments'
                    channelNames={this.state.channels}
                />
            </>
        )
    }
}

export default ChannelList
