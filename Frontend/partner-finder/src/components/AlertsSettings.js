import React from "react";
import TextField from "@material-ui/core/TextField";
import FormGroup from "@material-ui/core/FormGroup";
import Switch from "@material-ui/core/Switch";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Grid from "@material-ui/core/Grid";
import { Button } from "@material-ui/core";
import CallsResultsTable from "./CallsResultsTable";
import moment from "moment";
import { Msgtoshow } from "./Msgtoshow";
import ResultsTable from "./ResultsTable";
import { BeatLoader } from "react-spinners";
import {
  makeStyles,
  Dialog,
  DialogTitle,
  DialogContent,
} from "@material-ui/core/";
import { BACKEND_URL } from "../utils";

const calls_columns = [
  { title: "Title", field: "title" },
  { title: "Call Title", field: "callTitle" },
  { title: "Identifier", field: "identifier" },
  { title: "Type", field: "type" },
  { title: "Status", field: "status" },
  { title: "Deadline Date", field: "deadlineDate" },
  { title: "Submission Procedure Role", field: "sumbissionProcedure" },
];

const useStyles = makeStyles((theme) => ({
  title: {
    textAlign: "center",
    fontSize: 30,
  },
}));

const events_columns = [
  { title: "Name", field: "event_name" },
  {
    title: "URL",
    field: "event_url",
    render: (rowData) => (
      <a href={rowData.event_url} style={{color: "white"}} target="_blank" rel="noopener noreferrer">
        {rowData.event_url}{" "}
      </a>
    ),
  },
];

