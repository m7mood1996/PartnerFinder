import React from "react";
import MaterialTable, { MTableToolbar } from "material-table";
import { TablePagination } from "@material-ui/core";
import { styled } from "@material-ui/core/styles";
import ResultsTable from "./ResultsTable";
import { Msgtoshow } from "./Msgtoshow";
import { BeatLoader } from "react-spinners";
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
import { EU_columns, BACKEND_URL, tableIcons } from "../utils";

const useStyles = makeStyles((theme) => ({
  title: {
    textAlign: "center",
    fontSize: 30,
  },
}));

const MyTablePagination = styled(TablePagination)((theme) => ({
  color: "white",
  fontSize: "16px",
}));

function CallsResultsTable(props) {
  const [data, setData] = React.useState(props.data);
  const [msgState, setMsgState] = React.useState({
    title: "",
    body: "",
    visible: false,
  });
  const [columns] = React.useState(props.columns);
  const [title] = React.useState(props.title);
  const [visible, setVisible] = React.useState(false);
  const [searchResult, setSearchResult] = React.useState([]);
  const [searchTitle, setSearchTitle] = React.useState("");
  const classes = useStyles();
  const [state, setState] = React.useState({
    loading: false,
  });
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
    setState({ loading: true });
    let url = new URL(BACKEND_URL + "calls/search_organizations/");
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
        if ("error" in resp) {
          setMsgState({
            title: "Failed",
            body: "Error while searching organizations",
            visible: true,
          });
          setState({ loading: false });
          setSearchTitle("");
          setSearchResult([]);
          setVisible(false);
        } else {
          setState({ loading: false });
          setSearchTitle(rowData["title"]);
          resp['EU'] = resp['EU'].map(val =>{
            return  {...val, 'consorsiumRoles': val.consorsiumRoles ? 'Coordinator' : 'Regular'  }
           })
          setSearchResult(resp.EU);
          setVisible(true);
        }
      })
      .catch((error) => {
        setMsgState({
          title: "Failed",
          body: "Error while searching organizations",
          visible: true,
        });
        setState({ loading: false });
        setSearchTitle("");
        setSearchResult([]);
        setVisible(false);
      });
  };

  const handleDelete = (oldData) => {
    let newData = [...data];
    newData.splice(newData.indexOf(oldData), 1);
    setData(newData);
  };

  return (
    <React.Fragment>
      <Msgtoshow
        {...msgState}
        handleClose={() => setMsgState({ ...msgState, visible: false })}
      />
      <div>
        {data.length === 0 ? null : (
          <MaterialTable
            style={{ color: "white", backgroundColor: "#02203c" }}
            icons={tableIcons}
            title={title}
            components={{
              Pagination: (props) => <MyTablePagination {...props} />,
              Toolbar: (props) => (
                <div
                  style={{
                    backgroundColor: "#02203c",
                    color: "white",
                  }}
                >
                  <MTableToolbar {...props} />
                </div>
              ),
            }}
            options={{
              actionsCellStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              cellStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              headerStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
                zIndex: 0,
              },
              searchFieldStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              filterCellStyle: {
                backgroundColor: "#02203c",
                textAlign: "center",
                color: "white",
              },
              showEmptyDataSourceMessage: false,
              header: true,
              exportButton: true,
              exportAllData: true,
            }}
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
                id="exitColor"
              >
                Exit
              </Button>
            </DialogActions>
          </Dialog>
        )}
      </div>
      {state.loading ? (
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
      ) : null}
    </React.Fragment>
  );
}
export default CallsResultsTable;
