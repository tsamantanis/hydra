import React, {Component} from 'react'

class UserGroup extends Component {
    render() {
        return(
            <div className='UserGroup m-t-15 m-b-15 m-l-15'>
                <h4 className="m-b-30">{this.props.groupTitle}</h4>
                { this.props.userItems.map((item) => {
                    return (
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
                    )
                })}
            </div>
        );
    }
}

export default UserGroup
