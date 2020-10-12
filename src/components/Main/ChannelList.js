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
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then((response) => {
            console.log(section)
            for (const channel of response.data) {
                if (channel.category === section) {
                    this.setState({section: [...this.state.section, channel.name]})
                }
            }
            console.log(this.state.section)
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
                    channels={this.state.assignments}
                    getChannels={this.getChannels.bind(this, 'Discussions')}
                    loadPosts={this.props.loadPosts}
                />
            </>
        )
    }
}

export default ChannelList
