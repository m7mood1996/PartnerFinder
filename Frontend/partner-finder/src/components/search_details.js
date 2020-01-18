import React, { useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import Select from '@material-ui/core/Select';
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
// import SearchResults from './searchResults'
import SearchResults from './searchResults';

const columns = [
    'legalName',
    'businessName',
    'classificationType',
    'country', 'city',
    'description',

]

function SearchDetails() {
    const [type, setType] = React.useState('');
    const [country, setCountry] = React.useState('');
    const [value, setValue] = React.useState('');
    const [keyword, setKeyword] = React.useState('');
    const [field, setField] = React.useState('');
    const [name, setName] = React.useState('');
    const [checked, setChecked] = React.useState(false);
    const [data, setData] = React.useState([]);
    const [orgsByCountries, setOrgsByCountries] = React.useState([]);
    const [orgsByTags, setOrgsByTags] = React.useState([]);


    const companyTypesOptions = [
        "SME", "International organisation", "Higher or secondary education",
        "Research organisation", "Private for profit organisation", "Public organisation", "other"
    ]
    const toggleChecked = () => {
        setChecked(prev => !prev);
    };

    const handleChange = event => {
        setType(event.target.value);
    };
    const handleCountry = event => {
        setCountry(event.target.value);
    };
    const handleInputChange = event => {
        setValue(event.target.value === "" ? "" : Number(event.target.value));
    }
    const handleBlur = () => {
        if (value < 1) {
            setValue(1);
        } else if (value > 100) {
            setValue(100);
        }
    };




    const getOrgsByTags = (tags) => {
        // console.log("COUNTRIES")
        let url = new URL('http://127.0.0.1:8000/api/organizations/getOrganizationsByTags/')
        // let params = {'tags': tags}
        let params = { 'data': tags }
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        // url.search = new URLSearchParams(params)
        fetch(url, {
            method: 'GET'

        }).then(res => res.json())
            .then(resp => setOrgsByTags(resp))
            // .then(resp => console.log(resp))
            .catch(error => console.log(error))
    }

    const getRelativeData = (arr) => {
        let res = arr.map(org => {
            console.log("Curr", org)
            let temp = org
            let address = temp.address
            delete temp.pic
            delete temp.address
            temp = { ...temp, 'city': address.city, 'country': address.country }

            return temp
        })

        console.log(res)
        return res
    }
    useEffect(() => {
        if (orgsByCountries !== [] && orgsByTags !== []) {

            if (data.length === 0) {
                let res = getRelativeData(getIntersect(orgsByCountries, orgsByTags))
                console.log(res)
                setData(res)
                console.log("Set DATA")
            }
            // console.log("intersect", getIntersect(orgsByCountries, orgsByTags))
        }

    }, [orgsByCountries, orgsByTags])

    const getOrgsByCountries = (countries) => {

        let url = new URL('http://127.0.0.1:8000/api/organizations/getOrganizationsByCountries/')
        // let params = {'tags': tags}
        let params = { 'data': countries }
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
        // url.search = new URLSearchParams(params)
        fetch(url, {
            method: 'GET'

        }).then(res => res.json())
            .then(resp => setOrgsByCountries(resp))
            // .then(resp => console.log(resp))
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
        console.log("HERE")
        // let arr1 = [{'pic': 123, 'name': 'ss'}, {'pic':434, 'name':'nnn'}]
        // console.log(isExist(arr1, 434))
        getOrgsByCountries(['Italy', 'Germany'])
        getOrgsByTags(['materials engineering', 'security'])

        // while(orgsByCountries === [] || orgsByTags === []){
        //     let i = 0;
        // }

        // console.log("Here")
        // console.log('arr1', orgsByCountries,'\narr2', orgsByTags)
        // console.log('intersect', getIntersect(orgsByCountries, orgsByTags))


        // setData(['blabla'])
    }
    return (
        <React.Fragment>
            <div className="first_row">
                <div className="SearchTab">
                    <h1>Clients Organization Name:</h1>
                    <form className={SearchDetails.root} noValidate autoComplete="off">
                        <TextField id="company_name" label="Name" variant="outlined" />
                    </form>
                </div>
                <div className="type">
                    <h1>Clients Organization Type:</h1>
                    <FormControl className={SearchDetails.formControl} id="tab">
                        <InputLabel id="company_type">Type</InputLabel>
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
                    <h1>Country:</h1>
                    <FormControl className={SearchDetails.formControl} id="tab">
                        <InputLabel id="company_type">Country</InputLabel>
                        <Select
                            options={countryList().getData()}
                            value={country}
                            onChange={handleCountry}
                        >
                            {countryList().getData().map(val => {
                                return <MenuItem value={val.value}>{val.label}</MenuItem>
                            })}
                        </Select>
                    </FormControl>
                </div>
            </div>
            <div className="second_row">
                <div className="profit">
                    <h1>Profit:</h1>
                    <FormGroup style={{ 'margin-top': '5px' }}>
                        <FormControlLabel
                            control={<Switch size="medium" checked={checked} onChange={toggleChecked} />}
                            label="Yes"
                        />
                    </FormGroup>
                </div>
                <div className="Partners">
                    <h1>Number Of Partners: </h1>
                    <Grid container spacing={2} alignItems="center" style={{ 'margin-left': '5px' }} >
                        <Grid item>
                            <Input
                                className={SearchDetails.input}
                                id="company_type"
                                value={value}
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
            <div className="third_row">
                <div className="SearchTab">
                    <h1>Field:</h1>
                    <form className={SearchDetails.root} noValidate autoComplete="off">
                        <TextField id="company_name" label="Field" variant="outlined"
                            value={setField}
                        />
                    </form>
                </div>
                <div className="SearchTab">
                    <h1>Keyword:</h1>
                    <form className={SearchDetails.root} noValidate autoComplete="off">
                        <TextField id="company_name" label="Keyword" variant="outlined"
                            value={keyword}
                        // onChange={}
                        />
                    </form>
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
