import React from 'react'
import MaterialTable from 'material-table';
import { forwardRef } from 'react';

import AddBox from '@material-ui/icons/AddBox';
import ArrowDownward from '@material-ui/icons/ArrowDownward';
import Check from '@material-ui/icons/Check';
import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import Clear from '@material-ui/icons/Clear';
import DeleteOutline from '@material-ui/icons/DeleteOutline';
import Edit from '@material-ui/icons/Edit';
import FilterList from '@material-ui/icons/FilterList';
import FirstPage from '@material-ui/icons/FirstPage';
import LastPage from '@material-ui/icons/LastPage';
import Remove from '@material-ui/icons/Remove';
import SaveAlt from '@material-ui/icons/SaveAlt';
import Search from '@material-ui/icons/Search';
import ViewColumn from '@material-ui/icons/ViewColumn';


const tableIcons = {
    Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
    Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
    Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
    DetailPanel: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
    Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
    Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
    FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
    LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
    NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    PreviousPage: forwardRef((props, ref) => <ChevronLeft {...props} ref={ref} />),
    ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
    SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
    ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
    ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />)
};

const EU_columns = [
    { title: 'Name', field: 'legalName' },
    { title: 'Type', field: 'classificationType' },
    { title: 'Country', field: 'country' },
    { title: 'Data Status', field: 'dataStatus' },
    { title: 'Number of EU Projects', field: 'numberOfProjects' },
    { title: 'Description', field: 'description' },
    { title: 'Consorsium Role', field: 'consorsiumRoles' }
]

const B2Match_columns = [
    { title: 'Name', field: 'participant_name' },
    { title: 'Org. Name', field: 'organization_name' },
    { title: 'Type', field: 'org_type' },
    { title: 'Country', field: 'address' },
    { title: 'Website', field: 'org_url' },
    //{ title: 'Event Name', field: 'event' },
    { title: 'Description', field: 'description' }
]



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

function handleDataChange(data) {
    let tempData = data;
    let eu = getRelativeData(tempData['EU']);
    tempData = { ...tempData, 'EU': eu };

    return tempData;
}



function SearchResults(props) {
    const [data, setData] = React.useState([]);

    React.useEffect(function effectFunction() {
        setData(handleDataChange(props.data))
    }, [props.data]);

    return (
        <React.Fragment>
            <div>
                {data.length === 0 ? null :
                    <MaterialTable
                        icons={tableIcons}
                        title="EU Funding and Tenders Portal Results"
                        options={{ exportButton: true }}
                        columns={EU_columns}
                        data={data.EU}
                    />}
            </div>
            <div style={{ 'margin-top': '10px' }}>
                {data.length === 0 ? null :
                    <MaterialTable
                        icons={tableIcons}
                        title="B2MATCH Results"
                        options={{ exportButton: true }}
                        columns={B2Match_columns}
                        data={data.B2MATCH}
                    />}
            </div>
        </React.Fragment>
    );
}
export default SearchResults;