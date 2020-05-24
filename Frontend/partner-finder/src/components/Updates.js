import React from 'react';
import { Button } from '@material-ui/core';


function Updates() {
    return (
        <React.Fragment>
            <div>
              <h1>Updates</h1>  
            </div>
            <div style={{'margin-top' : '50px'}}>
                <h1 style={{'margin-left' : '50px'}}>B2MATCH</h1>
            </div>
            <div className="update">
                <h2 style={{'margin-left':'50px'}}>Last Update</h2>
            </div>
            <div style={{'margin-left':'50px','margin-top':'50px'}}>
                <Button color="primary" round variant="contained" id="ButtonText" style={{'width':'20%'}}>Update Now</Button>
            </div>
            <div style={{'margin-top' : '50px'}}>
                <h1 style={{'margin-left' : '50px'}}>EU</h1>
            </div>
            <div className="update">
                <h2 style={{'margin-left':'50px'}}>Last Update</h2>
            </div>
            <div style={{'margin-left':'50px','margin-top':'50px'}}>
                <Button color="primary" round variant="contained" id="ButtonText" style={{'width':'20%'}}>Update Now</Button>
            </div>
            <div style={{'margin-top':'10%'}}>
                <h1 style={{'margin-left':'45px','color':'blue','font-weight':'bold'}}>*There is an automatically updates every two weeks for both EU & B2MATCH</h1>
            </div>
        </React.Fragment>
    )
}
export default Updates;