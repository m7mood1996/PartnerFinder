import React from 'react'
import TextField from '@material-ui/core/TextField';
import FormGroup from '@material-ui/core/FormGroup';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from "@material-ui/core/Grid";
import { Button } from '@material-ui/core';
import Typography from '@material-ui/core/Typography'

function AlertsSettings() {

    const [email, setEmail] = React.useState('')
    const [checked, setChecked] = React.useState(false);
    const [number, setNumber] = React.useState();
    const [italy, setItaly] = React.useState();
    const [france, setFrance] = React.useState();
    const [austria, setAustria] = React.useState();
    const [germany, setGermany] = React.useState();
    const [denmark, setDenmark] = React.useState();
    const [czech, setCzech] = React.useState();
    const [finland, setFinland] = React.useState();
    const [ireland, setIreland] = React.useState();
    const [israel, setIsrael] = React.useState();
    const [portugal, setPortugal] = React.useState();
    const [ukranie, setUkranie] = React.useState();
    const [uk, setUK] = React.useState();
    const [turkey, setTurkey] = React.useState();
    const [switzerland, setSwitzerland] = React.useState();
    const [spain, setSpain] = React.useState();
    const [norway, setNorway] = React.useState();
    const [agency, setAgency] = React.useState();
    const [uni, setUni] = React.useState();
    const [company, setCompany] = React.useState();
    const [RD, setRD] = React.useState();
    const [start, setStart] = React.useState();
    const [oth, setOth] = React.useState();
    const [formState, setFormState] = React.useState({

    number:false,
    italy:false,
    france:false,
    austria:false,
    germany:false,
    denmark:false,
    czech:false,
    finland:false,
    ireland:false,
    israel:false,
    portugal:false,
    ukranie:false,
    uk:false,
    turkey:false,
    switzerland:false,
    spain:false,
    norway:false,
    agency:false,
    uni:false,
    company:false,
    RD:false,
    start:false,
    oth:false,
    })

    const changeEmail = event => {
        setEmail(event.target.value);
    }
    const toggleChecked = () => {
        setChecked(prev => !prev);
    };
    
    const handleInputChange = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setNumber(event.target.value);
            setFormState({...formState,number:true})
        }
        else{
            setNumber(event.target.value);
            setFormState({...formState,number:false})
        }
    }
    const handleItaly = event => {
        if(event.target.value > 1 || event.target.value < 0) {
            setItaly(event.target.value)
            setFormState({...formState,italy:true})
        }
        else{
            setItaly(event.target.value)
            setFormState({...formState,italy:false})
        }
    }
    const handleFrance = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setFrance(event.target.value)
            setFormState({...formState,france:true})
        }
        else{
            setFrance(event.target.value)
            setFormState({...formState,france:false})
        }
    }
    const handleAustria = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setAustria(event.target.value)
            setFormState({...formState,austria:true})
        }
        else{
            setAustria(event.target.value)
            setFormState({...formState,austria:false})
        }
    }
    const handleGermany = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setGermany(event.target.value)
            setFormState({...formState,germany:true})
        }
        else{
            setGermany(event.target.value)
            setFormState({...formState,germany:false})
        }
    }
    const handleDenmark= event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setDenmark(event.target.value)
            setFormState({...formState,denmark:true})
        }
        else{
            setDenmark(event.target.value)
            setFormState({...formState,denmark:false})
        }
    }
    const handleCzech = event => {
       
        if(event.target.value > 1 || event.target.value < 0) {
            setCzech(event.target.value)
            setFormState({...formState,czech:true})
        }
        else{
            setCzech(event.target.value)
            setFormState({...formState,czech:false})
        }
    }
    const handleFinland = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setFinland(event.target.value)
            setFormState({...formState,finland:true})
        }
        else{
            setFinland(event.target.value)
            setFormState({...formState,finland:false})
        }
    }
    const handleIreland = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setIreland(event.target.value)
            setFormState({...formState,ireland:true})
        }
        else{
            setIreland(event.target.value)
            setFormState({...formState,ireland:false})
        }
    }
    const handleIsrael = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setIsrael(event.target.value)
            setFormState({...formState,israel:true})
        }
        else{
            setIsrael(event.target.value)
            setFormState({...formState,israel:false})
        }
    }
    const handlePortugal = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setPortugal(event.target.value)
            setFormState({...formState,portugal:true})
        }
        else{
            setPortugal(event.target.value)
            setFormState({...formState,portugal:false})
        }
    }
    const handleUkranie = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setUkranie(event.target.value)
            setFormState({...formState,ukranie:true})
        }
        else{
            setUkranie(event.target.value)
            setFormState({...formState,ukranie:false})
        }
    }
    const handleUK = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setUK(event.target.value)
            setFormState({...formState,uk:true})
        }
        else{
            setUK(event.target.value)
            setFormState({...formState,uk:false})
        }
    }
    const handleTurkey = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setTurkey(event.target.value)
            setFormState({...formState,turkey:true})
        }
        else{
            setTurkey(event.target.value)
            setFormState({...formState,turkey:false})
        }
    }
    const handleSwitzerland = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setSwitzerland(event.target.value)
            setFormState({...formState,switzerland:true})
        }
        else{
            setSwitzerland(event.target.value)
            setFormState({...formState,switzerland:false})
        }
    }
    const handleSpain = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setSpain(event.target.value)
            setFormState({...formState,spain:true})
        }
        else{
            setSpain(event.target.value)
            setFormState({...formState,spain:false})
        }
    }
    const handleNorway = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setNorway(event.target.value)
            setFormState({...formState,norway:true})
        }
        else{
            setNorway(event.target.value)
            setFormState({...formState,norway:false})
        }
    }
    const handleAgency = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setAgency(event.target.value)
            setFormState({...formState,agency:true})
        }
        else{
            setAgency(event.target.value)
            setFormState({...formState,agency:false})
        }
    }
    const handleUni = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setUni(event.target.value)
            setFormState({...formState,uni:true})
        }
        else{
            setUni(event.target.value)
            setFormState({...formState,uni:false})
        }
    }
    const handleCompany= event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setCompany(event.target.value)
            setFormState({...formState,company:true})
        }
        else{
            setCompany(event.target.value)
            setFormState({...formState,company:false})
        }
    }
    const handleRD = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setRD(event.target.value)
            setFormState({...formState,RD:true})
        }
        else{
            setRD(event.target.value)
            setFormState({...formState,RD:false})
        }
    }
    const handleStartUp = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setStart(event.target.value)
            setFormState({...formState,start:true})
        }
        else{
            setStart(event.target.value)
            setFormState({...formState,start:false})
        }
    }
    const handleOTH = event => {
        
        if(event.target.value > 1 || event.target.value < 0) {
            setOth(event.target.value)
            setFormState({...formState,oth:true})
        }
        else{
            setOth(event.target.value)
            setFormState({...formState,oth:false})
        }
    }

    const formValidation = () => {

        let res = {}
        let check = false;
        if(number < 0 || number > 1)
        {
            res = { ...res, number: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, number: false }
        }
        if(italy < 0 || italy > 1)
        {
            res = { ...res, italy: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, italy: false }
        }
        if(france < 0 || france > 1)
        {
            res = { ...res, france: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, france: false }
        }
        if(austria < 0 || austria > 1)
        {
            res = { ...res, austria: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, austria: false }
        }
        if(germany < 0 || germany > 1)
        {
            res = { ...res, germany: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, germany: false }
        }
        if(denmark < 0 || denmark > 1)
        {
            res = { ...res, denmark: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, denmark: false }
        }
        if(czech < 0 || czech > 1)
        {
            res = { ...res, czech: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, czech: false }
        }
        if(finland < 0 || finland > 1)
        {
            res = { ...res, finland: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, finland: false }
        }
        if(ireland < 0 || ireland > 1)
        {
            res = { ...res, ireland: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, ireland: false }
        }
        if(israel < 0 || israel > 1)
        {
            res = { ...res, israel: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, israel: false }
        }
        if(portugal < 0 || portugal > 1)
        {
            res = { ...res, portugal: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, portugal: false }
        }
        if(ukranie < 0 || ukranie > 1)
        {
            res = { ...res, ukranie: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, ukranie: false }
        }
        if(uk < 0 || uk > 1)
        {
            res = { ...res, uk: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, uk: false }
        }
        if(turkey < 0 || turkey > 1)
        {
            res = { ...res, turkey: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, turkey: false }
        }
        if(switzerland < 0 || switzerland > 1)
        {
            res = { ...res, switzerland: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, switzerland: false }
        }
        if(spain < 0 || spain > 1)
        {
            res = { ...res, spain: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, spain: false }
        }
        if(norway < 0 || norway > 1)
        {
            res = { ...res, norway: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, norway: false }
        }
        if(agency < 0 || agency > 1)
        {
            res = { ...res, agency: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, agency: false }
        }
        if(uni < 0 || uni > 1)
        {
            res = { ...res, uni: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, uni: false }
        }
        if(company < 0 || company > 1)
        {
            res = { ...res, company: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, company: false }
        }
        if(RD < 0 || RD > 1)
        {
            res = { ...res, RD: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, RD: false }
        }
        if(start < 0 || start > 1)
        {
            res = { ...res, start: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, start: false }
        }
        if(oth < 0 || oth > 1)
        {
            res = { ...res, oth: true }
            setFormState(res)
            check = true;
        }
        else
        {
            res = { ...res, oth: false }
        }
        setFormState(res)
        return check;
    }

    const updateAlert = () => {
        console.log("form is " + formValidation());
        if(formValidation()){
            alert("Scores must be between 0 and 1")
        }
        else {
            console.log("It's Done");
        }
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
                            error={formState.number}
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
                                    min="0"
                                    max="1"
                                    onChange={handleItaly}
                                    error={formState.italy}
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
                            onChange={handleFrance}
                            error={formState.france}
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
                            onChange={handleAustria}
                            error={formState.austria}
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
                            onChange={handleGermany}
                            error={formState.germany}
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
                                    onChange={handleDenmark}
                                    error={formState.denmark}
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
                            onChange={handleCzech}
                            error={formState.czech}
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
                            onChange={handleFinland}
                            error={formState.finland}
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
                            onChange={handleIreland}
                            error={formState.ireland}
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
                                    onChange={handleIsrael}
                                    error={formState.israel}
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
                            onChange={handlePortugal}
                            error={formState.portugal}
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
                            onChange={handleUkranie}
                            error={formState.ukranie}
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
                            onChange={handleUK}
                            error={formState.uk}
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
                                    onChange={handleTurkey}
                                    error={formState.turkey}
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
                            onChange={handleSwitzerland}
                            error={formState.switzerland}
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
                            onChange={handleSpain}
                            error={formState.spain}
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
                            onChange={handleNorway}
                            error={formState.norway}
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
                            onChange={handleAgency}
                            error={formState.agency}
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
                            onChange={handleUni}
                            error={formState.uni}
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
                            onChange={handleCompany}
                            error={formState.company}
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
                            onChange={handleRD}
                            error={formState.RD}
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
                            onChange={handleStartUp}
                            error={formState.start}
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
                            onChange={handleOTH}
                            error={formState.oth}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            variant="outlined"
                            />
                </Grid>
            </Grid>
        </div>
        <div className="Buttons">
                <Button color="primary" round variant="contained" id="ButtonText" onClick={() => updateAlert()}>Update</Button>
            </div>
        
        </React.Fragment>
    )
}
export default AlertsSettings;