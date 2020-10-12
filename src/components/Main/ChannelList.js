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

    componentDidMount() {
        this.getTopics()
        this.getDiscussions()
    }

    getChannels = (section) => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then((response) => {
            for (const channel of response.data) {
                if (channel.category === section) {
                    this.setState({section: [...this.state.section, channel]})
                }
            }
        })
        .catch((error) => {
            console.log(error)
        })
    }

    getTopics = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then((response) => {
            for (const channel of response.data) {
                if (channel.category === 'Topics') {
                    this.setState({topics: [...this.state.topics, channel]})
                }
            }
            console.log(this.state.topics)
        })
        .catch((error) => {
            console.log(error)
        })
    }

    getDiscussions = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then((response) => {
            for (const channel of response.data) {
                if (channel.category === 'Discussions') {
                    this.setState({discussions: [...this.state.discussions, channel]})
                }
            }
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
                    getChannels={this.getTopics}
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
                    getChannels={this.getDiscussions}
                    loadPosts={this.props.loadPosts}
                />
            </>
        )
    }
}

export default ChannelList
