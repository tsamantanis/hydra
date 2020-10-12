import React, {Component} from 'react'
import api from '../../api'

import ChannelGroup from './ChannelGroup'

class ChannelList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            channels: [],
            assignments: []
        }
    }

    componentDidMount() {
        this.getChannels()
    }

    getChannels = () => {
        const _this = this
        this.setState({channels: []})
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

    getAssignments = () => {
        const _this = this
        this.setState({assignments: []})
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/assignments'
        })
        .then(function (response) {
            for (const assignment of response.data) {
                _this.setState({assignments: [..._this.state.assignments, assignment.name]})
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
                    getChannels={this.getChannels}
                />
                <ChannelGroup
                    channelLabel='Assignments'
                    channelNames={this.state.assignments}
                    getChannels={this.getAssignments}
                />
            </>
        )
    }
}

export default ChannelList
