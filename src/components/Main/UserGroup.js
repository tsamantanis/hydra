import React, {Component} from 'react'

class UserGroup extends Component {
    render() {
        return(
            <div className='UserGroup m-t-15 m-b-15 m-l-15'>
                <h4 className="m-b-10">{this.props.groupTitle}</h4>
                { this.props.userItems.map((item) => {
                    return (
                        <div className='UserItem m-t-5'>
                            <div className='UserIcon' />
                            <div className='User m-l-10'>
                                <div className='UserName'>
                                    <h6 className='m-0'>{item.name}</h6>
                                </div>
                                <div className='UserStatus'>
                                    <p className='m-0'>{item.status}</p>
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
