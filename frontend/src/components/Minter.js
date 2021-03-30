import React from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function Minter(props) {
  const classes = useStyles();
  const [name, setName] = React.useState(null);
  const [description, setDescription] = React.useState(null);
  const [imageURL, setImageURL] = React.useState(null);
  const [attributes, setAttributes] = React.useState(null);
  
  const handleFormFieldChange = (event) => {
    switch (event.target.id) {
      case "name":
        setName(event.target.value);
        break;
      case "description":
        setDescription(event.target.value);
        break;
      case "imageURL":
        setImageURL(event.target.value);
        break;
      case "attributes":
        setAttributes(event.target.value);
        break;
      default:
        return null;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    props.onAuth(name, description, imageURL, attributes);
  };


  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="name"
            label="Name"
            name="name"
            autoComplete="name"
            autoFocus
            onChange={handleFormFieldChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            id="description"
            label="Description"
            name="description"
            autoComplete="description@example.com"
            onChange={handleFormFieldChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            name="imageURL"
            label="Image URL"
            type="imageURL"
            id="imageURL"
            autoComplete="current-imageURL"
            onChange={handleFormFieldChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            fullWidth
            name="attributes"
            label="Attributes"
            type="attributes"
            id="attributes"
            autoComplete="current-attributes"
            onChange={handleFormFieldChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Mint
          </Button>
        </form>
      </div>
    </Container>
  );
}
