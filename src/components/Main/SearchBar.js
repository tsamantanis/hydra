import React, {Component} from 'react'
import './SearchBar.css'

class SearchBar extends Component {
    render() {
        return (
            <div className='SearchBar'>
                <form className='m-t-20 m-l-10 m-r-10 m-b-14'>
                    <input type='text' placeholder={this.props.placeHolder} />
                </form>
            </div>
        )
    }
}

export default SearchBar
