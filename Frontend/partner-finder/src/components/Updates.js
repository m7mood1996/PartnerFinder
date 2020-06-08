import React from "react";
import { Button } from "@material-ui/core";
import { Msgtoshow } from "./Msgtoshow"
import { BACKEND_URL } from '../utils';

function Updates(props) {
  const [state, setState] = React.useState({
    EU: '',
    B2MATCH: '',
    firstLoading: true,
  });

  const [msgState, setMsgState] = React.useState({ title: '', body: '', visible: false });

  if (state.firstLoading) {
    setState({ ...props.state });
  }

  const updateB2match = (event) => {
    let url = new URL(
      BACKEND_URL + "events/update_upcoming_events/"
    );
    fetch(url, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((resp) => {
        setMsgState({
          title: 'Success',
          body: 'B2match has been updated successfully',
          visible: true
        });
      })
      .catch((error) => setMsgState({
        title: 'Error',
        body: 'Error while updating B2match data',
        visible: true
      }));
  };

  const updateEU = (event) => {
    let url = new URL(
      BACKEND_URL + "organizations/updateOrganizations/"
    );
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        setMsgState({
          title: 'Success',
          body: 'EU has been updated successfully.',
          visible: true
        });
      })
      .catch((error) => setMsgState({
        title: 'Error',
        body: 'Error while updating EU data',
        visible: true
      }));
  };

  return (
    <React.Fragment>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }}>
        <Msgtoshow {...msgState} handleClose={() => setMsgState({ ...msgState, visible: false })} />
      </div>
      <div>
        <h1>Updates</h1>
      </div>
      <div style={{ "margin-top": "50px" }}>
        <h1 style={{ "margin-left": "50px" }}>B2MATCH</h1>
      </div>
      <div className="update">
        <h2 style={{ "margin-left": "50px" }}>Last Update</h2>
        <h3>{state.B2MATCH}</h3>
      </div>
      <div style={{ "margin-left": "50px", "margin-top": "50px" }}>
        <Button
          color="primary"
          round
          variant="contained"
          id="ButtonText"
          onClick={updateB2match}
          style={{ width: "20%" }}
        >
          Update Now
        </Button>
      </div>
      <div style={{ "margin-top": "50px" }}>
        <h1 style={{ "margin-left": "50px" }}>EU</h1>
      </div>
      <div className="update">
        <h2 style={{ "margin-left": "50px" }}>Last Update</h2>
        <h3>{state.EU}</h3>
      </div>
      <div style={{ "margin-left": "50px", "margin-top": "50px" }}>
        <Button
          color="primary"
          round
          variant="contained"
          id="ButtonText"
          onClick={updateEU}
          style={{ width: "20%" }}
        >
          Update Now
        </Button>
      </div>
      <div style={{ "margin-top": "10%" }}>
        <h1
          style={{
            "margin-left": "45px",
            color: "blue",
            "font-weight": "bold",
          }}
        >
          ** There is an automatically updates every month for both EU & B2MATCH **
        </h1>
      </div>
    </React.Fragment>
  );
}
export default Updates;
