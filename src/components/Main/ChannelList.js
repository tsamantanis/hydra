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

    getChannels = (section) => {
        api({
            method: 'GET',
            url: '/groups/5f848e95c86be6cef283dfee/channels'
        })
        .then((response) => {
            let topics = []
            let assignments = []
            let discussions = []
            response && response.data && response.data.forEach((channel) => {
                if (channel.category === "content") {
                    topics.push(channel)
                } else if (channel.category === "assignments") {
                    assignments.push(channel)
                } else if (channel.category === "discussions") {
                    discussions.push(channel)
                }
            })
            this.setState({topics, assignments, discussions})
            console.log(response);
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
                    getChannels={this.getChannels.bind(this, 'Topics')}
                    loadPosts={this.props.loadPosts}
                />
                <ChannelSection
                    channelLabel='Assignments'
                    channels={this.state.assignments}
                    getChannels={this.getChannels.bind(this, 'Assignments')}
                    loadPosts={this.props.loadPosts}
                />
                <ChannelSection
                    channelLabel='Discussions'
                    channels={this.state.discussions}
                    getChannels={this.getChannels.bind(this, 'Discussions')}
                    loadPosts={this.props.loadPosts}
                />
            </>
        )
    }
}

export default ChannelList
