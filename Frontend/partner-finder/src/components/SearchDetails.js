import React from "react";
import Select from "@material-ui/core/Select";
import Typography from "@material-ui/core/Typography";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import { Button } from "@material-ui/core";
import countryList from "react-select-country-list";
import "react-phone-number-input/style.css";
import { WithContext as ReactTags } from "react-tag-input";
import SearchResults from "./SearchResults";
import { BeatLoader } from 'react-spinners';
import { Msgtoshow } from "./Msgtoshow";
import { makeStyles, Dialog, DialogTitle, DialogContent } from '@material-ui/core/';
import { companyTypesOptions, BACKEND_URL } from '../utils';

const KeyCodes = {
  comma: 188,
  enter: 13,
};
const delimiters = [KeyCodes.comma, KeyCodes.enter];

const useStyles = makeStyles(theme => ({
  title: {
    textAlign: 'center',
    fontSize: 30,
  },


}));

function SearchDetails(props) {

  const classes = useStyles();
  const [msgState, setMsgState] = React.useState({ title: '', body: '', visible: false });
  const [data, setData] = React.useState({});
  const [tags, setTags] = React.useState([]);
  const [countrySearched, setCountrySearched] = React.useState([]);
  const [state, setState] = React.useState({
    loading: false,
    firstLoading: true,
  });

  const [formState, setFormState] = React.useState({
    tags: false,
  });

  if (state.firstLoading) {
    console.log('PROPS', props.state)
    setTags([...props.state.tags])
    setCountrySearched([...props.state.countrySearched])
    setData({ ...props.state.data })
    setState({ ...state, firstLoading: false })
  }



  const handleCountrySearched = (event) => {
    setCountrySearched(event.target.value);
    props.setState({ ...props.state, 'countrySearched': event.target.value });
  };

  const addTag = (tag) => {
    setTags([...tags, tag]);
    props.setState({ ...props.state, 'tags': [...props.state.tags, tag] })
  };

  const changeTagInput = (event) => {
    if (event.length !== 0) {
      setFormState({ ...formState, tags: false });
    }
  };
  const deleteTag = (idx) => {
    let newTags = tags.filter((val, i) => i !== idx);
    setTags(newTags);
    props.setState({ ...props.state, 'tags': [...newTags] })
  };

  const dragTag = (tag, currPos, newPos) => { };

  const searchCompany = () => {
    if (formValidation()) {
      setMsgState({
        title: 'Error',
        body: 'Please fill the tag field',
        visible: true
      });
    }
    else {
      searchByTagsAndCountires(tags, countrySearched);
    }
  };

  const searchByTagsAndCountires = (tags, countries) => {
    setState({ ...state, loading: true });
    tags = tags.map((tag) => tag.text);
    let url = new URL(
      BACKEND_URL + "genericSearch/searchByCountriesAndTags/"
    );
    let params = { data: JSON.stringify({ tags: tags, countries: countries }) };
    Object.keys(params).forEach((key) =>
      url.searchParams.append(key, params[key])
    );
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ('error' in resp) {
          console.log("ERROR", resp)
          setMsgState({
            title: 'Failed',
            body: 'Error while searching for organizations',
            visible: true
          });
          setState({ ...state, loading: false });
          setData({});
          props.setState({ ...props.state, 'data': {} })
        }
        else {
          console.log(resp)
          setState({ ...state, loading: false });
          setData(resp);
          props.setState({ ...props.state, 'data': { ...resp } })
        }
      })
      .catch((error) => {
        console.log("ERROR", error)
        setData({})
        props.setState({ ...props.state, 'data': {} })
        setMsgState({
          title: 'Failed',
          body: 'Error while searching for organizations',
          visible: true
        });
        setState({ ...state, loading: false });
      });
  };

  const formValidation = () => {
    let res = {};
    let check = false;

    if (tags.length === 0 || tags === undefined || tags === null) {
      res = { ...res, tags: true };
      setFormState(res);
      check = true;
    } else {
      res = { ...res, tags: false };
    }
    setFormState(res);
    return check;
  };

  return (
    <React.Fragment style={{ 'backgroundColor': '#7395AE' }}>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: 100 }}>
        <Msgtoshow {...msgState} handleClose={() => setMsgState({ ...msgState, visible: false })} />
      </div>
        <h1 >Simple Partner Search</h1>

        <div className="Search_Details" >
          <h1 style={{ "margin-left": "1%" }}>Search Details</h1>
          <div className="third_row">
            <div className="Tags">
              <h1>Tags and Keywords</h1>
              <ReactTags
                tags={tags}
                handleDelete={deleteTag}
                handleAddition={addTag}
                handleDrag={dragTag}
                delimiters={delimiters}
                handleInputChange={changeTagInput}
              />

              {formState && formState.tags ? (
                <Typography
                  variant="caption"
                  display="block"
                  gutterBottom
                  style={{ color: "red" }}
                >
                  Enter at least one tag
              </Typography>
              ) : null}
            </div>
            <div className="SCountry">
              <h1>Country</h1>
              <FormControl className={SearchDetails.formControl} id="tab">
                <InputLabel
                  id="demo-mutiple-name-label"
                >
                  Country
              </InputLabel>
                <Select
                  options={countryList().getData()}
                  value={countrySearched}
                  onChange={handleCountrySearched}
                  labelId="demo-mutiple-name-label"
                  id="demo-mutiple-name"
                  multiple
                >
                  {countryList()
                    .getData()
                    .map((val) => {
                      return <MenuItem value={val.label}>{val.label}</MenuItem>;
                    })}
                </Select>
              </FormControl>
            </div>
          </div>
        </div>





        <div className="Buttons">
          <Button
            color="primary"
            round
            variant="contained"
            id="ButtonText"
            onClick={() => searchCompany()}
            disabled={state.loading}
          >
            {state && state.loading && <i className="fa fa-refresh fa-spin"></i>}
            {state && state.loading && <Dialog
              disableBackdropClick
              disableEscapeKeyDown
              open={true}
              aria-labelledby="alert-dialog-title"
              aria-describedby="alert-dialog-description">
              <DialogTitle className={classes.title}>LOADING</DialogTitle>
              <DialogContent style={{ 'margin-left': '17px' }}>
                <BeatLoader />
              </DialogContent>
            </Dialog>}
            {state && !state.loading && <span>Search</span>}
          </Button>
        </div>
        {data && data.length === 0 ? null : (
          <div style={{ "margin-top": "10px" }}>
            <SearchResults data={data} />
          </div>
        )}
    </React.Fragment>
  );
}
export default SearchDetails;
