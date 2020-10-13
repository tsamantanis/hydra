import React, {Component} from 'react'
import api from '../../api'

import ChannelSection from './ChannelSection'

class ChannelList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            topics: [],
            assignments: [],
            discussions: []
        }
    }

    getChannels = () => {
        api({
            method: 'GET',
            url: '/groups/5f848e95c86be6cef283dfee/channels'
        })
        .then((response) => {
            let topics = []
            let assignments = []
            let discussions = []
            response && response.data && response.data.forEach((channel) => {
                if (channel.category.toLowerCase() === "content") {
                    topics.push(channel)
                } else if (channel.category.toLowerCase() === "assignments") {
                    assignments.push(channel)
                } else if (channel.category.toLowerCase() === "discussions") {
                    discussions.push(channel)
                }
            })
            this.setState({topics, assignments, discussions})
            // console.log(this.state);
        })
        .catch((error) => {
            console.log(error)
        })
    }

    render() {
        return (
            <>
                <ChannelSection
                    channelLabel='Topics'
                    channels={this.state.channels}
                    getChannels={this.getChannels}
                    loadPosts={this.props.loadPosts}
                />
                <ChannelSection
                    channelLabel='Assignments'
                    channels={this.state.assignments}
                    getChannels={this.getChannels}
                    loadPosts={this.props.loadPosts}
                />
                <ChannelSection
                    channelLabel='Discussions'
                    channels={this.state.discussions}
                    getChannels={this.getChannels}
                    loadPosts={this.props.loadPosts}
                />
            </>
        )
    }
}

export default ChannelList
