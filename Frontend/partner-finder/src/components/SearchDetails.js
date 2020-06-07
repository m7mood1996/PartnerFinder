import React from "react";
import TextField from "@material-ui/core/TextField";
import Select from "@material-ui/core/Select";
import Typography from "@material-ui/core/Typography";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import Grid from "@material-ui/core/Grid";
import { Button } from "@material-ui/core";
import countryList from "react-select-country-list";
import "react-phone-number-input/style.css";
import PhoneInput from "react-phone-number-input";
import { WithContext as ReactTags } from "react-tag-input";
import SearchResults from "./SearchResults";
import { BeatLoader } from 'react-spinners'
import { makeStyles, Dialog, DialogTitle, DialogContent } from '@material-ui/core/';
import { companyTypesOptions } from '../utils';

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
  const [type, setType] = React.useState("");
  const [country, setCountry] = React.useState([]);
  const [data, setData] = React.useState([]);
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [number, setNumber] = React.useState();
  const [phone_num, setPhone] = React.useState("");
  const [tags, setTags] = React.useState([]);
  const [countrySearched, setCountrySearched] = React.useState([]);
  const [state, setState] = React.useState({
    loading: false,
    firstLoading: true,
  });

  const [formState, setFormState] = React.useState({
    name: false,
    email: false,
    country: false,
    countrySearched: false,
    type: false,
    tags: false,
    number: false,
    phone_num: false,
  });

  if (state.firstLoading) {
    setName(props.state.name)
    setState({ ...state, firstLoading: false })
  }

  const changeName = (event) => {
    setName(event.target.value);
    props.setState({ ...props.state, 'name': event.target.value })
    if (event.target.value.length !== 0)
      setFormState({ ...formState, name: false });
  };
  const changeEmail = (event) => {
    setEmail(event.target.value);
    if (event.target.value.length !== 0 || event.target.value === "")
      setFormState({ ...formState, email: false });
  };
  const changePhone = (event) => {
    setPhone(event);
    if (event !== 0 || event !== "")
      setFormState({ ...formState, phone_num: false });
    console.log("phone" + phone_num);
  };
  const handleChange = (event) => {
    setType(event.target.value);
    if (event.target.value.length !== 0)
      setFormState({ ...formState, type: false });
  };

  const handleCountry = (event) => {
    setCountry(event.target.value);
    if (event.target.value.length !== 0)
      setFormState({ ...formState, country: false });
  };

  const handleCountrySearched = (event) => {
    setCountrySearched(event.target.value);
  };

  const handleInputChange = (event) => {
    setNumber(event.target.value);
    if (event.target.value <= 0) {
      setFormState({ ...formState, number: true });
    }
    else {
      setFormState({ ...formState, number: false });
    }

  };
  const addTag = (tag) => {
    setTags([...tags, tag]);
  };

  const changeTagInput = (event) => {
    if (event.length !== 0) {
      setFormState({ ...formState, tags: false });
    }
  };
  const deleteTag = (idx) => {
    let newTags = tags.filter((val, i) => i !== idx);
    setTags(newTags);
  };

  const dragTag = (tag, currPos, newPos) => { };

  const searchCompany = () => {
    if (formValidation()) {
      // TODO: show error message
    }
    else {
      searchByTagsAndCountires(tags, countrySearched);
    }
  };

  const validate = () => {
    let check = true;
    let emailError = "";
    if (!state.email.includes('@')) {
      emailError = 'invalid email !'
    }
    if (emailError) {
      setState(...setState, emailError);
      return check = false;
    }
    return check;
  }

  const searchByTagsAndCountires = (tags, countries) => {
    setState({ loading: true });
    tags = tags.map((tag) => tag.text);
    let url = new URL(
      "http://127.0.0.1:8000/api/genericSearch/searchByCountriesAndTags/"
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
        setState({ loading: false });
        setData(resp);
      })
      .catch((error) => {
        setData([])
        //TODO: show error message
        setState({ loading: false });
      });
  };

  const formValidation = () => {
    let res = {};
    let check = false;
    if (name === "" || name.length === 0) {
      res = { ...res, name: true };
      setFormState(res);
      check = true;
    } else {
      res = { ...res, name: false };
    }
    if (email === "" || email.length === 0) {
      res = { ...res, email: true };
      setFormState(res);
      check = true;
    } else {
      if (!email.match(/^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$/i)) {
        res = { ...res, email: true };
        setFormState(res);
        check = true;
      }
      else {
        res = { ...res, email: false };
      }
    }
    if (country.length === 0 || country === undefined || country === null) {
      res = { ...res, country: true };
      setFormState(res);
      check = true;
    } else {
      res = { ...res, country: false };
    }
    if (type.length === 0 || type === undefined || type === null) {
      res = { ...res, type: true };
      setFormState(res);
      check = true;
    } else {
      res = { ...res, type: false };
    }
    if (number === undefined || number === null) {
      res = { ...res, number: true };
      setFormState(res);
      check = true;
    } else {
      if (number <= 0) {
        res = { ...res, number: true };
        setFormState(res);
        check = true;
      }
      else {
        res = { ...res, number: false };
      }
    }
    if (phone_num.length === 0 || phone_num === undefined || phone_num === null) {
      res = { ...res, phone_num: true };
      setFormState(res);
      check = true;
    } else {
      res = { ...res, phone_num: false };
    }
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
      <div className="Org_Details">
        <h1>Simple Partner Search</h1>
        <h2>Organization Details</h2>
        <div className="first_row">
          <div className="SearchTab">
            <h1>Name</h1>
            <form className={SearchDetails.root} autoComplete="off">
              <TextField
                id="fields"
                style={{ 'margin-top': '19px' }}
                onChange={changeName}
                label="Name"
                variant="outlined"
                error={formState.name}
              />
            </form>
          </div>
          <div className="type">
            <h1>Type</h1>
            <FormControl className={SearchDetails.formControl} id="tab">
              <InputLabel id="company_type" error={formState.type}>
                Type
              </InputLabel>
              <Select
                labelId="company_type"
                id="company_type"
                value={type}
                onChange={handleChange}
              >
                {companyTypesOptions.map((val, idx) => {
                  return <MenuItem value={idx}>{val}</MenuItem>;
                })}
              </Select>
            </FormControl>
          </div>
          <div className="country">
            <h1>Country</h1>
            <FormControl className={SearchDetails.formControl} id="tab">
              <InputLabel style={{ 'margin-top': '12px' }} id="company_type" error={formState.country}>
                Country
              </InputLabel>
              <Select
                style={{ 'margin-top': '26.8px' }}
                options={countryList().getData()}
                value={country}
                onChange={handleCountry}
              >
                {countryList()
                  .getData()
                  .map((val) => {
                    return <MenuItem value={val.label}>{val.label}</MenuItem>;
                  })}
              </Select>
            </FormControl>
          </div>
          <div className="Email">
            <h1>E-mail</h1>
            <TextField
              id="fields"
              label="E-mail"
              style={{ 'margin-top': '19px' }}
              onChange={changeEmail}
              className={SearchDetails.textField}
              type="email"
              name="email"
              autoComplete="email"
              margin="normal"
              variant="outlined"
              error={formState.email}
            />
          </div>
        </div>
        <div className="second_row">
          <div className="Projects">
            <h1>Number Of Projects</h1>
            <Grid container spacing={2} alignItems="center">
              <Grid item>
                <TextField
                  style={{ width: "40%" }}
                  id="fields"
                  label=""
                  type="number"
                  error={formState.number}
                  onChange={handleInputChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                  variant="outlined"
                />
              </Grid>
            </Grid>
          </div>
          <div className="Phone_Number">
            <h1>Phone</h1>
            <PhoneInput
              placeholder="Enter phone number"
              value={phone_num}
              onChange={changePhone}
              error={formState.phone_num}
            />
          </div>
        </div>
      </div>
      <hr
        style={{
          "margin-top": "3%",
          border: "2px solid gray",
          "border-radius": "5px",
          marginLeft: "2%",
          marginRight: "4%",
        }}
      />
      <div className="Search_Details">
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
