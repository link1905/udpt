import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import { useForm } from "@mantine/form";
import { useMutation } from "@tanstack/react-query";
import { requestLogin } from "../services/account/login.ts";
import { FormHelperText } from "@mui/material";
import { AUTH_LOCALSTORAGE_KEY } from "../services/client.ts";

const defaultTheme = createTheme();

export default function SignIn() {
  const navigate = useNavigate();

  const { mutate, isLoading, error } = useMutation(requestLogin, {
    onSuccess(data) {
      const { token, user } = data;
      localStorage.setItem(AUTH_LOCALSTORAGE_KEY, token);
      localStorage.setItem("user", JSON.stringify(user));

      console.log("User data:", user);
      console.log("User data:", user);
      if (user && user.fields.is_staff) {
        console.log("User is staff, navigating to /admin/manage-threads");
        navigate("/admin/manage-threads");
      } else {
        console.log("User is not staff, navigating to /");
        navigate("/");
      }
    },
  });
  const form = useForm({
    initialValues: {
      username: "",
      password: "",
    },
  });
  const handleSignUp = () => {
    navigate("/signup");
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Grid container component="main" sx={{ height: "100vh" }}>
        <CssBaseline />
        <Grid
          item
          xs={false}
          sm={4}
          md={7}
          sx={{
            backgroundImage:
              "url(https://source.unsplash.com/random?wallpapers)",
            backgroundRepeat: "no-repeat",
            backgroundColor: (t) =>
              t.palette.mode === "light"
                ? t.palette.grey[50]
                : t.palette.grey[900],
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        />
        <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
          <Box
            sx={{
              my: 8,
              mx: 4,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign in
            </Typography>
            <Box
              component="form"
              noValidate
              onSubmit={form.onSubmit((loginValues) => {
                mutate(loginValues);
              })}
              sx={{ mt: 1 }}
            >
              {!!error && (
                <FormHelperText error>
                  {String(error.response.data.message)}
                </FormHelperText>
              )}
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="Username"
                autoComplete="username"
                autoFocus
                {...form.getInputProps("username")}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                {...form.getInputProps("password")}
              />
              <FormControlLabel
                control={<Checkbox value="remember" color="primary" />}
                label="Remember me"
              />
              <Button
                disabled={isLoading}
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
              <Grid container>
                <Grid item xs>
                  <Link href="#" variant="body2">
                    Forgot password?
                  </Link>
                </Grid>
                <Grid item>
                  <Link
                    onClick={handleSignUp}
                    className="cursor-pointer"
                    variant="body2"
                  >
                    {"Don't have an account? Sign Up"}
                  </Link>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </Grid>
      </Grid>
    </ThemeProvider>
  );
}
