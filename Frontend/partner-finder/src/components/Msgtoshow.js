
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
            <DialogContent >
                <DialogContentText style={{color:'#02203c'}} id="textFontFamily">
                    {body}
                </DialogContentText>
            </DialogContent>
            <DialogActions id="textFontFamily" style={{ alignSelf: 'center'}}>
                <Button onClick={_handleClose} id="BackgroundColor" className= "Buttons" style={{color:"white"}} >
                    OK
          </Button>
            </DialogActions>
        </Dialog>
    );
}

export { Msgtoshow };