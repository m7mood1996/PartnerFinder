import React from "react";
import MaterialTable from "material-table";
import { forwardRef } from "react";
import ResultsTable from "./ResultsTable";
import {
  makeStyles,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText,
} from "@material-ui/core/";

import SearchIcon from "@material-ui/icons/Search";
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
import { EU_columns } from '../utils';


const useStyles = makeStyles((theme) => ({
  title: {
    textAlign: "center",
    fontSize: 30,
  },
}));

const tableIcons = {
  Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => (
    <ChevronRight {...props} ref={ref} />
  )),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => (
    <ChevronLeft {...props} ref={ref} />
  )),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />),
};

// const EU_columns = [
//   { title: "Name", field: "legalName" },
//   { title: "Type", field: "classificationType" },
//   { title: "Country", field: "country" },
//   { title: "Data Status", field: "dataStatus" },
//   { title: "Number of EU Projects", field: "numberOfProjects" },
//   { title: "Description", field: "description" },
//   { title: "Consorsium Role", field: "consorsiumRoles" },
// ];

function CallsResultsTable(props) {
  const [data, setData] = React.useState(props.data);
  const [columns] = React.useState(props.columns);
  const [title] = React.useState(props.title);
  const [visible, setVisible] = React.useState(false);
  const [searchResult, setSearchResult] = React.useState([]);
  const [searchTitle, setSearchTitle] = React.useState("");
  const classes = useStyles();

  React.useEffect(
    function effectFunction() {
      setData(props.data);
    },
    [props.data]
  );

  const _handleClose = () => {
    setVisible(false);
    setSearchResult([]);
    setSearchTitle("");
  };

  const searchOrganizations = (rowData) => {
    //TODO: loading
    console.log("COLSS", EU_columns)
    let url = new URL("http://127.0.0.1:8000/api/calls/search_organizations/");
    let params = {
      data: JSON.stringify({ ccm2Id: rowData["ccm2Id"] }),
    };
    Object.keys(params).forEach((key) =>
      url.searchParams.append(key, params[key])
    );
    fetch(url, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((resp) => {
        //TODO: end loading
        setSearchTitle(rowData["title"]);
        setSearchResult(resp.EU);
        setVisible(true);
      })
      // TODO: show error message and end loading
      .catch((error) => console.log(error));
  };

  const handleDelete = (oldData) => {
    let newData = [...data];
    newData.splice(newData.indexOf(oldData), 1);
    setData(newData);
  };

  return (
    <React.Fragment>
      <div>
        {data.length === 0 ? null : (
          <MaterialTable
            icons={tableIcons}
            title={title}
            options={{ exportButton: true }}
            columns={columns}
            data={data}
            editable={{
              onRowDelete: (oldData) =>
                new Promise((resolve) => {
                  setTimeout(() => {
                    resolve();
                    handleDelete(oldData);
                  }, 600);
                }),
            }}
            actions={[
              {
                icon: SearchIcon,
                tooltip: "Search Organizations",
                onClick: (event, rowData) => {
                  searchOrganizations(rowData);
                },
              },
            ]}
          />
        )}
        {searchResult.length === 0 ? null : (
          <Dialog
            fullScreen={true}
            disableBackdropClick
            disableEscapeKeyDown
            open={visible}
            onClose={_handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                <ResultsTable
                  title={"Results For Call " + searchTitle}
                  data={searchResult}
                  columns={EU_columns}
                />
              </DialogContentText>
            </DialogContent>
            <DialogActions
              style={{
                justifyContent: "center",
              }}
            >
              <Button
                onClick={_handleClose}
                variant="contained"
                color="secondary"
                className={classes.button}
              >
                Exit
              </Button>
            </DialogActions>
          </Dialog>
        )}
      </div>
    </React.Fragment>
  );
}
export default CallsResultsTable;
