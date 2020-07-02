
import React from "react";

import {
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    DialogContentText,

} from '@material-ui/core/';



const Msgtoshow = ({ title, body, visible, handleClose }) => {


    function _handleClose() {
        handleClose();
    }

    return (
        <Dialog
            disableBackdropClick
            disableEscapeKeyDown
            open={visible}
            onClose={_handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
        >
            <DialogTitle id="textFontFamily" style={{color: 'red'}}>{title}</DialogTitle>
            <DialogContent style={{backgroundColor: '#ececec'}}>
                <DialogContentText style={{color:'#02203c'}} id="textFontFamily">
                    {body}
                </DialogContentText>
            </DialogContent>
            <DialogActions style={{backgroundColor: '#ececec', alignContent: 'center'}}>
                <Button onClick={_handleClose} style={{color:"#02203c", marginRight: '100px'}} id="textFontFamily" >
                    OK
          </Button>
            </DialogActions>
        </Dialog>
    );
}

export { Msgtoshow };