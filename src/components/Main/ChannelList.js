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
        this.getTopics();
        this.getAssignments();
    }

    getTopics = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/channels'
        })
        .then((response) => {
            console.log(response.data)
            this.setState({topics: response.data})
        })
        .catch((error) => {
            console.log(error)
        })
    }

    getAssignments = () => {
        const _this = this
        api({
            method: 'GET',
            url: '/groups/5f83e890d1bf28e13820a756/assignments'
        })
        .then((response) => {
            this.setState({assignments: response.data})
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
                    getChannels={this.getAssignments}
                    loadPosts={this.props.loadPosts}
                />
                <ChannelSection
                    channelLabel='Discussions'
                    channels={this.state.assignments}
                    getChannels={this.getAssignments}
                    loadPosts={this.props.loadPosts}
                />
            </>
        )
    }
}

export default ChannelList
