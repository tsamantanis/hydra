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
            url: '/groups/1/channels'
        })
        .then(function (response) {
            console.log(response)
        })
        .catch(function (error) {
            console.log(error)
        })
        // api.get('/groups/1/channels').then(function (response) {
        //     console.log(response)
        // })
        // .catch(function (error) {
        //     console.log(error)
        // })
    }



    render() {
        return (
            <ChannelGroup
                channelLabel='Lectures'
                channelNames={this.state.channels.map((channel) => {
                    return ""
                })}
            />

        )
    }
}

export default ChannelList
