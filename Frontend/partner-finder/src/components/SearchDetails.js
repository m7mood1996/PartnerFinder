import React from "react";
import Select from "@material-ui/core/Select";
import Typography from "@material-ui/core/Typography";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import { Button, Checkbox } from "@material-ui/core";
import countryList from "react-select-country-list";
import "react-phone-number-input/style.css";
import { WithContext as ReactTags } from "react-tag-input";
import SearchResults from "./SearchResults";
import { BeatLoader } from "react-spinners";
import { Msgtoshow } from "./Msgtoshow";
import {
  makeStyles,
  Dialog,
  DialogTitle,
  DialogContent,
} from "@material-ui/core/";
import { classificationTypesOptions, consorsiumRoles, BACKEND_URL } from "../utils";

const KeyCodes = {
  comma: 188,
  enter: 13,
};
const delimiters = [KeyCodes.comma, KeyCodes.enter];

const useStyles = makeStyles((theme) => ({
  title: {
    textAlign: "center",
    fontSize: 30,
  },
}));

function SearchDetails(props) {
  const classes = useStyles();
  const [msgState, setMsgState] = React.useState({
    title: "",
    body: "",
    visible: false,
  });
  const [data, setData] = React.useState({});
  const [tags, setTags] = React.useState([]);
  const [type, setType] = React.useState([]);
  const [role, setRole] = React.useState('');
  const [countrySearched, setCountrySearched] = React.useState([]);
  
  const [state, setState] = React.useState({
    loading: false,
    firstLoading: true,
   
  });
  const [checked, setChecked] = React.useState([]);
  
  const [formState, setFormState] = React.useState({
    tags: false,
  });
  
  
  /**
   * handler function for the checkbox to set the values of the countries and the 
   * classification types that the user chose
   * @param {event} event event when the user want to choose value from the checkbox
   */
  const handleCheckbox = (event) => {

    const currentIndex = checked.indexOf(event.target.name);
    const countryIndex = countrySearched.indexOf(event.target.name);
    const typeIndex = type.indexOf(event.target.name);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(event.target.name);
      if(event.target.id === "country"){
        countrySearched.push(event.target.name);
        setCountrySearched([...countrySearched]);
        props.setState({ ...props.state, countrySearched: event.target.name });
      }else{
        type.push(event.target.name);
        setType([...type]);
        props.setState({ ...props.state, type: event.target.name });
      }
    } else {
      if(event.target.id === "country"){
        countrySearched.splice(countryIndex, 1);
      }
      else{ 
        type.splice(typeIndex, 1);
      }
      newChecked.splice(currentIndex, 1);
    }
    setChecked(newChecked);
  };

  if (state.firstLoading) {
    setTags([...props.state.tags]);
    setType([...props.state.type]);
    setRole(...props.state.role);
    setCountrySearched([...props.state.countrySearched]);
    setData({ ...props.state.data });
    setState({ ...state, firstLoading: false });
  }

  /**
   * handler function to set the role that the user chose
   * @param {event} event event when the user choose a role
   */
  const handleRole = (event) => {
    setRole(event.target.value);
    props.setState({ ...props.state, role: event.target.value });
  };

  /**
   * function for adding a new tag
   * @param {String} tag the tag that the user inserts
   */
  const addTag = (tag) => {
    setTags([...tags, tag]);
    props.setState({ ...props.state, tags: [...props.state.tags, tag] });
  };

  
  /**
   * function that sets the value of the tag that the user filled
   * @param {event} event 
   */
  const changeTagInput = (event) => {
    if (event.length !== 0) {
      setFormState({ ...formState, tags: false });
    }
  };
  /**
   * function for deleting the tag that has been inserted
   * @param {int} idx index of the tag we want to delete
   */
  const deleteTag = (idx) => {
    let newTags = tags.filter((val, i) => i !== idx);
    setTags(newTags);
    props.setState({ ...props.state, tags: [...newTags] });
  };

  const dragTag = (tag, currPos, newPos) => {};

  /**
   * Method that checkes the validation 
   */
  const searchCompany = () => {
    if (formValidation()) {
      setMsgState({
        title: "Error",
        body: "Please fill the tag field",
        visible: true,
      });
    } else {
      searchByTagsAndCountires(tags, countrySearched, type, role);
    }
  };

  /**
   *[description] Method that searchs for the organizations from EU and for the participants 
    from B2MATCH in our DB by tags and countries 
   * @param {array} tags array of tags that the user entered
   * @param {array} countries array of the countries that the user chose
   * @param {array} type array of the classification types that the user chose
   * @param {String} role the role that the user chose
   * @returns {JSON} JSON file of the results 
   */
  const searchByTagsAndCountires = (tags, countries, type, role) => {
    
    setState({ ...state, loading: true });
    tags = tags.map((tag) => tag.text);
    let url = new URL(BACKEND_URL + "genericSearch/searchByCountriesAndTags/");
    let params = { data: JSON.stringify({ tags: tags, countries: countries, type: type, role: role }) };
    Object.keys(params).forEach((key) =>
      url.searchParams.append(key, params[key])
    );
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        if ("error" in resp) {
          console.log("ERROR", resp);
          setMsgState({
            title: "Failed",
            body: "Error while searching for organizations",
            visible: true,
          });
          setState({ ...state, loading: false });
          setData({ EU: [], B2MATCH: [] });
          props.setState({ ...props.state, data: { EU: [], B2MATCH: [] } });
        } else {
          console.log(resp);
          setState({ ...state, loading: false });
          setData(resp);
          props.setState({ ...props.state, data: { ...resp } });
        }
      })
      .catch((error) => {
        console.log("ERROR", error);
        setData({ EU: [], B2MATCH: [] });
        props.setState({ ...props.state, data: { EU: [], B2MATCH: [] } });
        setMsgState({
          title: "Failed",
          body: "Error while searching for organizations",
          visible: true,
        });
        setState({ ...state, loading: false });
      });
  };
  /**
   * Method that checks if the tag input has been filled or not
   */
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
    <React.Fragment>
      <Msgtoshow
        {...msgState}
        handleClose={() => setMsgState({ ...msgState, visible: false })}
      />
      <h1 id="textFontFamily" style={{ color: "#02203c" }}>
        Simple Partner Search
      </h1>

      <div className="Search_Details">
        <h1
          style={{ "margin-left": "1%" }}
        >
          Search Details
        </h1>
        <div className="input_row">
          <div className="Tags">
            <h1>
              Tags and Keywords
            </h1>
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
                style={{ color: "red", fontWeight: "bold" }}
              >
                Enter at least one tag
              </Typography>
            ) : null}
          </div>
          <div className="SCountry">
            <h1 id="textFontFamily" style={{ color: "#02203c" }}>
              Country\ies
            </h1>
            <FormControl className={SearchDetails.formControl} id="tab">
              <InputLabel
                id="textFontFamily"
                style={{ 'color': "#02203c" }}
              >
                Country\ies
              </InputLabel>
              <Select
                id="textFontFamily"
                style={{ 'color': "#02203c" }}
                options={countryList().getData()}
                value={countrySearched}
                
                autoWidth='true'
              >
                {countryList()
                  .getData()
                  .map((val) => {
                    return <MenuItem id="country" style= {{ 'backgroundColor':'#ececec'}} value={val.label}><Checkbox id="country" name={val.label} checked={checked.indexOf(val.label) !== -1} onChange={handleCheckbox}/>{val.label}</MenuItem>;
                  })}
                  
              </Select>
            </FormControl>
          </div>
          <div>
            <h1>Classification Type\s</h1>       
            <FormControl className={SearchDetails.formControl} id="tab">
                <InputLabel 
                id="textFontFamily"
                style={{ 'color': "#02203c" }}
                >Type\s</InputLabel>
                  <Select
                      value={MenuItem.value}
                  >
                  {classificationTypesOptions.map((val) => {
                      return <MenuItem style= {{ 'backgroundColor':'#ececec'}} value={val}><Checkbox id={val} name={val} checked={checked.indexOf(val) !== -1} onChange={handleCheckbox}/>{val}</MenuItem>
                  })}
                  </Select>
            </FormControl>
          </div>
          <div>
          <h1>Consortium Role</h1>       
            <FormControl className={SearchDetails.formControl} id="tab">
                <InputLabel 
                id="textFontFamily"
                style={{ 'color': "#02203c" }}
                >Role</InputLabel>
                  <Select
                      value={role}
                      onChange={handleRole}
                  >
                  {consorsiumRoles.map((val) => {
                      return <MenuItem style= {{ 'backgroundColor':'#ececec'}} onChange={handleRole}value={val} >{val}</MenuItem>;
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
          id="BackgroundColor"
          onClick={() => searchCompany()}
          disabled={state.loading}
        >
          {state && state.loading && <i className="fa fa-refresh fa-spin"></i>}
          {state && state.loading && (
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
          )}
          {state && !state.loading && <span>Search</span>}
        </Button>
      </div>
      {data &&
      data.EU &&
      data.B2MATCH &&
      data.EU.length === 0 &&
      data.B2MATCH.length === 0 ? null : (
        <div style={{ "margin-top": "10px" }}>
          <SearchResults data={data} />
        </div>
      )}
    </React.Fragment>
  );
}
export default SearchDetails;
