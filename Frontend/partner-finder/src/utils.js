import React, { forwardRef } from "react";

import { GridList, GridListTile } from '@material-ui/core';
import AddBox from "@material-ui/icons/AddBox";
import ArrowDownward from "@material-ui/icons/ArrowDownward";
import Check from "@material-ui/icons/Check";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import Clear from "@material-ui/icons/Clear";
import DeleteOutline from "@material-ui/icons/DeleteOutline";
import Edit from "@material-ui/icons/Edit";
import FilterList from "@material-ui/icons/FilterList";
import FirstPage from "@material-ui/icons/FirstPage";
import LastPage from "@material-ui/icons/LastPage";
import Remove from "@material-ui/icons/Remove";
import SaveAlt from "@material-ui/icons/SaveAlt";
import Search from "@material-ui/icons/Search";
import ViewColumn from "@material-ui/icons/ViewColumn";

const customStyle = { maxHeight: '110px', width: '240px', maxWidth: '250px'}

const EU_columns = [
  { title: "Name", field: "legalName", render: (rowData) => (
    <GridList cols={1} cellHeight='auto'>
    <div style={customStyle, {width: '180px'}}>{rowData.legalName}</div>
    </GridList>
      ) },
  { title: "Classification Type", field: "classificationType" },
  { title: "Country", field: "country" },
  { title: "Data Status", field: "dataStatus" },
  { title: "Number of EU Projects", field: "numberOfProjects" },
  { title: "Description", field: "description", render: (rowData) => (
    <GridList cols={1} cellHeight='auto'>
    <div style={customStyle}>{rowData.description}</div>
    </GridList>
      )},
  {
    title: "Consortium Role",
    field: "consorsiumRoles",
  },
];

const calls_columns = [
  { title: "Title", field: "title", render: (rowData) => (
    <GridList cols={1} cellHeight='auto'>
    <div style={customStyle}>{rowData.title}</div>
    </GridList>
      ) },
  { title: "Call Title", field: "callTitle" },
  { title: "Identifier", field: "identifier" },
  { title: "Type", field: "type" },
  { title: "Status", field: "status" },
  { title: "Deadline Date", field: "deadlineDate" },
  { title: "Submission Procedure Role", field: "sumbissionProcedure" },
];

const B2Match_columns = [
  { title: "Name", field: "participant_name" },
  { title: "Org. Name", field: "organization_name" },
  { title: "Type", field: "org_type" },
  { title: "Country", field: "address" },
  { title: "Website", field: "org_url" ,
  render: (rowData) => (

<a href={rowData.org_url} target="_blank" rel="noopener noreferrer" style={{color: 'white'}}>
      {rowData.org_url}{" "}
    </a>
  )},
  { title: "Description", field: "description", render: (rowData) => (
    <GridList style={customStyle} cols={1}>
    <div style={customStyle}>{rowData.description}</div>
    </GridList>
      ) },
];

const classificationTypesOptions = [
  {label :"Small or medium-size enterprise", value:"Small or medium-size enterprise"}, {label:"International Organisation", value:"International Organisation"},
  {label:"Higher or secondary education establishment", value: "Higher or secondary education establishment"},
  {label:"Research Organisation", value: "Research Organisation"}, {label:"Private for profit organisation", value:"Private for profit organisation"},
  {label:"Public organisation", value: "Public organisation"}, {label:"Other", value:"Other"}
];

const events_columns = [
  { title: "Name", field: "event_name" },
  { title: "Event Date", field: "date" },
  {
    title: "URL",
    field: "event_url",
    render: (rowData) => (
      <a href={rowData.event_url} style={{color: "white"}} target="_blank" rel="noopener noreferrer">
        {rowData.event_url}{" "}
      </a>
    ),
  },
  
];

const consorsiumRoles = [
  {label:"Coordinator", value:"Coordinator"}, {label:"Regular", value:"Regular"}
];

const tableIcons = {
  Add: forwardRef((props, ref) => (
    <AddBox
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Check: forwardRef((props, ref) => (
    <Check
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Clear: forwardRef((props, ref) => (
    <Clear
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Delete: forwardRef((props, ref) => (
    <DeleteOutline
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  DetailPanel: forwardRef((props, ref) => (
    <ChevronRight
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Edit: forwardRef((props, ref) => (
    <Edit
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Export: forwardRef((props, ref) => (
    <SaveAlt
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Filter: forwardRef((props, ref) => (
    <FilterList
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  FirstPage: forwardRef((props, ref) => (
    <FirstPage
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  LastPage: forwardRef((props, ref) => (
    <LastPage
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  NextPage: forwardRef((props, ref) => (
    <ChevronRight
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  PreviousPage: forwardRef((props, ref) => (
    <ChevronLeft
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  ResetSearch: forwardRef((props, ref) => (
    <Clear
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  Search: forwardRef((props, ref) => (
    <Search
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  SortArrow: forwardRef((props, ref) => (
    <ArrowDownward
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  ThirdStateCheck: forwardRef((props, ref) => (
    <Remove
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
  ViewColumn: forwardRef((props, ref) => (
    <ViewColumn
      {...props}
      ref={ref}
      style={{ backgroundColor: "#02203c", color: "white" }}
    />
  )),
};

const BACKEND_URL = "http://62.90.89.14:8000/api/";

export { EU_columns, B2Match_columns, BACKEND_URL, tableIcons, classificationTypesOptions, consorsiumRoles, calls_columns, events_columns };
