import React, { Component } from "react";
import { render } from "react-dom";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";

export default class AddRecipeBtn extends Component {
    constructor(props) {
        super(props);
    }

    handleClick() {
        console.log("Heh");
    }

    render() {
        return (
            <Button color="primary" variant="contained">
                primary
            </Button>
            /*
            <button onClick={handleClick}>
                Activate Lasers
            </button>
            */
        );
    }
}

const appDiv = document.getElementById("app");
render(<AddRecipeBtn />, appDiv);

/*
export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <h1>Hi. Please Send Help.</h1>;
    }
}
*/

