import {} from "react-router";
import { createBrowserRouter } from "react-router-dom";
import { Layout } from "../components/layout";
import { CreateQuestionPage } from "./question/create.tsx";
import { ViewQuestionPage } from "./question/view.tsx";
import { ListQuestionPage } from "./question/list.tsx";
import { HomePage } from "./home.tsx";
import SignIn from "./sign-in.tsx";
import SignUp from "./sign-up.tsx";
import { LoginGuard } from "../components/login-guard/login-guard.tsx";
import {AccountPage} from "./account.tsx";

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <LoginGuard>
        <Layout />
      </LoginGuard>
    ),
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/question/create",
        element: <CreateQuestionPage />,
      },
      {
        path: "/question/:id",
        element: <ViewQuestionPage />,
      },
      {
        path: "/question",
        element: <ListQuestionPage />,
      },
      {
        path: "/account",
        element: <AccountPage />,
      },
    ],
  },
  {
    path: "/signin",
    element: <SignIn />,
  },
  {
    path: "/signup",
    element: <SignUp />,
  },
]);
