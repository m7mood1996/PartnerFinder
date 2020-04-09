import React, { useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
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
import SearchResults from './searchResults';
import { WithContext as ReactTags } from 'react-tag-input';


const KeyCodes = {
    comma: 188,
    enter: 13,
};

const delimiters = [KeyCodes.comma, KeyCodes.enter];


function SearchDetails() {
    const [type, setType] = React.useState('');
    const [country, setCountry] = React.useState('');
    const [countrySearched, setCountrySearched] = React.useState('');
    const [number, setNumber] = React.useState('');
    const [tags, setTags] = React.useState([]);
    const [field, setField] = React.useState('');
    const [name, setName] = React.useState('');
    const [checked, setChecked] = React.useState(false);
    const [data, setData] = React.useState([]);
    const [orgsByCountries, setOrgsByCountries] = React.useState([]);
    const [orgsByTags, setOrgsByTags] = React.useState([]);
    const [formState, setFormState] = React.useState({
        name :false,
        field : false,
        country : false,
        countrySearched : false,
        type : false, 
        tags : false,
        numbers : false,
    })

    const companyTypesOptions = [
        "SME", "International Organization", "Higher or Secondary Education",
        "Research Organization", "Private for Profit Organization", "Public Organization", "Other"
    ]

    const deleteTag = (idx) => {
        let newTags = tags.filter((val, i) => i !== idx)
        setTags(newTags)
    }

    const dragTag = (tag, currPos, newPos) => {
    }

    const addTag = (tag) => {
        setTags([...tags, tag])
        
    }

    const changeTagInput = (event) => {
        if (event.length !== 0) {
            setFormState({...formState, tags:false})
        }
    }
    const toggleChecked = () => {
        setChecked(prev => !prev);
    };
    const changeName = event => {
        setName(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({...formState, name: false})
    }
    const handleChange = event => {
        setType(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({...formState, type: false})
    
    };
    const changeField = event => {
        setField(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({...formState, field: false})
    
    };
    const handleCountry = event => {
        setCountry(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({...formState, country: false})
    
    };
    const handleCountrySearched = event => {
        setCountrySearched(event.target.value);
        if (event.target.value.length !== 0)
            setFormState({...formState, countrySearched: false})
    };
    const handleInputChange = event => {
        setNumber(event.target.value === "" ? "" : Number(event.target.value));
        if (event.target.value.length !== 0)
            setFormState({...formState, number: false})
    }
    const handleBlur = () => {
        if (number < 1) {
            setNumber(1);
        } else if (number > 100) {
            setNumber(100);
        }
    };
    const formValidation = () => {
        let res = {}
        let check = false
        if(name === '' || name.length === 0 ){
            res = {...res, name: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, name: false}
        }

        if(country.length === 0 || country === undefined || country === null){
            res = {...res, country: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, country: false}
        }
        if(countrySearched.length === 0 || countrySearched === undefined || countrySearched === null){
            res = {...res, countrySearched: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, countrySearched: false}
        }
        if(field.length === 0 || field === undefined || field === null){
            res = {...res, field: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, field: false}
        }
        if(type.length === 0 || type === undefined || type === null){
            res = {...res, type: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, type: false}
        }
        if(number.length === 0 || number === undefined || number === null){
            res = {...res, number: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, number: false}
        }
        if(tags.length === 0 || tags === undefined || tags === null){
            res = {...res, tags: true}
            setFormState(res)
            check = true
        }  
        else{
            res = {...res, tags: false}
        }

 
        setFormState(res)
        return check
    }



    const getOrgsByTags = (tags) => {
        let url = new URL('http://127.0.0.1:8000/api/organizations/getOrganizationsByTags/')
        let params = { 'data': tags }
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        fetch(url, {
            method: 'GET'

        }).then(res => res.json())
            .then(resp => setOrgsByTags(resp))
            .catch(error => console.log(error))
    }

    const getRelativeData = (arr) => {
        let res = arr.map(org => {
            let temp = org
            let address = temp.address
            delete temp.pic
            delete temp.address
            temp = { ...temp, 'city': address.city, 'country': address.country }

            return temp
        })

        return res
    }
    
    useEffect(() => {
        if (orgsByCountries !== [] && orgsByTags !== []) {

            if (data.length === 0) {
                let res = getRelativeData(getIntersect(orgsByCountries, orgsByTags))
                setData(res)
            }
        }

    }, [orgsByCountries, orgsByTags])

    const getOrgsByCountries = (countries) => {
        let url = new URL('http://127.0.0.1:8000/api/organizations/getOrganizationsByCountries/')
        let params = { 'data': countries }
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        fetch(url, {
            method: 'GET'

        }).then(res => res.json())
            .then(resp => setOrgsByCountries(resp))
            .catch(error => console.log(error))

    }
    const isExist = (arr, pic) => {
        arr = arr.filter(val => val.pic === pic)
        return arr.length !== 0
    }
    const getIntersect = (arr1, arr2) => {
        return arr1.filter(org => isExist(arr2, org.pic))
    }
    const searchCompany = () => {
        if(formValidation()){
            setData([])
            return;
        }else{
            setData([])
            getOrgsByCountries([countrySearched])
            let Tags = tags.map(tag => tag.text)
            getOrgsByTags(Tags)
        }
    }
    return (
        <React.Fragment>
            <div className="Org_Details">
                <h1 style={{'margin-left':'1%'}}>Organization Details</h1>
            <div className="first_row">
                <div className="SearchTab">
                    <h1>Name</h1>
                    <form className={SearchDetails.root}  autoComplete="off">
                        <TextField  id="company_name" onChange={changeName} label="Name" variant="outlined" error={formState.name}/>
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
            </div>
            
            <div className="second_row">
                <div className="SearchTab">
                    <h1>City</h1>
                    <form className={SearchDetails.root} noValidate autoComplete="off">
                        <TextField id="company_name" label="City" variant="outlined" />
                    </form>
                </div>
                <div className="SearchTab" >
                    <h1>Profit / Non-profit</h1>
                    <FormGroup style={{ 'margin-top': '5px' }}>
                        <FormControlLabel
                            control={<Switch size="medium" checked={checked} onChange={toggleChecked} />}
                            label="Yes"
                        />
                    </FormGroup>
                </div>
            </div>
                
            </div>
            <hr  style={{'margin-top':'3%','border': '2px solid gray','border-radius': '5px', 'marginLeft': '7%', 'marginRight': '7%'}}/>
            <div className="Search_Details">
                <h1 style={{'margin-left':'1%'}}>Search Details</h1>
                <div className="third_row">
                    <div className="SearchTab">
                        <h1>Field</h1>
                        <form className={SearchDetails.root} noValidate autoComplete="off">
                            <TextField id="company_name" label="Field" variant="outlined"
                                onChange={changeField}
                                error={formState.field}
                            />
                        </form>
                    </div>
                    <div className="country">
                    <h1>Country</h1>
                    <FormControl className={SearchDetails.formControl} id="tab" >
                        <InputLabel id="company_type" error={formState.countrySearched} >Country</InputLabel>
                        <Select
                            options={countryList().getData()}
                            value={countrySearched}
                            onChange={handleCountrySearched}
                        >
                            {countryList().getData().map(val => {
                                return <MenuItem value={val.label}>{val.label}</MenuItem>
                            })}
                        </Select>
                    </FormControl>
                </div>
                <div className="Partners">
                    <h1>Number Of Partners</h1>
                    <Grid container spacing={2} alignItems="center" style={{ 'margin-left': '5px' }} >
                        <Grid item>
                            <Input
                                error={formState.number}
                                className={SearchDetails.input}
                                id="company_type"
                                value={number}
                                margin="dense"
                                onChange={handleInputChange}
                                onBlur={handleBlur}
                                inputProps={{
                                    step: 1,
                                    min: 1,
                                    max: 100,
                                    type: "number",
                                    "aria-labelledby": "input-slider"
                                }}
                            />
                        </Grid>
                    </Grid>
                </div>
                </div>
                <div className="fourth_row">
                <div className="SearchTab">
                    <h1>Tags and Keywords</h1>
                            <ReactTags tags={tags}
                                handleDelete={deleteTag}
                                handleAddition={addTag}
                                handleDrag={dragTag}
                                delimiters={delimiters}
                                handleInputChange={changeTagInput}
                                />

                               {formState.tags ? <Typography variant="caption" display="block" gutterBottom style= {{'color': 'red'}}>
                                    Enter at least one tag
                                    </Typography> : null}
                        
                        
                </div>
                </div>
            </div>
            <div className="SearchButton">
                <Button variant="contained" id="Search" onClick={() => searchCompany()}>Search</Button>
            </div>
            {data.length === 0 ? null : <div >
                <SearchResults data={data} />
            </div>
            }

        </React.Fragment>
    )
}
export default SearchDetails;
