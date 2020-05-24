import React from 'react'
import TextField from '@material-ui/core/TextField';
import FormGroup from '@material-ui/core/FormGroup';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from "@material-ui/core/Grid";
import { Button } from '@material-ui/core';

function AlertsSettings() {

    const [email, setEmail] = React.useState('')
    const [checked, setChecked] = React.useState(false);
    const [number, setNumber] = React.useState('');


    const changeEmail = event => {
        setEmail(event.target.value);
    }
    const toggleChecked = () => {
        setChecked(prev => !prev);
    };
    const handleBlur = () => {
        if (number < 1) {
            setNumber(1);
        } else if (number > 100) {
            setNumber(100);
        }
    };
    const handleInputChange = event => {
        setNumber(event.target.value === "" ? "" : Number(event.target.value));
    }
    return (
        <React.Fragment>
         <div className="title">
            <h1>Alerts Settings</h1>
         </div>
         <div className="alert_email">
            <h2>Update Email Address: </h2>
            <TextField
                    id="fields"
                    label="E-mail"
                    onChange={changeEmail}
                    className={AlertsSettings.textField}
                    type="email"
                    name="email"
                    autoComplete="email"
                    margin="normal"
                    variant="outlined"
                        />
            <h5 style={{'margin-left' : '10px', 'margin-top' : '25px'}}>*Email is mutual for EU and B2MATCH</h5>
            
                <h3>Enable/Disable Alerts</h3>
                <FormGroup style={{ 'margin-top': '15px' }}>
                    <FormControlLabel
                        
                        control={
                        <Switch size="medium" checked={checked} onChange={toggleChecked} />
                                }
                        label="On"
                        style={{'margin-right' : '30px'}}
                    />
                </FormGroup>
         </div> 
         <div>
            <h1>B2MATCH</h1>
         </div>  
         <div className="res_score">
            <h3 style={{'margin-left' : '50px'}}>RES SCORE</h3>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div>
            <h1 style={{'margin-left' : '50px'}}>Countries Score</h1>
        </div>
        <div className="first_sc">
            <h2 style={{'margin-left' : '50px'}}>Italy</h2>
            <Grid container spacing={2} alignItems="center"  >
                            <Grid item>
                                <TextField
                                    style={{'width' : '40%'}}
                                    id="fields"
                                    label=""
                                    type="number"
                                    onChange={handleInputChange}
                                    onBlur={handleBlur}
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    variant="outlined"
                                />
                            </Grid>
                        </Grid>
            <h2>France</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Austria</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Germany</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="second_sc">
            <h2 style={{'margin-left' : '50px'}}>Denmark</h2>
            <Grid container spacing={2} alignItems="center"  >
                            <Grid item>
                                <TextField
                                    style={{'width' : '40%'}}
                                    id="fields"
                                    label=""
                                    type="number"
                                    onChange={handleInputChange}
                                    onBlur={handleBlur}
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    variant="outlined"
                                />
                            </Grid>
                        </Grid>
            <h2>Czech Republic</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Finland</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Ireland</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="third_sc">
            <h2 style={{'margin-left' : '50px'}}>Israel</h2>
            <Grid container spacing={2} alignItems="center"  >
                            <Grid item>
                                <TextField
                                    style={{'width' : '40%'}}
                                    id="fields"
                                    label=""
                                    type="number"
                                    onChange={handleInputChange}
                                    onBlur={handleBlur}
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    variant="outlined"
                                />
                            </Grid>
                        </Grid>
            <h2>Portugal</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Ukranie</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>United Kingdom</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="fourth_sc">
            <h2 style={{'margin-left' : '50px'}}>Turkey</h2>
            <Grid container spacing={2} alignItems="center"  >
                            <Grid item>
                                <TextField
                                    style={{'width' : '40%'}}
                                    id="fields"
                                    label=""
                                    type="number"
                                    onChange={handleInputChange}
                                    onBlur={handleBlur}
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    variant="outlined"
                                />
                            </Grid>
                        </Grid>
            <h2>Switzerland</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Spain</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Norway</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="line"></div>
        <div>
            <h1 style={{'margin-left' : '50px'}}>Types Scores</h1>
        </div>
        <div className="first_ty" style={{'margin-top' : '5px'}}>
            <h2 style={{'margin-left' : '50px'}}>Association/Agency</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>University</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Company</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="first_ty" style={{'margin-top' : '5px'}}>
            <h2 style={{'margin-left' : '50px'}}>R&D Institution</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Start-Up</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
            <h2>Others</h2>
            <Grid container spacing={2} alignItems="center"  >
                <Grid item>
                    <TextField
                            style={{'width' : '40%'}}
                            id="fields"
                            label=""
                            type="number"
                            onChange={handleInputChange}
                            onBlur={handleBlur}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="Buttons">
                <Button color="primary" round variant="contained" id="ButtonText">Update</Button>
            </div>
        </React.Fragment>
    )

}
export default AlertsSettings;
