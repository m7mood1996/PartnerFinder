import React from 'react';
import { Button } from '@material-ui/core';
import moment from 'moment'

function Updates() {

    const [state, setState] = React.useState({
        'EU': 0,
        'B2MATCH': 0,
        'firstLoading': true
    })

    if (state.firstLoading) {
        let url = new URL('http://127.0.0.1:8000/api/updates/getSettings/')
        fetch(url, {
            method: 'GET'
        }).then(res => res.json())
            .then(resp => {
                // TODO: show successful message
                console.log("GET SETTINGS", resp)
                setState({ ...state, 'EU': moment.unix(resp.EU).format('MMMM Do YYYY, h:mm:ss a'), 'B2MATCH': moment.unix(resp.B2MATCH).format('MMMM Do YYYY, h:mm:ss a'), 'firstLoading': false })
            })
            // TODO: show error message
            .catch(error => console.log(error))
    }


    const updateB2match = event => {

        let url = new URL('http://127.0.0.1:8000/api/events/update_upcoming_events/')
        fetch(url, {
            method: 'POST'
        }).then(res => res.json())
            .then(resp => {
                // TODO: show successful message
                console.log("GET SETTINGS", resp)

            })
            // TODO: show error message
            .catch(error => console.log(error))
    }

    const updateEU = event => {

        let url = new URL('http://127.0.0.1:8000/api/organizations/updateOrganizations/')
        fetch(url, {
            method: 'GET'
        }).then(res => res.json())
            .then(resp => {
                // TODO: show successful message
                console.log("GET SETTINGS", resp)

            })
            // TODO: show error message
            .catch(error => console.log(error))

    }

    return (
        <React.Fragment>
            <div>
                <h1>Updates</h1>
            </div>
            <div style={{ 'margin-top': '50px' }}>
                <h1 style={{ 'margin-left': '50px' }}>B2MATCH</h1>
            </div>
            <div className="update">
                <h2 style={{ 'margin-left': '50px' }}>Last Update</h2>
                <h3>{state.B2MATCH}</h3>
            </div>
            <div style={{ 'margin-left': '50px', 'margin-top': '50px' }}>
                <Button color="primary" round variant="contained" id="ButtonText" onClick={updateB2match} style={{ 'width': '20%' }}>Update Now</Button>

            </div>
            <div style={{ 'margin-top': '50px' }}>
                <h1 style={{ 'margin-left': '50px' }}>EU</h1>
            </div>
            <div className="update">
                <h2 style={{ 'margin-left': '50px' }}>Last Update</h2>
                <h3>{state.EU}</h3>
            </div>
            <div style={{ 'margin-left': '50px', 'margin-top': '50px' }}>
                <Button color="primary" round variant="contained" id="ButtonText" onClick={updateEU} style={{ 'width': '20%' }}>Update Now</Button>
            </div>
            <div style={{ 'margin-top': '10%' }}>
                <h1 style={{ 'margin-left': '45px', 'color': 'blue', 'font-weight': 'bold' }}>*There is an automatically updates every month for both EU & B2MATCH</h1>
            </div>
        </React.Fragment>
    )
}
export default Updates;