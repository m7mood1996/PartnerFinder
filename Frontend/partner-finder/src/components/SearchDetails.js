import React from 'react'
import TextField from '@material-ui/core/TextField';
import { makeStyles } from "@material-ui/core/styles";
import Select from '@material-ui/core/Select';
import Typography from '@material-ui/core/Typography'
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Switch from '@material-ui/core/Switch';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from "@material-ui/core/Grid";
import Input from "@material-ui/core/Input";
import { Button } from '@material-ui/core';
import countryList from 'react-select-country-list'
import 'react-phone-number-input/style.css'
import PhoneInput from 'react-phone-number-input'
import { formatPhoneNumber } from 'react-phone-number-input'
import { WithContext as ReactTags } from 'react-tag-input';
import SearchResults from './SearchResults';

const KeyCodes = {
    comma: 188,
    enter: 13,
};
const delimiters = [KeyCodes.comma, KeyCodes.enter];

function SearchDetails() {
    const [type, setType] = React.useState('');
    const [country, setCountry] = React.useState([]);
    const [data, setData] = React.useState([]);
    const [name, setName] = React.useState('');
    const [email, setEmail] = React.useState('')
    const [number, setNumber] = React.useState('');
    const [phone_num, setPhone] = React.useState('');
    const [tags, setTags] = React.useState([]);
    const [countrySearched, setCountrySearched] = React.useState([]);

    const [formState, setFormState] = React.useState({
        name: false,
        email: false,
        country: false,
        countrySearched: false,
        type: false,
        tags: false,
        number: false,
        phone_num: false,
    })
    const companyTypesOptions = [
        "SME", "International Organization", "Higher or Secondary Education",
        "Research Organization", "Private for Profit Organization", "Public Organization", "Other"
    ]



    const changeName = event => {
        setName(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({ ...formState, name: false })
    }
    const changeEmail = event => {
        setEmail(event.target.value);
        if (event.target.value.length !== 0 || event.target.value === "")
            setFormState({ ...formState, email: false })
    }
    const changePhone = event => {
        console.log("Halaa " + event)
        setPhone(event);
        if (event.target.value.length !== 0 || event.target.value === "")
            setFormState({ ...formState, phone_num: false })
    }
    const handleChange = event => {
        setType(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({ ...formState, type: false })

    };

    const handleCountry = event => {
        setCountry(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({ ...formState, country: false })

    };

    const handleCountrySearched = event => {
        setCountrySearched(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({ ...formState, countrySearched: false })
    };

    const handleInputChange = event => {
        setNumber(event.target.value === "" ? "" : Number(event.target.value));
        if (event.target.value.length !== 0)
            setFormState({ ...formState, number: false })
    }
    const handleBlur = () => {
        if (number < 1) {
            setNumber(1);
        } else if (number > 100) {
            setNumber(100);
        }
    };
    const addTag = (tag) => {
        setTags([...tags, tag])

    }

    const changeTagInput = (event) => {
        if (event.length !== 0) {
            setFormState({ ...formState, tags: false })
        }
    }
    const deleteTag = (idx) => {
        let newTags = tags.filter((val, i) => i !== idx)
        setTags(newTags)
    }

    const dragTag = (tag, currPos, newPos) => {
    }

    const searchCompany = () => {
        // if (formValidation()) {
        //     setData([])
        // }
        // else {
        searchByTagsAndCountires(tags, countrySearched)
        // }
        // setData([{ name: 'stam', type: 'stam', country: 'stam', phone: 'stam', email: 'stam', num: 'stam', description: 'stam' }])
    }

    const searchByTagsAndCountires = (tags, countries) => {
        tags = tags.map(tag => tag.text)
        let url = new URL('http://127.0.0.1:8000/api/genericSearch/searchByCountriesAndTags/')
        let params = { 'data': JSON.stringify({ tags: tags, countries: countries }) }
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        fetch(url, {
            method: 'GET'
        }).then(res => res.json())
            .then(resp => {
                setData(resp)
                console.log("DATA2", resp)
            })
            .catch(error => console.log(error))
    }

    const formValidation = () => {
        let res = {}
        let check = false
        if (name === '' || name.length === 0) {
            res = { ...res, name: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, name: false }
        }
        if (email === '' || email.length === 0) {
            res = { ...res, email: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, email: false }
        }
        if (country.length === 0 || country === undefined || country === null) {
            res = { ...res, country: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, country: false }
        }
        if (countrySearched.length === 0 || countrySearched === undefined || countrySearched === null) {
            res = { ...res, countrySearched: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, countrySearched: false }
        }
        if (type.length === 0 || type === undefined || type === null) {
            res = { ...res, type: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, type: false }
        }
        if (number.length === 0 || number === undefined || number === null) {
            res = { ...res, number: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, number: false }
        }
        if (phone_num.length === 0 || phone_num === undefined || phone_num === null) {
            res = { ...res, phone_num: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, phone_num: false }
        }
        if (tags.length === 0 || tags === undefined || tags === null) {
            res = { ...res, tags: true }
            setFormState(res)
            check = true
        }
        else {
            res = { ...res, tags: false }
        }

        setFormState(res)
        return check
    }


    return (
        <React.Fragment>
            <div className="Org_Details">
                <h1>Simple Partner Search</h1>
                <h2>Organization Details</h2>
                <div className="first_row">
                    <div className="SearchTab">
                        <h1>Name</h1>
                        <form className={SearchDetails.root} autoComplete="off">
                            <TextField id="fields" onChange={changeName} label="Name" variant="outlined" error={formState.name} />
                        </form>
                    </div>
                    <div className="type">
                        <h1>Type</h1>
                        <FormControl className={SearchDetails.formControl} id="tab">
                            <InputLabel id="company_type" error={formState.type}>Type</InputLabel>
                            <Select
                                labelId="company_type"
                                id="company_type"
                                value={type}
                                onChange={handleChange}
                            >
                                {companyTypesOptions.map((val, idx) => {
                                    return <MenuItem value={idx}>{val}</MenuItem>
                                })}
                            </Select>
                        </FormControl>
                    </div>
                    <div className="country">
                        <h1>Country</h1>
                        <FormControl className={SearchDetails.formControl} id="tab" >
                            <InputLabel id="company_type" error={formState.country} >Country</InputLabel>
                            <Select
                                options={countryList().getData()}
                                value={country}
                                onChange={handleCountry}
                            >
                                {countryList().getData().map(val => {
                                    return <MenuItem value={val.label}>{val.label}</MenuItem>
                                })}
                            </Select>
                        </FormControl>
                    </div>
                    <div className="Email">
                        <h1>E-mail</h1>
                        <TextField
                            id="fields"
                            label="E-mail"
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
                        <Grid container spacing={2} alignItems="center"  >
                            <Grid item>
                                <TextField
                                    id="fields"
                                    label=""
                                    type="number"
                                    error={formState.number}
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
            <hr style={{ 'margin-top': '3%', 'border': '2px solid gray', 'border-radius': '5px', 'marginLeft': '2%', 'marginRight': '4%' }} />
            <div className="Search_Details">
                <h1 style={{ 'margin-left': '1%' }}>Search Details</h1>
                <div className="third_row">
                    <div className="Tags">
                        <h1>Tags and Keywords</h1>
                        <ReactTags tags={tags}
                            handleDelete={deleteTag}
                            handleAddition={addTag}
                            handleDrag={dragTag}
                            delimiters={delimiters}
                            handleInputChange={changeTagInput}
                        />

                        {formState.tags ? <Typography variant="caption" display="block" gutterBottom style={{ 'color': 'red' }}>
                            Enter at least one tag
                                    </Typography> : null}
                    </div>
                    <div className="SCountry">
                        <h1>Country</h1>
                        <FormControl className={SearchDetails.formControl} id="tab" >
                            <InputLabel id="demo-mutiple-name-label" error={formState.country} >Country</InputLabel>
                            <Select
                                options={countryList().getData()}
                                value={countrySearched}
                                onChange={handleCountrySearched}
                                labelId="demo-mutiple-name-label"
                                id="demo-mutiple-name"
                                multiple
                            >
                                {countryList().getData().map(val => {
                                    return <MenuItem value={val.label}>{val.label}</MenuItem>
                                })}
                            </Select>
                        </FormControl>
                    </div>
                </div>
            </div>
            <div className="SearchButton">
                <Button color="primary" round variant="contained" id="Search" onClick={() => searchCompany()}>Search</Button>
            </div>
            {data.length === 0 ? null :
                <div style={{ 'margin-top': '10px' }}>
                    <SearchResults data={data} />
                </div>
            }
        </React.Fragment>

    );
}
export default SearchDetails;