import React from 'react';
import {Container, TextField,  InputLabel, Select, MenuItem } from '@material-ui/core';
import { createStyles, makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles(() =>
    createStyles({
        root: {
            display: 'flex',
            flex: 1,
            flexWrap: 'wrap',
            margin: 20,
        },
        input: {
            marginVertical: 10,
        },
        inputLabel: {
            marginTop: 20,
            marginBottom: 10
        }
    }),
);

export default function FormField(){
    const classes = useStyles();

    const longResponse = (questionText) =>
        <Container>
            <InputLabel className={classes.inputLabel}>{questionText}</InputLabel>
            <TextField multiline={true} margin={'normal'} variant="outlined" fullWidth={true} className={classes.input} />
        </Container>

    const dropDown = (questionText) =>
        <Container>
            <InputLabel className={classes.inputLabel}>{questionText}</InputLabel>
            <Select value={10} margin={'normal'} variant="outlined" fullWidth={true} className={classes.input} >
                <MenuItem value={10} margin={'normal'}>Ten</MenuItem>
                <MenuItem value={20} margin={'normal'}>Twenty</MenuItem>
                <MenuItem value={30} margin={'normal'}>Thirty</MenuItem>
            </Select>
        </Container>

    return(
        <form className={classes.root} autoComplete="off">
            {longResponse("What is a blocker you currently face?")}
            {longResponse("Why is this a blocker? What about the task is challenging for you, and what are you specifically stuck on?")}
            {longResponse("How does this blocker relate to progress in your overall research? In context to your research, what part does this challenge relate to?")}
            {dropDown("What sections and cells of the Practical Research Canvas, if any, does this map back to? If none please leave this blank ")}
        </form>
    );
}
