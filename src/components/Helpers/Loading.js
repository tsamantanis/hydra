import React, {Component} from 'react'
class Loading extends Component {
    render() {
        return (
            <>
                <svg className="loading rotate" width="128.8" height="100" viewBox="0 0 1319 1024" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1134.78 459.537C1031.61 728.683 945.786 1078.17 659.779 993.507C494.495 944.578 183.483 776.198 183.483 532.115C183.483 288.032 448.745 17.5852 692.828 17.5852C936.911 17.5852 1134.78 215.454 1134.78 459.537Z" fill="#1CA0DE" fill-opacity="0.3"/>
                </svg>
                <svg className="loading rotate-left" width="128.8" height="100" viewBox="0 0 1319 1024" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1044.82 228.741C1090.05 513.412 1190.47 858.994 900.446 928.674C732.841 968.941 379.306 978.627 257.265 767.245C135.223 555.862 229.724 189.017 441.106 66.9757C652.488 -55.0658 922.782 17.3591 1044.82 228.741Z" fill="#4E47FF" fill-opacity="0.2"/>
                </svg>
                <svg className="loading rotate-slow" width="128.8" height="100" viewBox="0 0 1319 1024" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M261.835 778.306C228.596 491.988 142.772 142.495 435.464 85.0508C604.612 51.854 958.241 57.0168 1071.3 273.335C1184.36 489.654 1074.55 852.209 858.229 965.27C641.911 1078.33 374.896 994.625 261.835 778.306Z" fill="url(#paint0_linear)" fill-opacity="0.3"/>
                    <defs>
                        <linearGradient id="paint0_linear" x1="888.093" y1="949.661" x2="430.06" y2="73.3115" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#5EFC8D"/>
                            <stop offset="0.432292" stop-color="#0CBCD3"/>
                            <stop offset="0.567708" stop-color="#1CA0DE"/>
                            <stop offset="0.651042" stop-color="#268FE4"/>
                            <stop offset="1" stop-color="#4E47FF"/>
                        </linearGradient>
                    </defs>
                </svg>
            </>
        )
    }
}

export default Loading
