import React, { Component } from 'react';
import { render } from 'react-dom';

export default class Dashboard extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return <h1>Hello React</h1>
    }
}

const dashDiv = document.getElementById("dash");
render(<Dashboard />, dashDiv);
