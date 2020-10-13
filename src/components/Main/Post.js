import React, {Component} from 'react'
import './Post.css'
class Post extends Component {
    render() {
        let item = {
            name: "Jon Snow",
            status: "Active",
            message: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur imperdiet sapien id lorem iaculis sollicitudin. Morbi sit amet interdum leo, in blandit sapien. Vivamus a scelerisque ligula. Sed tellus nibh, eleifend eu ex non, consequat pretium est. Nulla venenatis ex vel nisl tempor volutpat.",
            photo: ""

        }
        return (
            <div className='Post'>
                <div className='UserItem m-b-20'>
                    <div className='UserIcon' />
                    <div className='User m-l-10'>
                        <div className='UserName m-t-20'>
                            <h4>{this.props.post.ownerName}</h4>
                        </div>
                        <div className='UserStatus'>
                            <p>5 min ago</p>
                        </div>
                    </div>
                </div>
                <div className='PostContent'>
                    <div className='PostMessage m-b-10'>
                        <p>{this.props.post.dis}</p>
                    </div>
                    <div className='PostImage m-b-20' />
                </div>
                <hr />
                <div className='PostComments m-t-20 m-b-20'>
                    <div className='UserItem'>
                        <div className='UserIcon' />
                        <div className="UserComment">
                            <p>{this.props.post.dis}</p>
                        </div>
                    </div>
                </div>
                <hr />
                <div className="AddComment m-t-20">
                    <div className='UserItem'>
                        <div className='UserIcon' />
                        <input type="text" className="NewComment" placeholder="Comment on this thread" />
                    </div>
                </div>
                {/*<form className='m-t-10 m-l-10 m-r-10'>
                    <input type='text' placeholder={this.props.placeHolder} />
                </form>*/}
            </div>
        )
    }
}

export default Post
