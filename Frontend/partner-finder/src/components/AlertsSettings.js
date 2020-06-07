import React from "react";
import TextField from "@material-ui/core/TextField";
import FormGroup from "@material-ui/core/FormGroup";
import Switch from "@material-ui/core/Switch";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Grid from "@material-ui/core/Grid";
import { Button } from "@material-ui/core";
import CallsResultsTable from "./CallsResultsTable";
import moment from "moment";
import { Msgtoshow } from "./Msgtoshow"
import ResultsTable from "./ResultsTable";
import { BeatLoader } from 'react-spinners'
import { makeStyles, Dialog, DialogTitle, DialogContent } from '@material-ui/core/';
const calls_columns = [
  { title: "Title", field: "title" },
  { title: "Call Title", field: "callTitle" },
  { title: "Identifier", field: "identifier" },
  { title: "Type", field: "type" },
  { title: "Status", field: "status" },
  { title: "Deadline Date", field: "deadlineDate" },
  { title: "Submission Procedure Role", field: "sumbissionProcedure" },
];

const useStyles = makeStyles(theme => ({
  title: {
    textAlign: 'center',
    fontSize: 30,
  },


}));

const events_columns = [
  { title: "Name", field: "event_name" },
  {
    title: "URL", field: "event_url", render: rowData => <a href={rowData.event_url} target="_blank">{rowData.event_url} </a>
  },
];

