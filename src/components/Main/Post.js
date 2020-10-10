import React, {Component} from 'react'

class Post extends Component {
    render() {
        return (
            <div className='Post'>
                <form className='m-t-10 m-l-10 m-r-10'>
                    <input type='text' placeholder={this.props.placeHolder} />
                </form>
            </div>
        )
    }
}

export default Post
