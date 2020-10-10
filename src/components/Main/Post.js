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
                        <div className='UserName m-b-5'>
                            <h4>{item.name}</h4>
                        </div>
                        <div className='UserStatus'>
                            <p>{item.status}</p>
                        </div>
                    </div>
                </div>
                <div className='PostContent'>
                    <div className='PostMessage'>
                        <p>{item.message}</p>
                    </div>
                    <div className='PostImage m-b-20' />
                </div>
                {/*<form className='m-t-10 m-l-10 m-r-10'>
                    <input type='text' placeholder={this.props.placeHolder} />
                </form>*/}
            </div>
        )
    }
}

export default Post
