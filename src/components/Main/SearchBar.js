import React, {Component} from 'react'

class SearchBar extends Component {
    render() {
        return (
            <div className='SearchBar m-t-10'>
                <form>
                    <input type='text' placeholder={this.props.placeHolder} />
                </form>
            </div>
        )
    }
}

export default SearchBar