function AlertsSettings(props) {
  const classes = useStyles();
  const [msgState, setMsgState] = React.useState({
    title: "",
    body: "",
    visible: false,
  });
  const [turned_on, setturned_on] = React.useState(false);
  const [state, setState] = React.useState({
    firstLoading: true,
    loading: false,
    email: "",
    resScore: 0,
    italy: 0,
    france: 0,
    austria: 0,
    germany: 0,
    denmark: 0,
    czech: 0,
    finland: 0,
    ireland: 0,
    israel: 0,
    portugal: 0,
    ukranie: 0,
    uk: 0,
    turkey: 0,
    switzerland: 0,
    spain: 0,
    norway: 0,
    agency: 0,
    university: 0,
    company: 0,
    RD: 0,
    start_up: 0,
    other: 0,
    calls: [],
    events: [],
  });
  const [formState, setFormState] = React.useState({
    email: false,
    resScore: false,
    italy: false,
    france: false,
    austria: false,
    germany: false,
    denmark: false,
    czech: false,
    finland: false,
    ireland: false,
    israel: false,
    portugal: false,
    ukranie: false,
    uk: false,
    turkey: false,
    switzerland: false,
    spain: false,
    norway: false,
    agency: false,
    university: false,
    company: false,
    RD: false,
    start_up: false,
    other: false,
  });

  if (state.firstLoading) {
    let newState = { ...props.state };
    setturned_on(newState.turned_on);
    delete newState["turned_on"];
    newState["calls"] = [];
    newState["events"] = [];
    setState(newState);
  }

  /**
   * Method that change the state of the switch key from on to off or the opposite
   */
  const toggleChecked = () => {
    let temp = false;
    setturned_on((prev) => {
      temp = !prev;
      return temp;
    });
    props.setState({ ...props.state, turned_on: temp });
  };

  /**
   * Method that hides the alerts table 
   */
  const hideAlerts = () => {
    setState({ ...state, events: [], calls: [] });
  };
  
  /**
   * 
   */
  const getCalls = () => {
    setState({ ...state, loading: true });
    let url = new URL(BACKEND_URL + "calls/get_calls/");
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ("error" in resp) {
          setMsgState({
            title: "Failed",
            body: "Error while uploading alerts results",
            visible: true,
          });
          setState({ ...state, loading: false, calls: [] });
        } else {
          let calls = resp["calls"].map((call) => {
            call["deadlineDate"] = moment
              .unix(call.deadlineDate)
              .format("DD/MM/YYYY");
            return call;
          });
          setState({ ...state, calls });
          url = new URL(BACKEND_URL + "b2matchalerts/getEventFromAlerts/");
          fetch(url, {
            method: "GET",
          })
            .then((res) => res.json())
            .then((resp) => {
              if ("error" in resp) {
                setMsgState({
                  title: "Failed",
                  body: "Error while uploading alerts results",
                  visible: true,
                });
                setState({ ...state, loading: false, events: [] });
              } else {
                setState({ ...state, loading: false });
                setState({ ...state, calls, events: resp });
              }
            })
            .catch((error) => {
              setMsgState({
                title: "Failed",
                body: "Error while uploading alerts results",
                visible: true,
              });
              setState({ ...state, events: [] });
            });
        }
      })
      .catch((error) => {
        setMsgState({
          title: "Failed",
          body: "Error while uploading alerts results",
          visible: true,
        });
        setState({ ...state, loading: false, calls: [] });
      });
  };
  
  /**
   * Method that sets the value of the scores that has been entered 
   * @param {*} event event when the user to enter a new score
   */
  const handleInputChange = (event) => {
  
    let newState = { ...state };
    newState[event.target.id] = event.target.value;
    setState(newState);
    props.setState({ ...props.state, ...newState });
    let newFormState = { ...formState };
    if (
      event.target.id !== "email" &&
      (event.target.value > 1 || event.target.value < 0)
    ) {
      newFormState[event.target.id] = true;
    } else {
      newFormState[event.target.id] = false;
    }
    setFormState(newFormState);
  };

  /**
   *Method that checks if all the input fields has been
    filled with the approriate values
   */
  const formValidation = () => {
    let res = {};
    let check = false;
    Object.keys(state).forEach((key) => {
      if (key !== 'email' && key !== 'calls' && key !== 'events') {
        if (state[key] < 0 || state[key] > 1 || state[key].length === 0 || state[key] === undefined || state[key] === null) {
          res[key] = true;
          check = true;
        } else {
          res[key] = false;
        }
      } else if (key === 'email') {
        if (!state[key].match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i)) {
          res[key] = true;
          check = true;
        } else {
          res[key] = false;
        }
      }
    });
    console.log(res);
    setFormState(res);
    return check;
  };

  /**
   * Method that updates the scores that the user want to change them in our DB  
     with the new value that was inserted
   */
  const updateAlert = () => {
    if (formValidation()) {
      console.log(formState);
      if (formState.email) {
        console.log("Invalid Email");
        setMsgState({
          title: "Failed",
          body: "Invalid Email",
          visible: true,
        });
      } else {
        setMsgState({
          title: "Failed",
          body: "Scores must be between 0 and 1",
          visible: true,
        });
      }
    } else {
      setState({ ...state, loading: true });
      let url = new URL(BACKEND_URL + "alerts/set_settings/");
      let params = {
        data: JSON.stringify({ email: state.email, turned_on: turned_on }),
      };
      Object.keys(params).forEach((key) =>
        url.searchParams.append(key, params[key])
      );
      fetch(url, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((resp) => {
          if ("error" in resp) {
            setMsgState({
              title: "Failed",
              body: "Error while updating alerts settings",
              visible: true,
            });
            setState({ ...state, loading: false });
          } else {
            props.setState({
              ...props.state,
              email: state.email,
              turned_on: turned_on,
            });
            url = new URL(BACKEND_URL + "scores/updatescores/");
            let data = {
              RES: state.resScore,
              Italy: state.italy,
              France: state.france,
              Austria: state.austria,
              Germany: state.germany,
              Denmark: state.denmark,
              Czech_Republic: state.czech,
              Finland: state.finland,
              Ireland: state.ireland,
              Israel: state.israel,
              Portugal: state.portugal,
              Ukranie: state.ukranie,
              United_Kingdom: state.uk,
              Turkey: state.turkey,
              Switzerland: state.switzerland,
              Spain: state.spain,
              Norway: state.norway,
              Association_Agency: state.agency,
              University: state.university,
              Company: state.company,
              R_D_Institution: state.RD,
              Start_Up: state.start_up,
              Others: state.other,
            };
            params = { data: JSON.stringify(data) };
            Object.keys(params).forEach((key) =>
              url.searchParams.append(key, params[key])
            );
            fetch(url, {
              method: "POST",
            })
              .then((res) => res.json())
              .then((resp) => {
                if ("error" in resp) {
                  setMsgState({
                    title: "Failed",
                    body: "Error while updating alerts settings",
                    visible: true,
                  });
                  setState({ ...state, loading: false });
                } else {
                  props.setState({ ...props.state, ...state });
                  setState({ ...state, loading: false });
                  setMsgState({
                    title: "Success",
                    body: "Alerts settings has been updated successfully",
                    visible: true,
                  });
                }
              })
              .catch((error) => {
                setMsgState({
                  title: "Failed",
                  body: "Error while updating alerts settings",
                  visible: true,
                });
                setState({ ...state, loading: false });
              });
          }
        })
        .catch((error) => {
          setMsgState({
            title: "Failed",
            body: "Error while updating alerts settings",
            visible: true,
          });
          setState({ ...state, loading: false });
        });
    }
  };

  /**
   * function that updates the alert results in the EU & B2MATCH manually 
   */
  const updateAlertResults = () => {
    
    let url = new URL(BACKEND_URL + "calls/consortium_builder/");
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ("error" in resp) {
          setMsgState({
            title: "Failed",
            body: "Error while updating alerts results",
            visible: true,
          });
        }    
      })
      .catch((error) => {
        setMsgState({
          title: "Failed",
          body: "Error while updating alerts results",
          visible: true,
        });
      });
      url = new URL(BACKEND_URL + "alerts/alertB2match");
      fetch(url, {
        method: "GET",
      })
        .then((res) => res.json())
        .then((resp) => {
          if ("error" in resp) {
            setMsgState({
              title: "Failed",
              body: "Error while updating alerts results",
              visible: true,
            });
          }       
        })
        .catch((error) => {
          setMsgState({
            title: "Failed",
            body: "Error while updating alerts results",
            visible: true,
          });
        });
  };
  return (
    <React.Fragment>
      <Msgtoshow
        {...msgState}
        handleClose={() => setMsgState({ ...msgState, visible: false })}
      />
      <div className="title">
        <h1 id="textFontFamily">Alerts Settings</h1>
      </div>
      <div
        style={{ marginBottom: "30px", marginLeft: "50px" }}
        className="alert_email"
      >
        <h2 style={{marginTop:'25px'}} id="textFontFamily">E-mail</h2>
        <TextField
          id="email"
          style={{
            borderRadius: "3px",
            backgroundColor: "#02203c",
            marginBottom: "45px"
          }}
          onChange={handleInputChange}
          className={AlertsSettings.textField}
          type={state.email}
          name={state.email}
          value={state.email}
          error={formState.invalidemail}
          autoComplete="email"
          margin="normal"
          variant="outlined"
        />

        <h3
          style={{
            "margin-left": "10px",
            "margin-top": "35px",
            fontWeight: "bold",
          }}
          id="textFontFamily"
        >
          ** Email is mutual for B2MATCH & EU **
        </h3>
        <h2
          style={{
            marginLeft: "10px",
            // "margin-top": "35px",
            fontWeight: "bold",
          }}
          id="textFontFamily"
        >
          Enable/Disable Alerts
        </h2>
        <FormGroup style={{ "margin-top": "20px", color: "#02203c" }}>
          <FormControlLabel
            control={
              <Switch
                id="BackgroundColor"
                size="medium"
                checked={turned_on}
                onChange={toggleChecked}
                style={{ color: "#02203c" }}
              />
            }
            label="On"
            style={{
              color: "#02203c",
            }}
          />
        </FormGroup>
      </div>
      <div>
        <h1 id="textFontFamily">B2MATCH</h1>
      </div>
      <div className="res_score">
        <h2
          style={{
            "margin-left": "50px",
          }}
          id="textFontFamily"
        >
          RES SCORE
        </h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="resScore"
              label=""
              value={state.resScore}
              onChange={handleInputChange}
              error={formState.resScore}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div>
        <h1 style={{ "margin-left": "30px" }} id="textFontFamily">
          Countries Score
        </h1>
      </div>
      <div className="countries_scores">
        <h2 style={{ "margin-left": "50px" }} id="textFontFamily">
          Italy
        </h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="italy"
              label=""
              value={state.italy}
              onChange={handleInputChange}
              error={formState.italy}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>

        <h2 id="textFontFamily">France</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="france"
              label=""
              value={state.france}
              onChange={handleInputChange}
              error={formState.france}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Austria</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="austria"
              label=""
              value={state.austria}
              onChange={handleInputChange}
              error={formState.austria}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div className="countries_scores">
        <h2 style={{ "margin-left": "50px" }}>Denmark</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="denmark"
              label=""
              value={state.denmark}
              onChange={handleInputChange}
              error={formState.denmark}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Czech Republic</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="czech"
              label=""
              value={state.czech}
              onChange={handleInputChange}
              error={formState.czech}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Finland</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="finland"
              label=""
              value={state.finland}
              onChange={handleInputChange}
              error={formState.finland}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div className="countries_scores">
        <h2 style={{ "margin-left": "50px" }}>Israel</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="israel"
              label=""
              value={state.israel}
              onChange={handleInputChange}
              error={formState.israel}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Portugal</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="portugal"
              value={state.portugal}
              onChange={handleInputChange}
              error={formState.portugal}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Ukraine</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="ukranie"
              value={state.ukranie}
              onChange={handleInputChange}
              error={formState.ukranie}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div className="countries_scores">
        <h2 style={{ "margin-left": "50px" }}>Turkey</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="turkey"
              label=""
              value={state.turkey}
              onChange={handleInputChange}
              error={formState.turkey}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Switzerland</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="switzerland"
              label=""
              value={state.switzerland}
              onChange={handleInputChange}
              error={formState.switzerland}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Spain</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="spain"
              label=""
              value={state.spain}
              onChange={handleInputChange}
              error={formState.spain}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div className="countries_scores">
        <h2 style={{ "margin-left": "50px" }}>Germany</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="germany"
              label=""
              value={state.germany}
              onChange={handleInputChange}
              error={formState.germany}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Ireland</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="ireland"
              label=""
              value={state.ireland}
              onChange={handleInputChange}
              error={formState.ireland}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>United Kingdom</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="uk"
              label=""
              value={state.uk}
              onChange={handleInputChange}
              error={formState.uk}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div className="countries_scores">
        <h2 style={{ "margin-left": "50px" }}>Norway</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="norway"
              label=""
              value={state.norway}
              onChange={handleInputChange}
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
        <h1 style={{ "margin-left": "30px" }}>Types Scores</h1>
      </div>
      <div className="first_ty" style={{ "margin-top": "5px" }}>
        <h2 style={{ "margin-left": "50px" }}>Association/Agency</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="agency"
              label=""
              value={state.agency}
              onChange={handleInputChange}
              error={formState.agency}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>University</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="university"
              label=""
              value={state.university}
              onChange={handleInputChange}
              error={formState.university}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Company</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "40%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="company"
              label=""
              value={state.company}
              onChange={handleInputChange}
              error={formState.company}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>
      <div className="first_ty" style={{ "margin-top": "5px" }}>
        <h2 style={{ "margin-left": "50px" }}>R&D Institution</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "41%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="RD"
              label=""
              value={state.RD}
              onChange={handleInputChange}
              error={formState.RD}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Start-Up</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "41%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="start_up"
              label=""
              value={state.start_up}
              onChange={handleInputChange}
              error={formState.start_up}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
        <h2>Others</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{
                width: "41%",
                borderRadius: "3px",
                backgroundColor: "#02203c",
              }}
              id="other"
              label=""
              value={state.other}
              onChange={handleInputChange}
              error={formState.other}
              InputLabelProps={{
                shrink: true,
              }}
              variant="outlined"
            />
          </Grid>
        </Grid>
      </div>

      <div className="Buttons">
        <Button
          color="primary"
          round
          variant="contained"
          id="BackgroundColor"
          onClick={() => updateAlert()}
        >
          Update Scores
        </Button>

        <Button
          color="primary"
          round
          variant="contained"
          id="BackgroundColor"
          style={{'marginLeft' : '10%'}}
          onClick={() => updateAlertResults()}
        >
          Update Alerts Results
        </Button>
      </div>

      <div className="Buttons">
        <Button
          id="BackgroundColor"
          color="primary"
          round
          variant="contained"
          onClick={() => getCalls()}
        >
          Show Alerts Results
        </Button>
      </div>

      <div style={{ "margin-top": "10px" }}>
        {state && state.calls && state.calls.length === 0 ? null : (
          <CallsResultsTable
            title={"EU Proposal Calls"}
            columns={calls_columns}
            data={state.calls}
          />
        )}
      </div>
      <div style={{ "margin-top": "10px" }}>
        {state && state.events && state.events.length === 0 ? null : (
          <ResultsTable
            title={"B2match Recommended Events"}
            columns={events_columns}
            data={state.events}
          />
        )}
      </div>
      <div className="Buttons">
        {state &&
        ((state.events && state.events.length !== 0) ||
          (state.calls && state.calls.length !== 0)) ? (
          <Button
            color="secondary"
            round
            id="exitColor"
            variant="contained"
            onClick={() => hideAlerts()}
          >
            Hide Alerts Results
          </Button>
        ) : null}
      </div>
      {state && state.loading ? (
        <Dialog
          disableBackdropClick
          disableEscapeKeyDown
          open={true}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle className={classes.title}>LOADING</DialogTitle>
          <DialogContent style={{ "margin-left": "17px" }}>
            <BeatLoader />
          </DialogContent>
        </Dialog>
      ) : null}
    </React.Fragment>
  );
}
export default AlertsSettings;
