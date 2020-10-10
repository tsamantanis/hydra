import React, {Component} from 'react'

class UserGroup extends Component {
    render() {
        return(
            <div className='UserGroup'>
                <h4 className="m-b-20">{this.props.groupTitle}</h4>
                { this.props.userItems.map((item) => {
                    return (
                        <div className='UserItem m-b-10'>
                            <div className='UserIcon' />
                            <div className='User m-t-n20'>
                                <div className='UserName'>
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
