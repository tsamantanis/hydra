import React, {Component} from 'react'
import './SearchBar.css'

class SearchBar extends Component {
    render() {
        return (
            <div className='SearchBar'>
                <form className='m-t-10 m-l-10 m-r-10'>
                    <input type='text' placeholder={this.props.placeHolder} />
                </form>
            </div>
        )
    }
}

export default SearchBar