function AlertsSettings(props) {
  const classes = useStyles();
  const [msgState, setMsgState] = React.useState({ title: '', body: '', visible: false });
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
    uni: 0,
    company: 0,
    RD: 0,
    start: 0,
    oth: 0,
    calls: [],
    events: [],
  });
  const [formState, setFormState] = React.useState({
    valid_email: false,
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
    uni: false,
    company: false,
    RD: false,
    start: false,
    oth: false,
  });

  if (state.firstLoading) {
    let newState = { ...props.state };
    setturned_on(newState.turned_on);
    delete newState["turned_on"];
    newState["calls"] = [];
    newState['events'] = [];
    setState(newState);
  }

  const toggleChecked = () => {
    let temp = false;
    setturned_on((prev) => {
      temp = !prev;
      return temp
    });
    props.setState({ ...props.state, 'turned_on': temp })
  };

  const hideAlerts = () => {
    setState({ ...state, 'events': [], 'calls': [] })
  }
  const getCalls = () => {
    setState({ ...state, loading: true });
    let url = new URL("http://127.0.0.1:8000/api/calls/get_calls/");
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ("calls" in resp && resp.calls.length !== 0) {
          let calls = resp["calls"].map((call) => {
            call["deadlineDate"] = moment
              .unix(call.deadlineDate)
              .format("DD/MM/YYYY");
            return call;
          });
          setState({ ...state, calls });
          url = new URL("http://127.0.0.1:8000/api/b2matchalerts/getEventFromAlerts/");
          fetch(url, {
            method: "GET",
          })
            .then((res) => res.json())
            .then((resp) => {
              console.log("state is " + state.loading);
              // setState({ ...state, loading: false });
              setState({ ...state, calls, 'events': resp })
            })
            .catch((error) => {
              setMsgState({
                title: 'Error',
                body: 'Error while getting b2match events',
                visible: true
              });
              setState({ ...state, 'events': [] })
            });
        } else {
          setMsgState({
            title: 'Error',
            body: 'Error while getting organizations',
            visible: true
          });
        }
      })
      .catch((error) => {
        setMsgState({
          title: 'Error',
          body: 'Error while getting organizations',
          visible: true
        });
      });
  };

  const handleInputChange = (event) => {
    let newState = { ...state };
    newState[event.target.id] = event.target.value;
    setState(newState);
    props.setState({ ...props.state, ...newState })
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

  const formValidation = () => {
    let res = {};
    let check = false;
    Object.keys(state).forEach((key) => {
      if (key !== "email") {
        if (state[key] < 0 || state[key] > 1) {
          res[key] = true;
          check = true;
        } else {
          res[key] = false;
        }
      }
      else if (key === 'email') {
        if (!state[key].match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i)) {
          console.log("What the hell !!")
          setFormState({ ...formState, valid_email: true });
          console.log("state of email" + "\t" + formState.valid_email);
          check = true;
        }
        else {
          res[key] = false;
        }
      }
    });
    console.log(res);
    setFormState(res);
    return check;
  };

  const updateAlert = () => {
    if (formValidation()) {
      if (formState.valid_email) {
        console.log("Invalid Email");
        setMsgState({
          title: 'Failed',
          body: 'Invalid Email',
          visible: true
        });
      }
      else {
        console.log("form" + formState.valid_email);
        setMsgState({
          title: 'Failed',
          body: 'Scores must be between 0 and 1',
          visible: true
        });
      }

    } else {
      setState({ ...state, loading: true });
      let url = new URL("http://127.0.0.1:8000/api/alerts/setSettings/");
      let params = {
        data: JSON.stringify({ 'email': state.email, 'turned_on': turned_on }),
      };
      Object.keys(params).forEach((key) =>
        url.searchParams.append(key, params[key])
      );
      fetch(url, {
        method: "POST",
      })
        .then((res) => res.json())
        .then((resp) => {
          console.log("UPDATE SETTINGS", resp);
          props.setState({
            ...props.state,
            email: state.email,
            turned_on: turned_on,
          });
          url = new URL("http://127.0.0.1:8000/api/scores/updatescores/");
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
            University: state.uni,
            Company: state.company,
            R_D_Institution: state.RD,
            Start_Up: state.start,
            Others: state.oth,
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
              props.setState({ ...props.state, ...state });
              setState({ ...state, loading: false });
              setMsgState({
                title: 'Success',
                body: 'Alerts settings has been updated successfully',
                visible: true
              });

            })
            .catch((error) => {
              setMsgState({
                title: 'Error',
                body: 'Error while updating alerts settings',
                visible: true
              })
              setState({ ...state, loading: false });
            });
        })
        .catch((error) => {
          setMsgState({
            title: 'Error',
            body: 'Error while updating alerts settings',
            visible: true
          })
          setState({ ...state, loading: false });
        });
    }
  };

  return (
    <React.Fragment>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }}>
        <Msgtoshow {...msgState} handleClose={() => setMsgState({ ...msgState, visible: false })} />
      </div>
      <div className="title">
        <h1>Alerts Settings</h1>
      </div>
      <div className="alert_email">
        <TextField
          id="email"
          label="E-mail"
          onChange={handleInputChange}
          className={AlertsSettings.textField}
          type={state.email}
          name={state.email}
          value={state.email}
          error={formState.valid_email}
          autoComplete="email"
          margin="normal"
          variant="outlined"
        />

        <h3 style={{ 'margin-left': '14px', 'margin-top': '24px' }}>Enable/Disable Alerts</h3>
        <FormGroup style={{ "margin-top": "15px" }}>
          <FormControlLabel
            control={
              <Switch
                size="medium"
                checked={turned_on}
                onChange={toggleChecked}
              />
            }
            label="On"
            style={{ "margin-right": "30px" }}
          />
        </FormGroup>
      </div>
      <div>
        <h1>B2MATCH</h1>
      </div>
      <div className="res_score">
        <h3 style={{ "margin-left": "50px" }}>RES SCORE</h3>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="resScore"
              label=""
              type="number"
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
        <h1 style={{ "margin-left": "50px" }}>Countries Score</h1>
      </div>
      <div className="first_sc">
        <h2 style={{ "margin-left": "50px" }}>Italy</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="italy"
              label=""
              type="number"
              min="0"
              max="1"
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

        <h2>France</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="france"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="austria"
              label=""
              type="number"
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
        <h2>Germany</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="germany"
              label=""
              type="number"
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
      </div>
      <div className="second_sc">
        <h2 style={{ "margin-left": "50px" }}>Denmark</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="denmark"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="czech"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="finland"
              label=""
              type="number"
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
        <h2>Ireland</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="ireland"
              label=""
              type="number"
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
      </div>
      <div className="third_sc">
        <h2 style={{ "margin-left": "50px" }}>Israel</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="israel"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="portugal"
              label=""
              type="number"
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
        <h2>Ukranie</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="ukraine"
              label=""
              type="number"
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
        <h2>United Kingdom</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="uk"
              label=""
              type="number"
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
      <div className="fourth_sc">
        <h2 style={{ "margin-left": "50px" }}>Turkey</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="turkey"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="switzerland"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="spain"
              label=""
              type="number"
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
        <h2>Norway</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="norway"
              label=""
              type="number"
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
        <h1 style={{ "margin-left": "50px" }}>Types Scores</h1>
      </div>
      <div className="first_ty" style={{ "margin-top": "5px" }}>
        <h2 style={{ "margin-left": "50px" }}>Association/Agency</h2>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <TextField
              style={{ width: "40%" }}
              id="agency"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="uni"
              label=""
              type="number"
              value={state.uni}
              onChange={handleInputChange}
              error={formState.uni}
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
              style={{ width: "40%" }}
              id="company"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="RD"
              label=""
              type="number"
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
              style={{ width: "40%" }}
              id="start"
              label=""
              type="number"
              value={state.start}
              onChange={handleInputChange}
              error={formState.start}
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
              style={{ width: "40%" }}
              id="oth"
              label=""
              type="number"
              value={state.oth}
              onChange={handleInputChange}
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
        <Button
          color="primary"
          round
          variant="contained"
          id="ButtonText"
          onClick={() => updateAlert()}
        >
          Update
        </Button>
      </div>

      <div className="Buttons">
        <Button
          color="secondary"
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
            title={"B2match Alerts Results"}
            columns={events_columns}
            data={state.events}
          />
        )}
      </div>
      <div className="Buttons">
        {state && ((state.events && state.events.length !== 0) || (state.calls && state.calls.length !== 0)) ? (
          <Button
            color="secondary"
            round
            variant="contained"
            onClick={() => hideAlerts()}
          >
            Hide Alerts Results
        </Button>)
          : null}
      </div>
      {state && state.loading ? <Dialog
        disableBackdropClick
        disableEscapeKeyDown
        open={true}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description">
        <DialogTitle className={classes.title}>LOADING</DialogTitle>
        <DialogContent style={{ 'margin-left': '17px' }}>
          <BeatLoader />
        </DialogContent>
      </Dialog> : null}
    </React.Fragment>
  );
}
export default AlertsSettings;
