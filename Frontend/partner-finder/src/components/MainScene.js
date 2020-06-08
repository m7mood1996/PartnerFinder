import React from "react";
import SearchDetails from "./SearchDetails";
import AlertsSettings from "./AlertsSettings";
import Updates from "./Updates";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import moment from "moment";
import { Msgtoshow } from './Msgtoshow';
import { BACKEND_URL } from '../utils';

function MainScene(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`nav-tabpanel-${index}`}
      aria-labelledby={`nav-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

MainScene.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `nav-tab-${index}`,
    "aria-controls": `nav-tabpanel-${index}`,
  };
}

function LinkTab(props) {
  return (
    <Tab
      component="a"
      onClick={(event) => {
        event.preventDefault();
      }}
      {...props}
    />
  );
}

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

export default function NavTabs() {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);
  const [msgState, setMsgState] = React.useState({ title: '', body: '', visible: false });
  const [alertsState, setAlertsState] = React.useState({
    firstLoading: true,
    loading: false,
    turned_on: false,
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
  });

  const [searchState, setSearchState] = React.useState({
    type: '',
    country: '',
    data: [],
    name: '',
    email: '',
    number: '',
    phone_num: '',
    tags: [],
    countrySearched: [],
    firstLoading: false,
    loading: false,
  })

  const [updatesState, setUpdatesState] = React.useState({
    EU: '',
    B2MATCH: '',
    firstLoading: true,
  });


  if (updatesState.firstLoading) {
    let url = new URL(BACKEND_URL + "updates/getSettings/");
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ('error' in resp) {
          setMsgState({
            title: 'Failed',
            body: 'Error while getting updates settings',
            visible: true
          })
          setUpdatesState({
            EU: '',
            B2MATCH: '',
            firstLoading: false,
          })
        }
        else {
          setUpdatesState({
            EU: moment.unix(resp.EU).format("MMMM Do YYYY, h:mm:ss a"),
            B2MATCH: moment.unix(resp.B2MATCH).format("MMMM Do YYYY, h:mm:ss a"),
            firstLoading: false,
          });
        }
      })
      .catch((error) => {
        setMsgState({
          title: 'Failed',
          body: 'Error while getting updates settings',
          visible: true
        })
        setUpdatesState({
          EU: '',
          B2MATCH: '',
          firstLoading: false,
        })
      });
  }

  if (alertsState.firstLoading) {
    let newState = { ...alertsState, firstLoading: false };
    let newMail = "";
    let turned_on = false;
    let url = new URL(BACKEND_URL + "alerts/getSettings/");
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ('error' in resp) {
          setMsgState({
            title: 'Failed',
            body: 'Error while uploading alerts settings',
            visible: true
          })
          setAlertsState(newState);
        }
        else {
          turned_on = resp.turned_on;
          newMail = resp.email;
          url = new URL(BACKEND_URL + "scores/getscores/");
          fetch(url, {
            method: "GET",
          })
            .then((res) => res.json())
            .then((resp) => {
              if ('error' in resp) {
                setMsgState({
                  title: 'Failed',
                  body: 'Error while uploading alerts settings',
                  visible: true
                })
                setAlertsState(newState);
              }
              else {
                newState["resScore"] = resp.RES;
                newState["italy"] = resp.Italy;
                newState["france"] = resp.France;
                newState["austria"] = resp.Austria;
                newState["germany"] = resp.Germany;
                newState["denmark"] = resp.Denmark;
                newState["czech"] = resp.Czech_Republic;
                newState["finland"] = resp.Finland;
                newState["ireland"] = resp.Ireland;
                newState["israel"] = resp.Israel;
                newState["portugal"] = resp.Portugal;
                newState["ukranie"] = resp.Ukranie;
                newState["uk"] = resp.United_Kingdom;
                newState["turkey"] = resp.Turkey;
                newState["switzerland"] = resp.Switzerland;
                newState["spain"] = resp.Spain;
                newState["norway"] = resp.Norway;
                newState["agency"] = resp.Association_Agency;
                newState["uni"] = resp.University;
                newState["company"] = resp.Company;
                newState["RD"] = resp.R_D_Institution;
                newState["start"] = resp.Start_Up;
                newState["oth"] = resp.Others;
                newState["email"] = newMail;
                newState["turned_on"] = turned_on;
                setAlertsState(newState);
              }
            })
            .catch((error) => {
              setMsgState({
                title: 'Failed',
                body: 'Error while uploading alerts settings',
                visible: true
              })
              setAlertsState(newState);
            });
        }
      })
      .catch((error) => {
        setMsgState({
          title: 'Failed',
          body: 'Error while uploading alerts settings',
          visible: true
        })
        setAlertsState(newState);
      });
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs
          variant="fullWidth"
          value={value}
          onChange={handleChange}
          aria-label="nav tabs example"
        >
          <LinkTab label="Basic Search" href="/search" {...a11yProps(0)} />
          <LinkTab label="Alerts Settings" href="/settings" {...a11yProps(1)} />
          <LinkTab label="Updates" href="/updates" {...a11yProps(2)} />
        </Tabs>
      </AppBar>
      <MainScene value={value} index={0}>
        <SearchDetails state={searchState} setState={setSearchState} />
      </MainScene>
      <MainScene value={value} index={1}>
        <AlertsSettings state={alertsState} setState={setAlertsState} />
      </MainScene>
      <MainScene value={value} index={2}>
        <Updates state={updatesState} setState={setUpdatesState} />
      </MainScene>
    </div>
  );
}
