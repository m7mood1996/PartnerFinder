import React from "react";
import Select from "react-select";
import MultiSelect from "react-multi-select-component";
import Typography from "@material-ui/core/Typography";
import FormControl from "@material-ui/core/FormControl";
import { Button } from "@material-ui/core";
import countryList from "react-select-country-list";
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

const customStyles = {
  menu: (provided, state) => ({
    ...provided,
    backgroundColor: "#02203c",
    borderBottom: '1px dotted pink',
    color: "white",
    fontSize: "13px",
  }),

  placeholder: styles => ({ ...styles, color: "white", fontSize: "13px", }),
  control: styles => ({ ...styles, backgroundColor: '#02203c', color: "white", fontSize: "13px", }),

  option: styles => ({
    ...styles, color: "white", backgroundColor: "#02203c", fontSize: "13px", '&:hover': {
      backgroundColor: "#f1f3f5",
      color: "black",
      fontSize: "13px",
    },
  }),
  singleValue: styles => ({ ...styles, color: "white", fontSize: "13px" })



}

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

  const [formState, setFormState] = React.useState({
    tags: false,
  });

  if (state.firstLoading) {
    setTags([...props.state.tags]);
    setType([...props.state.type]);
    setRole(props.state.role);
    setCountrySearched([...props.state.countrySearched]);
    setData({ ...props.state.data });
    setState({ ...state, firstLoading: false });
  }

  const handleCountry = (event) => {
    console.log(event);
    setCountrySearched(event);
    props.setState({ ...props.state, countrySearched: event });
    console.log(countrySearched);
  };

  const handleSelect = (event) => {
    if (event instanceof Array === false) {
      let newRole = '';
      if (event === role) {
        newRole = '';
      }
      else {
        newRole = event;
      }
      setRole(newRole);
      props.setState({ ...props.state, role: newRole });
    }
    else {
        setType(event);
        props.setState({ ...props.state, type: event });
    }
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

  const dragTag = (tag, currPos, newPos) => { };

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
      let countriesToSearch = countrySearched.map((value) => {
        return value.label;
      })
      let typeTosSearch = type.map((value) => {
        return value.label;
      })
      let roleToSearch = '';
      if (role !== '') {
        roleToSearch = role.label;
      }
      genericSearch(tags, countriesToSearch, typeTosSearch, roleToSearch);
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
  const genericSearch = (tags, countries, type, role) => {
    setState({ ...state, loading: true });
    tags = tags.map((tag) => tag.text);
    let url = new URL(BACKEND_URL + "generic_search/");
    let params = { data: JSON.stringify({ tags: tags, countries: countries, types: type, role: role }) };
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
          setState({ ...state, loading: false });
          resp['EU'] = resp['EU'].map(val => {
            return { ...val, 'consorsiumRoles': val.consorsiumRoles ? 'Coordinator' : 'Regular' }
          })
          setData(resp);
          props.setState({ ...props.state, data: { ...resp } });
          if(resp.EU.length === 0 && resp.B2MATCH.length === 0){
            setMsgState({
              title: "Success",
              body: "We didn't find any relevant results",
              visible: true,
            });
          }
          else{
            if (resp.EU.length === 0){
              setMsgState({
                title: "Success",
                body: "We didn't find any relevant organizations from EU",
                visible: true,
              });
            }
            if (resp.B2MATCH.length === 0){
              setMsgState({
                title: "Success",
                body: "We didn't find any relevant participants from B2match",
                visible: true,
              });
            }
          }
         
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
            <FormControl className={SearchDetails.formControl} id="text_select">
              <MultiSelect
                options={countryList().getData()}
                value={countrySearched}
                onChange={handleCountry}
                focusSearchOnOpen={true}
                className="select"
                labelledBy={"Select"}
              />
            </FormControl>
          </div>
          <div>
            <h1>Classification Type\s</h1>
            <FormControl className={SearchDetails.formControl} id="text_select">
              <MultiSelect
                styles={customStyles}
                options={classificationTypesOptions}
                className="select"
                value={type}
                onChange={handleSelect}
                labelledBy={"Select"}
              />
            </FormControl>
          </div>
          <div>
            <h1>Consortium Role</h1>
            <FormControl className={SearchDetails.formControl} id="tab">
              <Select
                value={role}
                styles={customStyles}
                onChange={handleSelect}
                className="select_role"
                options={consorsiumRoles}
                id="textFontFamily"
                variant="outlined"
              />
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
